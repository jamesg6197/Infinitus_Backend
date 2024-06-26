"""infinitus_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from chat.views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('/', home, name = 'home'),
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name = 'auth_register'),
    path('login/', LoginView.as_view(), name = 'auth_login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('upload_pdf/', UploadPDFView.as_view(), name = 'upload_pdf'),
    path('ask_question/', AskQuestion.as_view(), name = 'ask_question'),
    path('token/', 
          jwt_views.TokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
     path('token/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh')

]
