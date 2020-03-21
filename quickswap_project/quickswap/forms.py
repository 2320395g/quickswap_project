from django import forms
from django.contrib.auth.models import User
from quickswap.models import Page, Category, UserProfile, Trade, Comment
from registration.forms import RegistrationForm



# We could add these forms to views.py, but it makes sense to split them off into their own file.



class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data

class TradeForm(forms.ModelForm):
    #user = forms.ForeignKey(widget=forms.HiddenInput())
    name = forms.CharField(max_length = 128, help_text="Please give your trade a name, try to be informative!")
    #picture = forms.ImageField()
    category = forms.ChoiceField(choices = Trade.CATEGORY_CHOICES,help_text="Please choose a category for your item of trade.")
    quality = forms.ChoiceField(choices = Trade.QUALITY_CHOICES,help_text="Please choose a level of quality for your item of trade.")
    description = forms.CharField(max_length = 256, help_text="Give your trade a description, let people know what it is and isn't!")
    suggested_trade = forms.CharField(max_length = 128, help_text="Help people know what you might want in return!")

    class Meta:
        model = Trade
        fields = ('name','picture','category',
            'quality','description','suggested_trade',)
        #exclude = ('user',)

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
