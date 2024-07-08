from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django import forms
from .models import CustomUser, Document, DownloadLog, EmailLog
from .forms import (
    DocumentForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    EmailForm,
)
from django.utils.html import strip_tags

from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
import json
from io import BytesIO
import os
import zipfile
from django.contrib import messages
import mimetypes
from django.utils import timezone


@login_required
def download_file(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    DownloadLog.objects.create(user=request.user, document=document)
    document.download_count += 1
    document.save()
    file_url = document.file.url
    return redirect(file_url)


@login_required
def download_file_view(request, file_id):
    document = get_object_or_404(Document, pk=file_id)
    file_path = document.file.path
    file_name = document.file.name.split("/")[-1]

    document.download_count += 1
    document.save()

    DownloadLog.objects.create(
        user=request.user, document=document, downloaded_at=timezone.now()
    )

    with open(file_path, "rb") as f:
        response = HttpResponse(
            f.read(), content_type=mimetypes.guess_type(file_path)[0]
        )
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response


@login_required(login_url="login")
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("userDashboard")
    documents = Document.objects.all()
    download_logs = DownloadLog.objects.all()
    email_logs = EmailLog.objects.all()
    return render(
        request,
        "adminDashboard.html",
        {
            "documents": documents,
            "download_logs": download_logs,
            "email_logs": email_logs,
        },
    )


@login_required(login_url="login")
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
            return redirect("admin_dashboard")
    else:
        form = DocumentForm(instance=document)
    return render(request, "edit_file.html", {"form": form, "document": document})

@login_required
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
            EmailLog.objects.create(
                user=request.user,
                document=document,
                recipient=recipient,
                sent_at=timezone.now(),
            )
            document.email_count += 1  
            document.save()
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
                DownloadLog.objects.create(
                    document=document, downloaded_at=timezone.now(), user=request.user

                )
                document.download_count += 1
                document.save()
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
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your account."
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse("activate", args=[uid, token])
            )
            message = render_to_string(
                "activation_email.html",
                {
                    "user": user,
                    "activation_link": activation_link,
                },
            )
            text_content = strip_tags(message)
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, text_content, to=[to_email])
            email.send()
            return redirect("confirmation_sent")
    else:
        form = CustomUserCreationForm()
    return render(request, "signUp_page.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("activation_complete")
    else:
        return render(request, "activation_invalid.html")


@login_required(login_url="login")
def userDashboard(request):
    query = request.GET.get("q")
    if query:
        documents = Document.objects.filter(
            Q(title__icontains=query) | Q(description__icontains(query))
        )
    else:
        documents = Document.objects.all()
    print(documents)
    return render(request, "userdashboard_page.html", {"documents": documents})


def landing_page(request):
    return render(request, "landing_page.html")
