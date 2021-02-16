from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        min_length=3,
        max_length=100,
        required=True,
        label='Заголовок',
    )

    text = forms.CharField(
        widget=forms.Textarea,
        min_length=3,
        max_length=10000,
        required=True,
        label='Текст',
    )

    image = forms.ImageField(
        required=False,
        label='Изображение'
    )

    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Article
        fields = ['title', 'text', 'image', 'user']
