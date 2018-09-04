from rest_framework import serializers
from .models import FootballClub, Competition, CompetitionResult
from django.contrib.auth.models import User


class FootballClubSerializer(serializers.ModelSerializer):
	class Meta:
		model = FootballClub
		fields = ('id', 'name',)


class CompetitionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Competition
		fields = ('id', 'name', 'football_clubs',)


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name',)


class CompetitionResultSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompetitionResult
		fields = ('id', 'season', 'football_club', 'competition', 'league_position', 'played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'goal_difference', 'points',)
