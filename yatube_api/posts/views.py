from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from .permissions import IsAuthorOrReadOnly

from rest_framework.response import Response
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

    def partial_update(self, request, pk, partial=True):

        post = self.get_queryset().get(pk=pk)
        serializer = self.get_serializer(post, data=request.data, partial=True)
        if serializer.is_valid() and post.author == self.request.user:
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk):

        post = self.get_queryset().get(pk=pk)
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(post)
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def partial_update(self, request, id, pk, partial=True):

        comment = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(
            comment, data=request.data, partial=True)
        if serializer.is_valid() and comment.author == self.request.user:
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, id, pk):

        comment = get_object_or_404(self.get_queryset(), pk=pk)
        if comment.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)
