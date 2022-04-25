from rest_framework import serializers

from core.models import Post, PostImage

class ImageSerializer(serializers.Serializer):
	images = serializers.ImageField()

class PostSerializer(serializers.Serializer):
	tag = serializers.StringRelatedField(many=True,read_only=True)
	id = serializers.IntegerField(read_only=True)
	title = serializers.CharField()
	description = serializers.CharField()
	created = serializers.DateTimeField()
	opinion = serializers.SerializerMethodField()
	image = ImageSerializer(many=True)

	def get_opinion(self, object):
		user =  self.context['request'].user
		if object.likes.filter(username=user.username).count() == 1:
			return "liked"
		elif object.dislikes.filter(username=user.username).count() == 1:
			return "disliked"
		else:
			return "no opinion"

class LikeSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	username = serializers.CharField()