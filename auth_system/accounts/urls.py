from django.urls import path

from . import views

urlpatterns = [
    path(
        "users/account",
        views.GathpayUsersAccount.as_view(),
        name="register-useraccount",
    ),
    path(
        "users/accounts/",
        views.GathpayUsersAccounts.as_view(),
        name="get-usersaccounts",
    ),
    path(
        "users/<int:pk>/account/",
        views.GathpayUserAccount.as_view(),
        name="get_update_delete_useraccount",
    ),
    path(
        "users/account/forgot_password",
        views.GathpayUserForgotPassword.as_view(),
        name="forgot_password",
    ),
    path(
        "users/account/reset_password",
        views.GathpayUserResetPassword.as_view(),
        name="reset_password",
    ),
    path(
        "users/account/active/change_password",
        views.GathpayUserChangePassword.as_view(),
        name="change-password",
    ),
    path(
        "users/account/verify",
        views.GathpayUserAccountVerify.as_view(),
        name="activate-account",
    ),
    path(
        "users/account/verify/resend_otp",
        views.GathpayUserResendAccountOTP.as_view(),
        name="resend-otp",
    ),
    path(
        "user/account/logout", views.GathpayUserAccountLogOut.as_view(), name="logout"
    ),
]
