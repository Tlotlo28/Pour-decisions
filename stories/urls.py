from django.urls import path
from . import views

app_name = "stories"

urlpatterns = [
    path("", views.feed, name="feed"),
    path("spin/", views.spin, name="spin"),
    path("submit/", views.submit_story, name="submit"),
    path("submitted/", views.submitted, name="submitted"),
    path("story/<int:pk>/", views.story_detail, name="detail"),
    path("story/<int:pk>/rate/", views.rate_story, name="rate"),
]