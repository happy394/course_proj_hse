from django.db import models

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
    position = models.CharField(max_length=2, default='')
    team = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.name}"