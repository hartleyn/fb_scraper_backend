from django.contrib import admin
from .models import FootballClub, Competition, CompetitionResult

# Register your models here.
admin.site.register(FootballClub)
admin.site.register(Competition)
admin.site.register(CompetitionResult)
