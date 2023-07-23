from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("skills/", views.skills, name="index"),
    path("experience/", views.experience, name="index"),
    path("contact/", views.contact, name="index")

]
