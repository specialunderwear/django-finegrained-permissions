from django.contrib import admin
from models import *
import fgp

@fgp.enforce
class InlineSpamAdmin(admin.StackedInline):
    model = Spam

@fgp.enforce
class ArticleAdmin(admin.ModelAdmin):
    inlines = [InlineSpamAdmin]
    model = Article
    
admin.site.register(Article, ArticleAdmin)
