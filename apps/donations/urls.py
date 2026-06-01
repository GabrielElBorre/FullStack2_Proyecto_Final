from django.urls import path

from . import views

app_name = "donations"

urlpatterns = [
    path(
        "campana/<int:campana_pk>/donar/",
        views.DonationCreateView.as_view(),
        name="create",
    ),
    path("mis-donaciones/", views.MyDonationsListView.as_view(), name="my_donations"),
]
