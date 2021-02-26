from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Article
from userprofile.models import UserMain
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm


@login_required
def add_article_view(request):
    user_profile = UserMain.objects.get(user=request.user)

    if request.POST:
        form = ArticleForm(request.POST, request.FILES, initial={'user': request.user.id})

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('save_article_success'))

    form = ArticleForm(request.POST or None, initial={'user': request.user.id, 'status': 'review'})

    data = {
        'title': 'Добавить новую статью',
        'user_profile': user_profile,
        'form': form,
    }

    return render(request, 'profile/article_add.html', data)


@login_required
def edit_article_view(request, slug):
    user_profile = UserMain.objects.get(user=request.user)
    article = get_object_or_404(Article, pk=slug)

    if request.POST:
        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('save_article_success'))

    form = ArticleForm(request.POST or None, instance=article, initial={'article_id': article.id})

    data = {
        'title': 'Редактирование статьи',
        'user_profile': user_profile,
        'form': form,
    }

    return render(request, 'profile/article_edit.html', data)


@login_required
def remove_article_view(request, slug):
    user_profile = UserMain.objects.get(user=request.user)

    data = {
        'title': 'Удаление статьи',
        'user_profile': user_profile,
        'slug': slug,
    }

    return render(request, 'profile/article_remove.html', data)


@login_required
def save_article_success(request):
    user_profile = UserMain.objects.get(user=request.user)
    return render(request, 'profile/article_success.html', {'user_profile': user_profile, 'title': 'Сообщение'})


@login_required
def article_remove_success(request, slug):
    article = Article.objects.get(id=slug)

    if request.user.id == article.user:
        article.delete()

    return HttpResponseRedirect(reverse('user_profile_articles'))
