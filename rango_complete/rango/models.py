from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    """
    A category represents a type of sport 
    """
    name_max_length = 128
    name = models.CharField(max_length=name_max_length, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(default='category',unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    """
    A page is used for displaying a piece of news 
    """
    title_max_length = 128
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=title_max_length)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """
    Storing user information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Team(models.Model):
    """
    Storing information of each team
    """
    likes = models.IntegerField(default=0)
    name = models.ForeignKey(Category, on_delete=models.CASCADE)
    country = models.CharField(max_length=128, blank=True, null=True)
    id = models.CharField(max_length=128, blank=True, primary_key=True)
    
    def __str__(self):
        return self.country