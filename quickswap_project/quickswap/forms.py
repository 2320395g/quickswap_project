from django import forms
from django.contrib.auth.models import User
from quickswap.models import  UserProfile, Trade, Comment, Pictures
from registration.forms import RegistrationForm


class TradeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '60'}), max_length = 128, help_text="Please give your trade a name, try to be informative!")
    category = forms.ChoiceField(choices = Trade.CATEGORY_CHOICES,help_text="Please choose a category for your item of trade.")
    quality = forms.ChoiceField(choices = Trade.QUALITY_CHOICES,help_text="Please choose a level of quality for your item of trade.")
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":4, "cols":60}), help_text="Give your trade a description, let people know what it is and isn't!")
    suggested_trade = forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":60}),max_length = 128, help_text="Help people know what you might want in return!")

    class Meta:
        model = Trade
        fields = ('name','category',
            'quality','description','suggested_trade', 'location',)
			
			
class EditTradeForm(forms.ModelForm):

	#name = None the name is a unique key, we kinda can't change it. We should instead have a unique id
	category = None
	quality = None
	description = None
	suggested_trade = None

	class Meta:
		model = Trade
		#fields = ('name','category','quality','description','suggested_trade','location',)
		fields = ('category','quality','description','suggested_trade','location',)
		
		
	def __init__(self, *args, **kwargs):
		trade = kwargs.pop('trade')
		super(EditTradeForm, self).__init__(*args, **kwargs)
		# self.fields['name'] = forms.CharField( 	widget=forms.TextInput(attrs={'size': '60'}), 
										# max_length = 128, 
										# help_text="Please give your trade a name, try to be informative!",
										# initial=trade.name
										# )
		self.fields['category'] = forms.ChoiceField(	choices = Trade.CATEGORY_CHOICES,
											help_text="Please choose a category for your item of trade.",
											initial=trade.category
											)
		self.fields['quality'] = forms.ChoiceField(	choices = Trade.QUALITY_CHOICES,
											help_text="Please choose a level of quality for your item of trade.",
											initial=trade.quality
											)
		self.fields['description'] = forms.CharField(	widget=forms.Textarea(attrs={"rows":4, "cols":60}), 
											help_text="Give your trade a description, let people know what it is and isn't!", 
											initial=trade.description
											)
		self.fields['suggested_trade'] = forms.CharField(	widget=forms.Textarea(attrs={"rows":2, "cols":60}),
												max_length = 128, 
												help_text="Help people know what you might want in return!", 
												initial=trade.suggested_trade
												)


class PictureForm(forms.ModelForm):
    #this does not have helptext as it will display it for each input
    picture = forms.ImageField(label='Image', required = True)

    class Meta:
        model = Pictures
        fields = ('picture',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('description', 'picture',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'picture')
