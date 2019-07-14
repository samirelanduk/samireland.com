from django.contrib import admin
from django.db import models
from django.forms import Textarea, ModelForm
from .models import *

class PublicationAdminForm(ModelForm):
    class Meta:
        model = Publication
        exclude = []
        widgets = {"body": Textarea(attrs={
         "style": "max-height: none;", "rows": 100, "class": "vLargeTextField"
        })}

class PublicationAdmin(admin.ModelAdmin):
    form = PublicationAdminForm


class ArticleAdminForm(ModelForm):
    class Meta:
        model = Article
        exclude = []
        widgets = {"body": Textarea(attrs={
         "style": "max-height: none;", "rows": 100, "class": "vLargeTextField"
        })}

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm


class BlogPostAdminForm(ModelForm):
    class Meta:
        model = BlogPost
        exclude = []
        widgets = {"body": Textarea(attrs={
         "style": "max-height: none;", "rows": 30, "class": "vLargeTextField"
        })}

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm


admin.site.register(EditableText)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Project)
admin.site.register(Article, ArticleAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(MediaFile)
