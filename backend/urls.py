# urls.py
from django.urls import path
from .views import (
    add_file,
    landing_page,
    login,
    signUp,
    userDashboard,
    logout,
    email_form_view,
    download_multiple_files,
    admin_dashboard,
    edit_file,
    delete_file,
    activate,
    download_file,  # Import the new view
)
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path("add-file/", add_file, name="add_file"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("edit-file/<int:document_id>/", edit_file, name="edit_file"),
    path("delete-file/<int:document_id>/", delete_file, name="delete_file"),
    path("download-multiple/", download_multiple_files, name="download_multiple"),
    path("email/<int:document_id>/", email_form_view, name="email_form"),
    path("", landing_page, name="landing_page"),
    path("login/", login, name="login"),
    path("signup/", signUp, name="signUp"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path(
        "confirmation-sent/",
        TemplateView.as_view(template_name="confirmation_sent.html"),
        name="confirmation_sent",
    ),
    path(
        "activation-complete/",
        TemplateView.as_view(template_name="activation_complete.html"),
        name="activation_complete",
    ),
    path(
        "activation-invalid/",
        TemplateView.as_view(template_name="activation_invalid.html"),
        name="activation_invalid",
    ),
    path(
        "reset-password/",
        auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
        name="reset_password",
    ),
    path(
        "reset-password-sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    path("logout/", logout, name="logout"),
    path("user-dashboard/", userDashboard, name="userDashboard"),
    path(
        "download-file/<int:document_id>/", download_file, name="download_file"
    ),  # New URL pattern
]
