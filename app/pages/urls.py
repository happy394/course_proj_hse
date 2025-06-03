from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_menu, name="main_menu"),
    path("teams/", views.teams, name="teams"),
    path('players/', views.players, name='players'),
    path('player/<str:image_url>/', views.player_detail, name='player_detail'),
]
