from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Article
from userprofile.models import UserMain
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm


def add_article_view(request):
    user_profile = UserMain.objects.get(user=request.user)

    form = ArticleForm(request.POST or None, initial={'user': request.user.id})

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('save_article_success'))

    data = {
        'user_profile': user_profile,
        'form': form,
    }

    return render(request, 'profile/article_add.html', data)


def edit_article_view(request, slug):
    user_profile = UserMain.objects.get(user=request.user)
    article = get_object_or_404(Article, pk=slug)

    form = ArticleForm(request.POST or None, instance=article)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('save_article_success'))

    data = {
        'user_profile': user_profile,
        'form': form,
    }

    return render(request, 'profile/article_edit.html', data)


@login_required
def save_article_success(request):
    user_profile = UserMain.objects.get(user=request.user)
    return render(request, 'profile/article_success.html', {'user_profile': user_profile})
