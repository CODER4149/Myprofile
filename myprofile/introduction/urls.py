from django.urls import path

from . import views
from .views import description

urlpatterns = [
    path("", views.index, name="index"),
    path("skills/", views.skills, name="index"),
    path("experience/", views.experience, name="index"),
    path("contact/", views.contact, name="contact"),
    path("description/", views.description, name="description"),
    path("download/<int:resume_id>/",
         views.download_resume, name="download_resume")



]
