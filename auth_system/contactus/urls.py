from django.urls import path

from . import views

urlpatterns = [
    path(
        "customers/contact",
        views.GathpayCustomerContactUs.as_view(),
        name="customer-contactus",
    )
]
