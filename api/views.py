from .models import Competition
from .serializers import CompetitionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class CompetitionList(APIView):
	"""
	List all competitions, or create a new competiton.
	"""
	def get(self, request, format=None):
		competitions = Competition.objects.all()
		serializer = CompetitionSerializer(competitions, many=True)
		return Response(serializer.data)
	
	
	def post(self, request, format=None):
		serializer = CompetitionSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompetitionDetail(APIView):
	"""
	Retrieve, update, or delete a competition instance.
	"""
	def get_object(self, pk):
		try:
			return Competition.objects.get(pk=pk)
		except Competition.DoesNotExist:
			raise Http404


	def get(self, request, pk, format=None):
		competition = self.get_object(pk)
		serializer = CompetitionSerializer(competition)
		return Response(serializer.data)


	def put(self, request, pk, format=None):
		competition = self.get_object(pk)
		serializer = CompetitionSerializer(competition)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		competition = self.get_object(pk)
		competition.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
