from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from .permissions import IsAuthorOrReadOnly

from .models import Post
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    ]

    def perform_create(self, serializer):

        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):

        post = get_object_or_404(Post, id=self.kwargs['id'])
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):

        post = get_object_or_404(Post, id=self.kwargs['id'])
        serializer.save(post=post, author=self.request.user)
# Теперь понял) Спасибо!
