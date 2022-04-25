from django.shortcuts import get_object_or_404
from django.db.models import Case, When, Value, IntegerField
from django.db.models import Count
from django.db.models import OuterRef, Subquery
from django.db import models

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.api.serializers import PostSerializer,LikeSerializer
from core.models import Post, Tag_Weight, Tag

class PostViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    
    def list(self, request):

        tag_weight = Tag_Weight.objects.filter(user=request.user,tag_id=OuterRef('tag')).values('weight').order_by('-weight')

        weight = Subquery(tag_weight)
        queryset = Post.objects.all().annotate(weight=weight).order_by('-weight','id')

        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class LikeViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response({"Error:'not slected a post for like'"})

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        
        if post.dislikes.filter(username=request.user.username).count() == 1:
            post.dislikes.remove(request.user)
            post.likes.add(request.user)
            
            tags = post.tag.all()
            if tags.exists():
                for tag in tags:
                    try:
                        tag_get = Tag_Weight.objects.get(user=request.user,tag=tag)
                        tag_get.weight += 2
                        tag_get.save()
                    except:
                        tag_get = Tag_Weight.objects.create(user=request.user,tag=tag)
                        tag_get.weight += 2
                        tag_get.save()

        
        elif post.likes.filter(username=request.user.username).count() == 0:
           post.likes.add(request.user)
           
           tags = post.tag.all()
           if tags.exists():
                for tag in tags:
                    try:
                        tag_get = Tag_Weight.objects.get(user=request.user,tag=tag)
                        tag_get.weight += 1
                        tag_get.save()
                    except:
                        tag_get = Tag_Weight.objects.create(user=request.user,tag=tag)
                        tag_get.weight += 1
                        tag_get.save()

        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

class DislikeViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response({"Error:'not slected a post for dislike'"})

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        
        if post.likes.filter(username=request.user.username).count() == 1:
            post.likes.remove(request.user)
            post.dislikes.add(request.user)
            tags = post.tag.all()
            if tags.exists():
                for tag in tags:
                    try:
                        tag_get = Tag_Weight.objects.get(user=request.user,tag=tag)
                        tag_get.weight -= 2
                        tag_get.save()
                    except:
                        tag_get = Tag_Weight.objects.create(user=request.user,tag=tag)
                        tag_get.weight -= 2
                        tag_get.save()
        
        elif post.dislikes.filter(username=request.user.username).count() == 0:
           post.dislikes.add(request.user)
           tags = post.tag.all()
           if tags.exists():
                for tag in tags:
                    try:
                        tag_get = Tag_Weight.objects.get(user=request.user,tag=tag)
                        tag_get.weight -= 1
                        tag_get.save()
                    except:
                        tag_get = Tag_Weight.objects.create(user=request.user,tag=tag)
                        tag_get.weight -= 1
                        tag_get.save()

        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

class LikeList(viewsets.ViewSet):
   
   permission_classes = [IsAuthenticated]

   def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        likes = post.likes.all()
        like_dict = likes.values('id', 'username')
        serializer = LikeSerializer(like_dict, many=True)
        return Response(serializer.data) 