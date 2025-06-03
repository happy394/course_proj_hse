from django.db import models
from django.contrib.auth.models import User

class BaseTeam(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True

class Team_east(BaseTeam):

    def __str__(self):
        return self.name

class Team_west(BaseTeam):

    def __str__(self):
        return self.name

class Player(models.Model):
    rank = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=0)
    position = models.CharField(max_length=2, default='')
    team = models.CharField(max_length=100, default='')
    g = models.IntegerField(default=0, null=True)
    gs = models.IntegerField(default=0, null=True)
    mp = models.IntegerField(default=0, null=True)
    per = models.FloatField(default=0.0, null=True)
    ts = models.FloatField(default=0.0, null=True)
    par = models.FloatField(default=0.0, null=True)
    ftr = models.FloatField(default=0.0, null=True)
    orb = models.FloatField(default=0.0, null=True)
    drb = models.FloatField(default=0.0, null=True)
    trb = models.FloatField(default=0.0, null=True)
    ast = models.FloatField(default=0.0, null=True)
    stl = models.FloatField(default=0.0, null=True)
    blk = models.FloatField(default=0.0, null=True)
    tov = models.FloatField(default=0.0, null=True)
    usg = models.FloatField(default=0.0, null=True)
    ows = models.FloatField(default=0.0, null=True)
    dws = models.FloatField(default=0.0, null=True)
    ws = models.FloatField(default=0.0, null=True)
    ws48 = models.FloatField(default=0.0, null=True)
    obpm = models.FloatField(default=0.0, null=True)
    dbpm = models.FloatField(default=0.0, null=True)
    bpm = models.FloatField(default=0.0, null=True)
    vorp = models.FloatField(default=0.0, null=True)
    awards = models.CharField(max_length=100, default='-', null=True)
    pos = models.IntegerField(default=0, null=True)
    neu = models.IntegerField(default=0, null=True)
    neg = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"{self.name}"


class PlayerNews(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    text = models.TextField()
    source = models.CharField(max_length=500)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['-timestamp']  # Show latest news first

    def __str__(self):
        return f"News for {self.player.name} - {self.timestamp.strftime('%Y-%m-%d')}"

class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lineup = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"

class TeamPlayer(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    position = models.CharField(max_length=50, blank=True, null=True)
