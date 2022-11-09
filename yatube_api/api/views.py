from django.shortcuts import get_object_or_404
from posts.models import Post, Group, Follow, User
from rest_framework import (
    viewsets, permissions, mixins, exceptions, pagination, filters
)

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer: serializer_class):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post

    def get_queryset(self):
        post = self.get_post()
        return post.comments

    def perform_create(self, serializer: serializer_class):
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        following_username = self.request.query_params.get('search')
        if following_username:
            return user.follower.filter(following__username=following_username)
        return user.follower

    def perform_create(self, serializer: serializer_class):
        following_username = self.request.data.get('following')
        following_user = get_object_or_404(User, username=following_username)
        follow = Follow.objects.filter(
            user=self.request.user, following=following_user
        )
        if follow.exists() or self.request.user == following_user:
            raise exceptions.ValidationError()
        serializer.save(user=self.request.user)
