import os
from django.apps import AppConfig
from django.core.files import File
from PyPDF2 import PdfReader

import uuid


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    def ready(self):
        from .models import PDFDocument
        try:
            
            if not PDFDocument.objects.filter(title='Startup Playbook.pdf').exists():
                
                pdf_path = os.path.join(os.getcwd(), 'chat', 'initial_data', 'Startup Playbook.pdf')
                with open(pdf_path, 'rb') as f:
                    reader = PdfReader(f)
                    content = ''
                    for page in reader.pages:
                        content += page.extract_text() or ''
                    print("this is the content", content)
                    pdf_document = PDFDocument(
                        user= None,  # Adjust as necessary
                        title='Startup Playbook.pdf',
                        documentContent=content
                    )
                    pdf_document.save()
                    f.seek(0)
                    
                    
        except Exception as e:
            print(f"Error setting up initial PDF: {str(e)}")