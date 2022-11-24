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
        'update_profile/<int:pk>/', views.UpdateProfileView.as_view(),
        name='update'
    ),
    # path('users/account/verify_email', views.GathpayUserAccountVerify.as_view(), name="verify"),
    path(
        'users/account/active/change-password',
        views.GathpayUserAccountChangePassword.as_view(),
        name="change-password")
]
    
