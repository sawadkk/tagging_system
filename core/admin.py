from django.contrib import admin

from .models import Post, PostImage, Tag, Tag_Weight

class PostImageAdmin(admin.StackedInline):
    model = PostImage

admin.site.register(Post)
admin.site.register(PostImage)

admin.site.register(Tag)
admin.site.register(Tag_Weight)