from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.ArticlePost)
admin.site.register(models.ArticleColumn)