from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('id', 'title', 'body_header', 'blockquote', 'body_content', 'header_image_small', 'header_image_medium', 'header_image_large', 'photo_credit',)
