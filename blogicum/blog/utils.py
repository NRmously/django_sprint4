from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Comment, Post


class IsAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class SuccessURLMixin:
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('blog:post_detail', kwargs={'pk': pk})


class CommentMixinView(LoginRequiredMixin, SuccessURLMixin, View):
    """Mixin для редактирования и удаления комментария."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        check_publication_valid(self.kwargs)
        return super().dispatch(request, *args, **kwargs)


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
