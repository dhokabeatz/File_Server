from django.urls import path
from .views import landing_page,login,signUp, userDashboard,logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    #Authentication patterns
    path("",landing_page, name="landing_page"),
    path("login/",login,name="login"),
    path("signup/",signUp,name="signUp"),
    path("reset-password", auth_views.PasswordResetView.as_view(template_name = "reset_password.html"), name ='reset_password'),
    path("reset-password-sent", auth_views.PasswordResetDoneView.as_view(template_name= "password_reset_sent.html"), name ='password_reset_done'),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name= "password_reset_form.html"), name ='password_reset_confirm'),
    path("reset_password_complete", auth_views.PasswordResetCompleteView.as_view(template_name= "password_reset_done.html"), name ='password_reset_complete'),
    path("logout",logout,name="logout"),


    path("user-dashboard/",userDashboard,name="userDashboard"),
    # path("user-open",userOpen,name="userOpen"),
    # path("user-download",download,name="download"),
    # path("user-email",email,name="email"),

    # path("admin-dashboard",userDashboard,name="userDashboard"),
    # path("admin-open",userOpen,name="userOpen"),
    # path("admin-edit",download,name="download"),
    # path("admin-delete",email,name="email"),
    # path("admin-dowload",logout,name="logout"),
    # path("admin-email",userDashboard,name="userDashboard"),

]