from django.urls import path
from . import views


urlpatterns = [
    path('users/account',
         views.GathpayUsersAccount.as_view(), name="register-useraccount"
         ),
    path('users/accounts/',
        views.GathpayUsersAccounts.as_view(), name="gtet-usersaccounts"
        ),
    # path('users/account/<int:pk>',
    #      views.GathpayUserAccount.as_view(), name="get-useraccount"
    #      ),
    # path('users/account/active/change-password',
    #      views.GathpayUserAccountPassword.as_view(), name="change-password"
    #      )
]
