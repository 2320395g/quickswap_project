from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings


class Category(models.Model):
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Trade(models.Model):

    #If you want to include a category with a space in it, you might need to
    #add a slug as one of their values is user as a url.
    CATEGORY_CHOICES = (
        ('art','Art'),
        ('books', 'Books'),
        ('clothes', 'Clothes'),
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('toys', 'Toys'),
        ('other', 'Other'),
    )
    QUALITY_CHOICES = (
        ('new', 'New'),
        ('good','Good'),
        ('fair','Fair'),
        ('slightly-damaged', 'Slightly Damaged'),
        ('battle-scarred', 'Battle Scarred'),
    )

    NAME_MAX_LENGTH = 128


    user = models.ForeignKey(settings.AUTH_USER_MODEL, default = None, on_delete=models.CASCADE)
    name = models.CharField(max_length = NAME_MAX_LENGTH, unique=True)
    category = models.CharField(max_length = 48, choices = CATEGORY_CHOICES)
    quality = models.CharField(max_length = 48, choices = QUALITY_CHOICES)
    description = models.TextField(blank = False)
    suggested_trade = models.CharField(max_length = 128, blank = False)
    slug = models.SlugField()
    date_made = models.DateField(auto_now = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Trade, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Pictures(models.Model):
    trade = models.ForeignKey(Trade,on_delete=models.CASCADE, default=None)
    picture = models.ImageField(upload_to='trade_images')

    #Need this otherwise it just adds an 's' in admin and displays it as Picturess
    class Meta:
        verbose_name_plural = "Pictures"

class Comment(models.Model):
     trade = models.ForeignKey(Trade, on_delete=models.CASCADE, default = None)
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     text = models.TextField()
     picture = models.ImageField(blank = True, upload_to='comment_images')
     date_made = models.DateTimeField(auto_now_add=True)

     class Meta:
        ordering = ['date_made']

     def __str__(self):
        return (self.text + ' - ' + self.user.username)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=256, blank = True)
    picture = models.ImageField(upload_to='profile_images', blank = True, default = 'profile_images/default/default_profile_picture.png')

    def __str__(self):
        return self.user.username
