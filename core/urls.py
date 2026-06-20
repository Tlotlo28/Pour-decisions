from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("house-rules/", views.terms, name="terms"),
    path("hall-of-shame/", views.hall_of_shame, name="hall_of_shame"),
]