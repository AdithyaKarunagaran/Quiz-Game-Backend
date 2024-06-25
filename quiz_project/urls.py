"""
URL configuration for quiz_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from quiz_game import views as qz

urlpatterns = [
    path('admin/', admin.site.urls),
    path('question/', qz.create_question, name='question'),
    path('get_question/', qz.get_question, name='get_question'),
    path('get_questions/', qz.get_questions, name='get_questions'),
    path('create_question/', qz.create_question, name='create_question'),
    path('delete_question/', qz.delete_question, name='delete_question'),
    path('register/', qz.user_register, name='register'),
    path('quiz_submission/', qz.submit_quiz, name='quiz_submission'),
    path('get_results/', qz.get_results, name='get_results'),
    path('admin_login/', qz.admin_login, name='admin_login'),
]
