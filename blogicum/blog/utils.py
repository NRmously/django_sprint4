from django.db.models import Count
from django.shortcuts import get_object_or_404

from blog.models import Post
from django.utils import timezone


def all_posts_query():
    """Возвращает все посты."""
    query_set = (
        Post.objects.select_related(
            'category',
            'location',
            'author',
        )
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )
    return query_set


def published_posts_query():
    """Возвращает опубликованные посты."""
    query_set = all_posts_query().filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )
    return query_set


def check_publication_valid(post_data):
    """Проверка на валидность перед публикацией поста"""
    post = get_object_or_404(
        Post,
        pk=post_data['pk'],
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )
    return post
