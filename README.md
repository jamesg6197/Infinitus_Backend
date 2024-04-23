# PDF Chat Application Backend

## This is to be set up and ran first before starting the frontend application.

## Overview
This Django application enables users to upload PDF files and engage in chat discussions about the content of these PDFs. It is designed to support user authentication, PDF management, and real-time chat functionality.

## Prerequisites
- Python 3.8 or higher
- Django 3.2 or higher
- Additional libraries as listed in `requirements.txt`

## Setup Instructions

### Clone the repository
To get started, clone this repository to your local machine:


```
git clone https://github.com/jamesg6197/Infinitus_Backend.git
```
### Once cloned, we need to ensure all the dependencies are installed.

We also need to ensure that we have a .env file which contains an OPEN_AI_KEY that allows us to access the LLMs

```
pip install -r requirements.txt
```
### After installing the dependencies, we can run the server

```
python manage.py runserver
```

Ensure the backend is running at 127.0.0.1 in order for the frontend requests to be sent to the correct IP address

### Technologies Used

Django: Python web framework that uses SQlite as the database connector.
Django-jwt tokens: Supports authentication with the frontend with the use of tokens.
Langchain: Python module with LLM and Vector database support.
PyPDF2: Python module that allows PDF parsing support.

### Limitations 

I initially wanted to deploy the application to a public URL using vercel. However, I had problems with deployment using Vercel because it does not support SQLite databases. I tried switching to a MySQL database, however, I ran into many more errors trying to switch. If I had more time, I would try out different deployment applications.

The PDF parser does not work well with Scanned PDFs of text. This is a problem with PyPDF2. However, with more time, I would work with another library or build my own parser with OCR to overcome this issue.

