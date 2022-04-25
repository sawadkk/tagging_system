from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from core.api.views import PostViewSet, LikeViewSet, DislikeViewSet, LikeList

router = DefaultRouter()

router.register(r'posts', PostViewSet, basename='post')
router.register(r'like', LikeViewSet, basename='like')
router.register(r'dislike', DislikeViewSet, basename='dislike')
router.register(r'likelist', LikeList, basename='likelist')

urlpatterns = [


		path("",include(router.urls)),
		

		path('schema', get_schema_view(
        title="Tagging_System",
        description="API for Tagging_System …",
        version="1.0.0"
    ), name='openapi-schema'),

		 path('docs/', include_docs_urls(title='Tagging_System')),




]