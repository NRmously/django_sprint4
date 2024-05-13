from django.utils import timezone
from django import forms

from .models import User, Post, Comment


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PostEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial['pub_date'] = timezone.now(
            ).strftime("%Y-%m-%dT%H:%M")

    class Meta:
        model = Post
        exclude = ('author', )
        widgets = {
            'text': forms.Textarea({'rows': '5'}),
            'pub_date': forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={'type': 'datetime-local'},
            ),
        }


class CommentEditForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea({'rows': '3'})
        }
