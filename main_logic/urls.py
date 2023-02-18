from django.urls import path
from . import views

urlpatterns = [
    path("teams/", views.get_teams, name="get_teams"),
    path("teams/add/", views.add_team, name="add_team"),
    path("teams/<int:id>/",
         views.get_or_update_team, name="get_or_update_team"),

    path("categories/", views.get_categories,
         name="get_categories"),

    path("categories/<int:id>/questions/",
         views.get_questions, name="get_questions"),

    path("tournaments/", views.get_tournaments,
         name="get_tournaments"),
    path("tournaments/<int:id>/", views.get_tournament,
         name="get_tournament"),
]
