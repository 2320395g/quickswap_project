from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.safestring import mark_safe
from mapbox_location_field.models import LocationField

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
	location = LocationField(map_attrs={"center": [-4.28992174937531, 55.872480052801336]})
	slug = models.SlugField()
	date_made = models.DateTimeField(auto_now = True)
	#saves_count = models.IntegerField(default= 0 )

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

    #these are mark safe as otherwise it wont display the image, instead the html
    def admin_image(self):
        return mark_safe('<img src="%s" />' % self.picture.url)
    admin_image.short_description = 'Picture Display'

    def admin_thumbnail(self):
        return mark_safe('<img src="%s" width="48" height="48" />' % self.picture.url)
    admin_thumbnail.short_description = 'Picture'

    def admin_user(self):
        return (self.trade.user)
    admin_user.short_description = 'User'



class Comment(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, default = None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    picture = models.ImageField(blank = True, upload_to='comment_images')
    date_made = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_made']

    def admin_thumbnail(self):
        if self.picture != '':
            return  mark_safe('<img src="%s" width="48" height="48" />' % self.picture.url)
    admin_thumbnail.short_description = 'Picture'

    def admin_image(self):
        if self.picture != '':
            return  mark_safe('<img src="%s" />' % self.picture.url)
    admin_image.short_description = 'Picture'

    def __str__(self):
        return (self.text + ' - ' + self.user.username)

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=256, blank = True)
	picture = models.ImageField(upload_to='profile_images', blank = True, default = 'profile_images/default/default_profile_picture.png')
	#A model is used to hold the number of trades rather than using a query to find
	#trades associatde with the user, as a trade may be deleted at some point,
	#making the number inaccurate.
	trades_made = models.IntegerField(default = 0)
	comments_made = models.IntegerField(default = 0)
	saved_trades = models.ManyToManyField(Trade)

	def admin_thumbnail(self):
		if self.picture != '':
			return  mark_safe('<img src="%s" width="48" height="48" />' % self.picture.url)
	admin_thumbnail.short_description = 'Picture'	
	
	def admin_image(self):
		if self.picture != '':
			return  mark_safe('<img src="%s" />' % self.picture.url)
	admin_image.short_description = 'Picture'

	def __str__(self):
		return self.user.username
