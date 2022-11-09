from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='posts')
router.register(r'groups', views.GroupViewSet, basename='groups')
router.register(
    r'posts/(?P<post_id>[1-9]\d*)/comments',
    views.CommentViewSet, basename='post_comments')
router.register(r'follow', views.FollowViewSet, basename='follow')


urlpatterns = [
    # path('api-token-auth/', auth_views.obtain_auth_token),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
