from django.db import models

# Create your models here.

class FootballClub(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.name


class Competition(models.Model):
	name = models.CharField(max_length=50, unique=True)
	football_clubs = models.ManyToManyField(FootballClub)

	def __str__(self):
		return self.name


class CompetitionResult(models.Model):
	football_club = models.ForeignKey(
		FootballClub,
		to_field='name',
		on_delete=models.CASCADE,
	)
	competition = models.ForeignKey(
		Competition,
		to_field='name',
		on_delete=models.CASCADE,
	)
	season = models.CharField(max_length=7)
	league_position = models.PositiveSmallIntegerField()
	played = models.PositiveSmallIntegerField()
	won = models.PositiveSmallIntegerField()
	drawn = models.PositiveSmallIntegerField()
	lost = models.PositiveSmallIntegerField()
	goals_for = models.PositiveSmallIntegerField()
	goals_against = models.PositiveSmallIntegerField()
	goal_difference = models.SmallIntegerField()
	points = models.PositiveSmallIntegerField()

	def __str__(self):
		return f'{self.football_club}_{self.competition}_{self.season}'
