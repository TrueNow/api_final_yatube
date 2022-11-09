from posts.models import Comment, Post, Group, Follow, User
from rest_framework import serializers, relations


class PostSerializer(serializers.ModelSerializer):
    author = relations.SlugRelatedField(slug_field='username', read_only=True)
    group = relations.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        required=True, slug_field='username'
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow
