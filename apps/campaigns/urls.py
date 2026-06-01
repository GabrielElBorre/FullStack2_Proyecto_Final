from django.urls import path

from . import views

app_name = "campaigns"

urlpatterns = [
    path("", views.CampaignListView.as_view(), name="list"),
    path("campana/<int:pk>/", views.CampaignDetailView.as_view(), name="detail"),
    path("campana/nueva/", views.CampaignCreateView.as_view(), name="create"),
    path("campana/<int:pk>/editar/", views.CampaignUpdateView.as_view(), name="update"),
    path("campana/<int:pk>/eliminar/", views.CampaignDeleteView.as_view(), name="delete"),
]
