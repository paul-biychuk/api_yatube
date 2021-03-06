from rest_framework.authtoken import views
from .views import CommentViewSet, PostViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(

    'posts/(?P<id>[0-9]+)/comments', CommentViewSet, basename='Comment'
)
router.register('posts', PostViewSet)


urlpatterns = [

    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]
