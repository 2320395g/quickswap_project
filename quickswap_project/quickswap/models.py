from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


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

    name = models.CharField(max_length = NAME_MAX_LENGTH, unique=True)
    picture = models.ImageField(blank = False, upload_to='trade_images')
    category = models.CharField(max_length = 48, choices = CATEGORY_CHOICES)
    quality = models.CharField(max_length = 48, choices = QUALITY_CHOICES)
    description = models.CharField(max_length = 256, blank = False)
    suggested_trage = models.CharField(max_length = 128, blank = False)

    def __str__(self):
        return self.name
    '''
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Trade, self).save(*args, **kwargs)
        '''

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=256, blank = True)
    picture = models.ImageField(upload_to='profile_images', default = 'profile_images/default/default_profile_picture.png')

    def __str__(self):
        return self.user.username
