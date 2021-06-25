from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    # Не убирал IsAuthorOrReadOnly, т.к. там была пометка можно лучше,
    #  чтобы удостовериться, что правильно сделал.

    def has_object_permission(self, request, view, obj):

        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
