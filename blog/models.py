from django.core.files.storage import FileSystemStorage
from django.db import models


# Create your models here.

#fs = FileSystemStorage(location='/media/images')


class Post(models.Model):
	title = models.CharField(max_length=60, unique=True)
	body_header = models.CharField(max_length=60)
	blockquote = models.TextField(max_length=280)  # Tweet length should suffice
	body_content = models.TextField()
	header_image_small = models.ImageField(upload_to='images')
	header_image_medium = models.ImageField(upload_to='images')
	header_image_large = models.ImageField(upload_to='images')
	photo_credit = models.TextField(max_length=200)  # Might need html

	def __str__(self):
		return self.title
