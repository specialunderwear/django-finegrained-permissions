from django.db import models
from fgp import guard
# Create your models here.

@guard('on_frontpage')
class Article(models.Model):
    """An article in a blog"""
    title = models.CharField(max_length=200)
    abstract = models.CharField(max_length=1000)
    body = models.TextField()
    slug = models.SlugField()
    on_frontpage = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%d Article" % (self.pk,)
    
    class Meta:
        verbose_name = 'a nice article'
    
@guard('is_spam')
class Spam(models.Model):
    """Spam posted by a user"""
    article = models.ForeignKey(Article)
    title = models.CharField(blank=True, max_length=100)
    email = models.EmailField()
    name = models.CharField(blank=True, max_length=256)
    body = models.TextField()
    is_spam = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%d Spam" % (self.pk,)
