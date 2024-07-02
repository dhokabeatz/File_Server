from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django import forms
from django.contrib.auth import forms
from django.contrib import messages
from .forms import (
    DocumentForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    EmailForm,
)
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from .models import Document
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from io import BytesIO
import os
import zipfile


@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect(
            "userDashboard"
        )  # Redirect non-admins to user dashboard or handle as needed

    documents = Document.objects.all()  # Retrieve all documents
    return render(request, "adminDashboard.html", {"documents": documents})


@login_required(login_url='login')
def add_file(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            return redirect("admin_dashboard")
    else:
        form = DocumentForm()
    return render(request, "add_file.html", {"form": form})




def delete_file(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if request.method == "POST":
        document.delete()
        return redirect("admin_dashboard") 
    return render(request, "delete_file.html", {"document": document})


def edit_file(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    if request.method == "POST":
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect(
                "admin_dashboard"
            )
    else:
        form = DocumentForm(instance=document)

    return render(request, "edit_file.html", {"form": form, "document": document})


def email_form_view(request, document_id):
    document = Document.objects.get(pk=document_id)
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data["recipient"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            file_url = request.build_absolute_uri(document.file.url)

            email_message = f"{message}\n\nYou can download the file here: {file_url}"

            send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [recipient])

            return redirect("userDashboard")
    else:
        form = EmailForm()
    return render(request, "email_form.html", {"form": form, "document": document})


@csrf_exempt
def download_multiple_files(request):
    if request.method == "POST":
        file_ids = request.POST.get("file_ids")
        file_ids = json.loads(file_ids)

        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w") as zip_file:
            for file_id in file_ids:
                document = get_object_or_404(Document, pk=file_id)
                file_path = document.file.path
                zip_file.write(file_path, os.path.basename(file_path))

        buffer.seek(0)

        response = HttpResponse(buffer, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=files.zip"
        return response

    return HttpResponse(status=405)


def logout(request):
    auth.logout(request)

    return redirect("landing_page")


def login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("userDashboard")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = CustomAuthenticationForm()

    context = {"form": form}

    return render(request, "login_page.html", context)


def signUp(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "signUp_page.html", context)


@login_required(login_url="login")
def userDashboard(request):
    query = request.GET.get("q")
    if query:
        documents = Document.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        documents = Document.objects.all()
    print(documents)
    return render(request, "userdashboard_page.html", {"documents": documents})


def landing_page(request):
    return render(request, "landing_page.html")
