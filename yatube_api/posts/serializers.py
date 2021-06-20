from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('author', 'pub_date', 'id', 'text')
        read_only_fields = ('pub_date',)
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    post = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'post', 'author', 'text', 'created')
        model = Comment
