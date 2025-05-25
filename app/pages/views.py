from django.shortcuts import render, get_object_or_404
from .models import Team_east, Team_west, Player
import plotly.graph_objects as go

def main_menu(request):
    return render(request, "pages/main_menu.html")

def teams(request):
    teams_west = Team_east.objects.all()
    teams_east = Team_west.objects.all()
    return render(request, "pages/teams.html", {'teams_east': teams_east, 'teams_west': teams_west})

def players(request):
    query = request.GET.get('q', '')
    if query:
        player_list = Player.objects.filter(name__icontains=query).order_by('rank')
    else:
        player_list = Player.objects.all().order_by('rank')

    return render(request, 'pages/players.html', {'players': player_list, 'query': query})

def player_detail(request, image_url):
    player = get_object_or_404(Player, image_url=image_url)

    return render(request, 'pages/player_detail.html', {'player': player})

def window_three(request):
    return render(request, "pages/window_three.html")

def window_four(request):
    return render(request, "pages/window_four.html")
