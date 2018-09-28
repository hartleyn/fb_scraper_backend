from django.urls import path
from . import views


urlpatterns = [
	path('clubs/', views.FootballClubList.as_view()),
	path('clubs/<int:pk>/', views.FootballClubDetail.as_view()),
	path('competitions/', views.CompetitionList.as_view()),
	path('competitions/<int:pk>/', views.CompetitionDetail.as_view()),
	path('competitions/<int:pk>/add-club/', views.AddCompetitionFootballClub.as_view()),
	path('competition-results/', views.CompetitionResultList.as_view()),
	path('competition-results/<str:competition_name>/<str:football_club_name>/seasons/', views.RetrieveFootballClubCompetitionSeasons.as_view()),
	path('competition-results/<str:competition_name>/<str:football_club_name>/historical-table/', views.RetrieveFootballClubCompetitionHistoricalTable.as_view()),
	path('competition-results/<str:season>/mock-super-league/', views.RetrieveFootballClubCompetitionMockSuperLeagueTable.as_view()),
	path('users/', views.UserList.as_view()),
]
