from django.urls import path
from . import views


urlpatterns = [
	path('competitions/', views.CompetitionList.as_view()),
	path('competitions/<int:id>', views.CompetitionDetail.as_view()),
]
