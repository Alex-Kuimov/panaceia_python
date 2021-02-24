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
        required=False,
        label='Текст',
    )

    preview = forms.CharField(
        widget=forms.Textarea,
        min_length=3,
        max_length=500,
        required=False,
        label='Отрывок',
    )

    image = forms.ImageField(
        required=False,
        label='Изображение'
    )

    user = forms.CharField(widget=forms.HiddenInput(), required=False)
    article_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    status = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Article
        fields = ['title', 'text', 'preview', 'image', 'user', 'status']
