from django.contrib import admin
from .models import Article


class ArticleSlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Article, ArticleSlug)
