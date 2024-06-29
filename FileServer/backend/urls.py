from django.urls import path
from .views import landing_page, login, signUp, userDashboard, logout, email_form_view, download_multiple_files, admin_dashboard,edit_file,delete_file
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('edit-file/<int:document_id>/', edit_file, name='edit_file'),
    path('delete-file/<int:document_id>/', delete_file, name='delete_file'),
    path('download-multiple/', download_multiple_files, name='download_multiple'),
    path('email/<int:document_id>/', email_form_view, name='email_form'),
    path('', landing_page, name='landing_page'),
    path('login/', login, name='login'),
    path('signup/', signUp, name='signUp'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),
    path('logout/', logout, name='logout'),
    path('user-dashboard/', userDashboard, name='userDashboard'),
]
