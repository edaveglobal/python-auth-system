from django.urls import path
from . import views


urlpatterns = [
    path(
        'users/account',
        views.GathpayUsersAccount.as_view(),
        name="register-useraccount"),
    path(
        'users/accounts/',
        views.GathpayUsersAccounts.as_view(),
        name="get-usersaccounts"),
    path(
        'users/account/<int:pk>/',
        views.GathpayUserAccount.as_view(),
        name="useraccount"),
    path(
        'users/account/forgot_password', 
        views.GathpayUserForgotPassword.as_view(),
        name='forgot_password'
    ),
    path(
        'users/account/reset_password', 
        views.GathpayUserResetPassword.as_view(), 
        name="reset_password"),
    path(
        'users/account/active/change_password',
        views.GathpayUserChangePassword.as_view(),
        name="change-password")
]
    
