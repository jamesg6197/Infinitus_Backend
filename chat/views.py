from PyPDF2 import PdfReader
import json
from django.http import JsonResponse

from langchain_community.llms.openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks.manager import get_openai_callback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import get_user_model # Import your custom form
from django.contrib.auth.models import User

from .forms import *
from .models import *
from dotenv import load_dotenv

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, email, password, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None


class RegisterView(APIView):

    """
    Handles user registration.

    :param request: HTTP request.
    :return: Rendered registration page or redirects to registration page.
    """
    permission_classes = [AllowAny]
    def post(self, request):

        try:
            data = request.data
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            username = data.get("username")
            password = data.get("password")
            email = data.get("email")
            
            user = User.objects.filter(username = username)
            
            if user.exists():
                return JsonResponse({'message': 'Username already taken!'}, status = 400)
            
            user_email = User.objects.filter(email = email)
            
            if user_email.exists():
                return JsonResponse({'message': 'Email already taken!'}, status = 400)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            
            user.set_password(password)
            user.save()
            token = RefreshToken.for_user(user)
            return Response({'message': 'User registered and logged in successfully', "access":str(token.access_token)})
        except:
            return Response({'message': 'Failed to register User.'}, status = 400)
        
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Post request to authenticate user log in. 
        
        Parameters
        ----------
        first : request
            Data object. Fields that represent a User's attempt to log in. 
        Returns
        -------

        Response({"access": str(token.access_token), "refresh": str(token)})

        Raises
        ------
        Response({"error": "Invalid login credentials"})
            Invalid login credentials.
        
        JsonResponse({'error': 'Invalid JSON data'}, status=400)
            Json body of request was not properly formatted. 
        """
        try:
            data = json.loads(request.body)

                # Extract email and password from the JSON data
            email = data["email"]
            password = data["password"]
            email_backend = EmailBackend()
                # Authenticate the user
            user = email_backend.authenticate(email=email, password=password)
            if user is not None:
                token = RefreshToken.for_user(user)
                return Response({"access": str(token.access_token), "refresh": str(token)})
            else:
                return Response({"error": "Invalid login credentials"})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

class LogoutView(APIView):

    permission_classes = [IsAuthenticated,]
    def post(self, request):
        """
        Post request to log out a user.
        
        Parameters
        ----------
        request : Request
            Data object. Fields that represent a User's attempt to log out. 
        
        Returns
        -------
        Response(status=status.HTTP_205_RESET_CONTENT)
            Successful logout.

        Raises
        ------
        Response(status=status.HTTP_400_BAD_REQUEST)
            Failed logout due to an exception.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

def get_pdf_text(pdf):
    pdf_reader = PdfReader(pdf)
    return ''.join(page.extract_text() for page in pdf_reader.pages)

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_text(text)

    return chunks

def get_similarity_search_structure(text_chunks):
    open_ai_embeddings = OpenAIEmbeddings()
    structure = FAISS.from_texts(text_chunks, open_ai_embeddings)
    return structure

class UploadPDFView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            print(request.POST, request.FILES)
            form = PDFUploadForm(request.POST, request.FILES)
            if form.is_valid():
                document = request.FILES['pdf_document']
                pdf = PDFDocument(user = request.user, title=document.name)
                pdf.documentContent = get_pdf_text(document)
                pdf.save()
                return Response({'message': 'Uploaded Successfully!'})
            else:
                return Response({'message': "Upload failed", "errors": form.errors})
        except Exception as e:
            print(e)
            return Response({'message:': "Received Error!"})
        
class AskQuestion(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            load_dotenv()  # Loading environment variables if needed
            data = request.data
            chat_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
            chat_response = ''
            user_question = data.get('question')

            # Include both user's documents and the default startup playbook
            pdfs = PDFDocument.objects.filter(
                Q(user=request.user) | Q(title='Startup Playbook.pdf')
            )
            
            # Concatenate text from all relevant PDFs
            text = " ".join(pdf.documentContent for pdf in pdfs)

            # Processing the text to form a knowledge base
            text_chunks = get_text_chunks(text)
            knowledge_base = get_similarity_search_structure(text_chunks)

            # Using the knowledge base to get documents related to the question
            docs = knowledge_base.similarity_search(user_question)

            # Setting up and querying the language model
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)

            chat_response = response
            chat_message = ChatMessage(user=request.user, message=user_question, answer=chat_response)
            chat_message.save()
            
            # Log the response
            print(response)
            print(chat_response, chat_history, user_question)

            # Return the chat response and question to the client
            context = {'chat_response': chat_response, 'user_question': user_question}
            return Response(context)
        except Exception as e:
            print(e)
            return Response({'message': "Received Error!"})