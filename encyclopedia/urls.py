from django.urls import path

from . import views




urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.query, name="query"),
    path("new_entry", views.new_article, name="new_form"),
    path("edit/<str:title>", views.update_article, name="edit"),
    path("random", views.random_article, name="random")
]
