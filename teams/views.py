import re
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import user_passes_test, login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from teams.models import *
# from backend.forms import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
# from backend.task import *
from ckeditor.fields import RichTextField
# from .decorators import *
from django.template.loader import render_to_string
import pandas as pd


def login_method(request):
    context = {}
    if request.user.is_authenticated:
        return render(request, 'frontend/demo.html') #redirect('admin_page')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        username = request.POST.get('email')
        password = request.POST.get('password')
        user_exists = User.objects.filter(email=username).exists()
        if user_exists:
            try:
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                print("You are now logged in as", username)
                return redirect('homepage')
            except:
                messages.info(request, f"Incorrect Password for {username}")
                errors = "Incorrect Password"
                print("Incorrect Password")
                context['errors'] = errors
        else:
            messages.info(request, f"{username} does not exist.")
            print("username does not exists.")
            errors = "Username/Email does not exists."
            context['errors'] = errors
    
    form = AuthenticationForm()
    context['form'] = form
    return render(request, 'frontend/login.html')


def logout_method(request):
    logout(request)
    print("Logged out successfully!")
    return redirect("homepage")


def homepage(request):
    dataframe = pd.read_excel('static/excel_file/data_file.xlsx')
    params = {}
    if request.method == 'POST':
        data = request.POST.get('btn')
        dataframe_values = dataframe[dataframe[data]==1]['File Name'].values
        params = {
            'dataframe_values': dataframe_values,
            'data': data,
            'fetching_data': True,
        }
    return render(request, "frontend/demo.html", params)