from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.get_users, name="get_users"),
    path("users/<int:id>/", views.get_user, name="get_user"),
    path("users/<int:id>/friendships/",
         views.get_friendships, name="get_friendships"),
    path("users/friendships/add/", views.add_friendship, name="add_friendship"),
]
