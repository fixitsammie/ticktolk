from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from PIL import Image
from django.utils.text import slugify


class UserProfile(models.Model):
    user=models.OneToOneField(User)
    pic=models.ImageField(upload_to='img',blank=True)

    def  __str__(self):
        return self.user.username
    
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    
class Thread(models.Model):
    topic=models.CharField(max_length=100)
    slug=models.CharField(max_length=150)
    main_post=models.CharField(max_length=1000)
    category=models.ForeignKey('Category')
    user=models.ForeignKey(User)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    image=models.ImageField(blank=True,upload_to='img/%y/%m/%d')

    def __str__(self):
        return self.topic
    def save(self,*args,**kwargs):
        if not self.id:
            self.slug=slugify(self.topic)
        super(Thread, self).save(*args,**kwargs)

    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('get_thread', args=[str(self.slug)])


class Category(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=500,null=True)
    
    slug=models.CharField(max_length=70)
   
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('get_category',args=[str(self.slug)])
  
    def save(self,*args,**kwargs):
        if not self.id:
            self.slug=slugify(self.name)
        super(Category,self).save(*args,**kwargs)
   


    def __str__(self):
        return self.name



class Post(models.Model):
    thread=models.ForeignKey(Thread)
    post=models.CharField(max_length=1000)
    markdown=models.CharField(max_length=2000)
    user=models.ForeignKey(User)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    post_type=models.CharField(max_length=50)

    def __str__(self):
        return self.post
    
