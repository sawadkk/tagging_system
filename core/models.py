from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class PostImage(models.Model):
    images = models.FileField(upload_to = 'images/')

class Post(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ManyToManyField(PostImage, related_name='posts', blank=True)
    tag = models.ManyToManyField(Tag, related_name='tags', blank=True, default='')
    likes = models.ManyToManyField(User, related_name='Likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='Dislikes', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        tags = self.tag.all()
        if tags.exists():
            for i in self.tag.all():
                tag = i.name
        else:
            tag = ""
        return self.title +" likes-"+ str(self.likes.count()) +" dislikes-"+ str(self.dislikes.count()) +" tag_name: "+ str(tag)

class Tag_Weight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username +"-"+ str(self.tag.name) +"-"+ str(self.weight)