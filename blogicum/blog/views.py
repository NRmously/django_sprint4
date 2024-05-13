from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)

from .utils import (
    IsAuthorMixin,
    SuccessURLMixin,
    CommentMixinView,
    all_posts_query,
    published_posts_query,
    check_publication_valid,
)
from .models import Post, User, Category, Comment
from .forms import UserEditForm, PostEditForm, CommentEditForm


class IndexView(ListView):
    """Главная страница со списком постов."""

    model = Post
    template_name = 'blog/index.html'
    queryset = published_posts_query()
    paginate_by = settings.LIMIT_OF_POSTS


class CategoryPostsView(IndexView):
    """Страница со списком постов выбранной категории."""

    template_name = 'blog/category.html'
    category = None

    def get_queryset(self):
        slug = self.kwargs['category_slug']
        self.category = get_object_or_404(
            Category, slug=slug, is_published=True
        )
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class UserPostsView(IndexView):
    """Страница со списком постов пользователя."""

    template_name = 'blog/profile.html'
    author = None

    def get_queryset(self):
        username = self.kwargs['username']
        self.author = get_object_or_404(User, username=username)
        if self.author == self.request.user:
            return all_posts_query().filter(author=self.author)
        return super().get_queryset().filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class PostDetailView(DetailView):
    """Страница поста."""

    model = Post
    template_name = 'blog/detail.html'
    post_data = None

    def get_queryset(self):
        self.post_data = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.post_data.author == self.request.user:
            return all_posts_query().filter(pk=self.kwargs['pk'])
        return published_posts_query().filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.is_valid_post_data():
            context['form'] = CommentEditForm()
        context['comments'] = self.object.comments.all().select_related(
            'author'
        )
        return context

    def is_valid_post_data(self):
        return all(
            (
                self.post_data.is_published,
                self.post_data.pub_date <= now(),
                self.post_data.category.is_published,
            )
        )


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя."""

    model = User
    form_class = UserEditForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        username = self.request.user
        return reverse('blog:profile', kwargs={'username': username})


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание поста."""

    model = Post
    form_class = PostEditForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user
        return reverse('blog:profile', kwargs={'username': username})


class PostUpdateView(
    LoginRequiredMixin,
    IsAuthorMixin,
    SuccessURLMixin,
    UpdateView,
):
    """Редактирование поста."""

    model = Post
    form_class = PostEditForm
    template_name = 'blog/create.html'


class PostDeleteView(LoginRequiredMixin, IsAuthorMixin, DeleteView):
    """Удаление поста."""

    model = Post
    template_name = 'blog/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostEditForm(instance=self.object)
        return context

    def get_success_url(self):
        username = self.request.user
        return reverse_lazy('blog:profile', kwargs={'username': username})


class CommentCreateView(LoginRequiredMixin, SuccessURLMixin, CreateView):
    """Создание комментария."""

    model = Comment
    form_class = CommentEditForm
    template_name = 'blog/comment.html'
    post_data = None

    def dispatch(self, request, *args, **kwargs):
        self.post_data = check_publication_valid(self.kwargs)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_data
        if self.post_data.author != self.request.user:
            self.send_author_email()
        return super().form_valid(form)

    def send_author_email(self):
        post_url = self.request.build_absolute_uri(self.get_success_url())
        recipient_email = self.post_data.author.email
        subject = 'New comment'
        message = (
            f'Пользователь {self.request.user} добавил '
            f'комментарий к посту {self.post_data.title}.\n'
            f'Читать комментарий {post_url}'
        )
        send_mail(
            subject=subject,
            message=message,
            from_email='from@example.com',
            recipient_list=[recipient_email],
            fail_silently=True,
        )


class CommentUpdateView(CommentMixinView, UpdateView):
    """Редактирование комментария."""

    form_class = CommentEditForm


class CommentDeleteView(CommentMixinView, DeleteView):
    """Удаление комментария."""

    pass
