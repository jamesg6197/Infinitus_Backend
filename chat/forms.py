from django import forms

class PDFUploadForm(forms.Form):

    pdf_document = forms.FileField(label = 'Upload a PDF', required=True)