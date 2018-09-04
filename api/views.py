from .models import FootballClub, Competition, CompetitionResult
from .serializers import FootballClubSerializer, CompetitionSerializer, UserSerializer, CompetitionResultSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from operator import itemgetter


# Create your views here.

class FootballClubList(generics.ListCreateAPIView):
	queryset = FootballClub.objects.all()
	serializer_class = FootballClubSerializer

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FootballClubDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = FootballClub.objects.all()
	serializer_class = FootballClubSerializer

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CompetitionList(generics.ListCreateAPIView):
	"""
	List all competitions, or create a new competiton.
	"""
	queryset = Competition.objects.all()
	serializer_class = CompetitionSerializer

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update, or delete a competition instance.
	"""
	@staticmethod
	def get_object(pk):
		try:
			return Competition.objects.get(pk=pk)
		except Competition.DoesNotExist:
			raise Http404

	queryset = Competition.objects.all()
	serializer_class = CompetitionSerializer

	def get(self, request, pk, format=None):
		clubs = FootballClub.objects.filter(competition=pk)
		names = []

		for club in clubs:
			names.append(club.name)
		names.sort()
		return Response({'id': pk, 'name': self.get_object(pk).name, 'football_clubs': names})

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	permission_classes = (permissions.IsAdminUser,)


class CompetitionResultList(APIView):

	def get(self, request, format=None):
		competition_results = CompetitionResult.objects.all()
		serializer = CompetitionResultSerializer(competition_results, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = CompetitionResultSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AddCompetitionFootballClub(APIView):

	@staticmethod
	def get_competition_object(pk):
		try:
			return Competition.objects.get(pk=pk)
		except Competition.DoesNotExist:
			raise Http404


	@staticmethod
	def get_football_club_object(pk):
		try:
			return FootballClub.objects.get(pk=pk)
		except FootballClub.DoesNotExist:
			raise Http404


	def post(self, request, pk, format=None):
		competition = self.get_competition_object(pk)
		if type(request.data) is list:
			for club in request.data:
				football_club = self.get_football_club_object(club['id'])
				competition.football_clubs.add(football_club)
		else:
			football_club = self.get_football_club_object(request.data['id'])
			competition.football_clubs.add(football_club)
		serializer = CompetitionSerializer(competition)
		return Response(serializer.data)


class RetrieveFootballClubCompetitionSeasons(APIView):

	@staticmethod
	def get_football_club_competition_seasons_list(competition_name, football_club_name):
		try:
			return CompetitionResult.objects.filter(competition=competition_name.title(), football_club=football_club_name.title()).values_list('season', flat=True)
		except CompetitionResult.DoesNotExist:
			raise Http404

	def get(self, request, competition_name, football_club_name, format=None):
		seasons = self.get_football_club_competition_seasons_list(competition_name, football_club_name)
		return Response(seasons)



class RetrieveFootballClubCompetitionHistoricalTable(APIView):

	@staticmethod
	def get_football_club_competition_seasons_table(competition_name, football_club_name):
		try:
			return CompetitionResult.objects.filter(competition=competition_name.title(), football_club=football_club_name.title(), played=38).values()
		except CompetitionResult.DoesNotExist:
			raise Http404


	@staticmethod
	def sort_by_goals_scored(table):
		final_table = []
		for x in range(0, len(table)):
			if x >= len(final_table):
				level_on_goal_difference = []
				addAmount = 1
				check = True
				while check:
					try:
						if table[x]['goal_difference'] == table[x+addAmount]['goal_difference']:
							if addAmount == 1:
								level_on_goal_difference.append(table[x])
							level_on_goal_difference.append(table[x+addAmount])
							addAmount += 1
						else:
							check = False
					except IndexError:
						check = False
					finally:
						if not check:
							if len(level_on_goal_difference) > 0:
								fixed = sorted(level_on_goal_difference, key=itemgetter('goals_for'), reverse=True)
								final_table.extend(fixed)
							else:
								final_table.append(table[x])
		return final_table

			
	def sort_by_goal_difference(self, table):
		final_table = []
		for x in range(0, len(table)):
			if x >= len(final_table):
				level_on_points = []
				addAmount = 1
				check = True
				while check:
					try:
						if table[x]['points'] == table[x+addAmount]['points']:
							if addAmount == 1:
								level_on_points.append(table[x])
							level_on_points.append(table[x+addAmount])
							addAmount += 1
						else:
							check = False
					except IndexError:
						check = False
					finally:
						if not check:
							if len(level_on_points) > 0:
								fixed = sorted(level_on_points, key=itemgetter('goal_difference'), reverse=True)
								fixed = self.sort_by_goals_scored(fixed)
								final_table.extend(fixed)
							else:
								final_table.append(table[x])
		return final_table


	def get(self, request, competition_name, football_club_name, format=None):
		table = self.get_football_club_competition_seasons_table(competition_name, football_club_name)
		sorted_table = sorted(table, key=itemgetter('points'), reverse=True)
		final_table = self.sort_by_goal_difference(sorted_table)
		return Response(final_table)
