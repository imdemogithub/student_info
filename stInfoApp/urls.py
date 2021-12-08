from django.urls import path
from .views import *

urlpatterns = [
    path("", index),
    path("register/", register, name="register"),
    path("register_page/", register_page, name="register_page"),

    path("login_page/", login_page, name="login_page"),
    path("login/", login, name="login"),

    path("otp_page/", otp_page, name="otp_page"),
    path("recover_pwd_page/", recover_pwd_page, name="recover_pwd_page"),
    path("profile_page/", profile_page, name="profile_page"),

    path("profile_update/", profile_update, name="profile_update"),

    path("varify_otp/<str:varify_for>", varify_otp, name="varify_otp"),
    path("check/", check, name="check"),

    path("signout/", signout, name="signout"),
]