from django.urls import path

from . import views

urlpatterns = [
    path(
        "customer/wallet",
        views.GathpayCustomerWallet.as_view(),
        name="customer-wallet",
    )
]
