from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from models import *

def index(request):
    return render(request, 'login_and_registration/index.html')

def success(request):
    if request.POST['submit'] == 'Register':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)
            return redirect('/index')

        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = password)
        context = {
            'name': user.first_name,
            'status': 'registered'
        }
        return render(request, 'login_and_registration/success.html', context)

    if request.POST['submit'] == 'Login':
        user = User.objects.filter(email = request.POST['email'])
        if not user:
            # request.flash.now['email_error'] = 'User does not exist'
            messages.add_message(request, messages.INFO, 'User does not exist')
            return redirect('/index')
        else:
            for user in user:
                user_password = user.password
            if bcrypt.checkpw(request.POST['password'].encode(), user_password.encode()):
                context = {
                    'name': user.first_name,
                    'status': 'logged in',
                    'email_error': 'User does not exist'
                }
                return render(request, 'login_and_registration/success.html', context)
            else:
                # request.flash.now['password_error'] = 'Password is incorrect'
                messages.add_message(request, messages.INFO, 'Password is incorrect')
                return redirect('/index')
