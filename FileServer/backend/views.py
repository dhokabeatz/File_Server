from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import forms  
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from .models import Document

def logout(request):
    auth.logout(request)

    return redirect('landing_page')


def login(request):

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            
            auth.login(request, user)
            return redirect('userDashboard')  # Redirect to a success page.
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthenticationForm()
    
    context = {
        'form': form
    }

    return render(request, 'login_page.html',context)

def signUp(request):

    form = CustomUserCreationForm()
    
    if request.method == 'POST':  
        form = CustomUserCreationForm(request.POST)  
  
        if form.is_valid():
            form.save()
            return redirect("login")  
    else:  
        form = CustomUserCreationForm()  
    context = {  
        'form':form  
    }  
    return render(request, 'signUp_page.html', context)  



#User views


# @login_required(login_url='login')
# def userDashboard(request):
#     documents = Document.objects.all()
#     context = {'documents': documents}
#     return render(request, 'userdashboard_page.html',context)

@login_required(login_url='login')
def userDashboard(request):
    documents = Document.objects.all()
    print(documents)
    return render(request, 'userdashboard_page.html', {'documents': documents})

# # views.py
# from django.shortcuts import render
# from .models import Document

# def dashboard(request):
#     documents = Document.objects.all()
#     return render(request, 'dashboard.html', {'documents': documents})




#Landing and authentication views
def landing_page(request):
    
    return render(request, "landing_page.html")


