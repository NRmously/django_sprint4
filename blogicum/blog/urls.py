from django.urls import path

from .views import (
    IndexView,
    CategoryPostsView,
    UserPostsView,
    PostDetailView,
    ProfileUpdateView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(),
         name='index'),
    path('category/<slug:category_slug>/', CategoryPostsView.as_view(),
         name='category_posts'),
    path('profile/<str:username>/', UserPostsView.as_view(),
         name='profile'),
    path('posts/<int:pk>/', PostDetailView.as_view(),
         name='post_detail'),
    path('edit_profile/', ProfileUpdateView.as_view(),
         name='edit_profile'),
    path('posts/create/', PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:pk>/comment/', CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:pk>/edit_comment/<int:comment_pk>/',
         CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:pk>/delete_comment/<int:comment_pk>/',
         CommentDeleteView.as_view(), name='delete_comment'),
]
