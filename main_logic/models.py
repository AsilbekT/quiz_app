import random
from django.db import models
from accounts.models import Account
# Create your models here.


class Team(models.Model):
    team_name = models.CharField(max_length=100, unique=True)
    team_leader = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name='team_leader')

    members = models.ManyToManyField(
        Account, blank=True, related_name='members')
    team_avatar = models.ImageField(
        upload_to="static/teams_avatar/", default='teams.jpg')

    def __str__(self) -> str:
        return self.team_name


class Category(models.Model):
    type = models.CharField(max_length=100)
    file = models.FileField(default="asd.txt", blank=True, null=True)


class Question(models.Model):
    question = models.TextField()
    question_type = models.ForeignKey(Category, on_delete=models.CASCADE)

    answer = models.CharField(max_length=200, blank=True, null=True)

    option1 = models.BooleanField(default=False)
    option2 = models.BooleanField(default=False)
    option3 = models.BooleanField(default=False)
    option4 = models.BooleanField(default=False)


class Tournament(models.Model):
    tournament_code = models.CharField(
        max_length=10, unique=True, blank=True, null=True)
    tournament_teams = models.ManyToManyField(
        Team, blank=True, related_name='tournament_teams')
    tournament_price = models.CharField(max_length=100)
    categories = models.ManyToManyField(
        Category, related_name="categories")
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.tournament_code

    def save(self, *args, **kwargs):
        if not self.tournament_code:
            while True:
                unique_number = str(random.randint(10000000, 999999999))
                try:
                    Tournament.objects.get(tournament_code=unique_number)
                except Tournament.DoesNotExist:
                    self.tournament_code = unique_number
                    break
        super().save(*args, **kwargs)
