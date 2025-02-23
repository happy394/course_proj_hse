from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_menu, name="main_menu"),
    path("window-one/", views.teams, name="teams"),
    path('players/', views.players, name='players'),
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
    path("window-three/", views.window_three, name="window_three"),
    path("window-four/", views.window_four, name="window_four"),
]
