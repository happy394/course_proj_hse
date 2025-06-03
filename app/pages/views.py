from django.shortcuts import render, get_object_or_404
from .models import Team_east, Team_west, Player, PlayerNews, Player, Team, TeamPlayer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import json
from django.http import JsonResponse

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

    total = player.pos + player.neg + player.neu
    if total == 0:
        mood_score = 0.5
    else:
        mood_score = (player.pos + player.neu) / total

    if mood_score > 0.6:
        mood_class = "mood-positive"
    elif mood_score < 0.4:
        mood_class = "mood-negative"
    else:
        mood_class = "mood-neutral"

    context = {
        'player': player,
        'mood_class': mood_class,
        'mood_score': round(mood_score * 100, 1),
    }

    return render(request, 'pages/player_detail.html', {'player': player, 'news': player_news, 'context': context})

@login_required
def team_constructor(request):
    players = Player.objects.all().values(
        'id', 'name', 'position', 'team', 'age', 'rank', 'image_url'
    )
    players_json = json.dumps(list(players))
    
    return render(request, 'pages/team_constructor.html', {
        'players_json': players_json
    })

@csrf_exempt
@login_required
def save_team(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            team_name = data.get('name')
            players = data.get('players')
            
            team = Team.objects.create(
                user=request.user,
                name=team_name,
                lineup=players,
            )
            
            return JsonResponse({'success': True, 'team_id': team.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

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