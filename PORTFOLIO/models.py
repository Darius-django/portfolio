from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

class Post(models.Model):
    author = models.CharField(max_length=60)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')

    def __str__(self):
        return f'{self.title}-{self.author}'

######################### here forms contact me###########
class Contact(models.Model):
    name = models.CharField(max_length=100,blank = False, null = False)
    email = models.EmailField(max_length=255,blank = False, null = False)
    projectDetails = models.CharField(max_length=2000,blank = False, null = False)

    def __str__(self):
        return f'{self.name}'
######################### coments block herre###########
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

#---------------scrap block herre--------------
class ScrapData(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.url} - {self.title}"
#------------shortner block here------------------
class URL(models.Model):
    original_url = models.CharField(max_length=255)
    shortened_url = models.CharField(max_length=255)

#----------quiz block here--------------
class Question(models.Model):
    question = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)
    ans = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.question

