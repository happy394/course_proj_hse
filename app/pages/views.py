from django.shortcuts import render, get_object_or_404
from .models import Team_east, Team_west, Player, PlayerNews, Player, Team, TeamPlayer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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
    player_news = PlayerNews.objects.filter(player=player)[:5]

    return render(request, 'pages/player_detail.html', {'player': player, 'news': player_news})

def window_three(request):
    return render(request, "pages/window_three.html")

def window_four(request):
    return render(request, "pages/window_four.html")

@login_required
def team_constructor(request):
    players = Player.objects.all()
    return render(request, 'pages/team_constructor.html', {'players': players})

@login_required
def save_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        player_ids = request.POST.getlist('player_ids[]')
        team = Team.objects.create(user=request.user, name=team_name)
        for pid in player_ids:
            TeamPlayer.objects.create(team=team, player_id=pid)
        return redirect('my_teams')

@login_required
def my_teams(request):
    teams = Team.objects.filter(user=request.user)
    return render(request, 'pages/my_teams.html', {'teams': teams})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('team_constructor')
    else:
        form = UserCreationForm()
    return render(request, 'pages/signup.html', {'form': form})