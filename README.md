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
