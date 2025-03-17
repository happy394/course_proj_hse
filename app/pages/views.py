from django.shortcuts import render, get_object_or_404
from .models import Team_east, Team_west, Player
import plotly.express as px
import plotly.io as pio
import json

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

    stats = {
        "Games": player.g,
        "Minutes": player.mp,
        "PER": player.per,
        "Assists": player.ast,
        "Rebounds": player.trb,
        "Steals": player.stl,
        "Blocks": player.blk
    }

    fig = px.bar(
        x=list(stats.keys()), 
        y=list(stats.values()), 
        labels={'x': 'Stat Type', 'y': 'Value'},
        title=f"{player.name} Stats",
        color_discrete_sequence=["#1f77b4"]
    )

    chart_json = json.dumps(pio.to_json(fig))

    return render(request, 'pages/player_detail.html', {'player': player, 'chart_image': chart_json})

def window_three(request):
    return render(request, "pages/window_three.html")

def window_four(request):
    return render(request, "pages/window_four.html")
