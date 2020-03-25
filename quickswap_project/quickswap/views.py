from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from quickswap.models import Category, Page, Trade, Comment, Pictures
from quickswap.forms import CategoryForm, PageForm, UserForm, UserProfileForm, TradeForm, CommentForm, PictureForm
from datetime import datetime
from django.contrib.auth.models import User
from quickswap.models import UserProfile
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView
from django.forms import modelformset_factory
from django.contrib import messages
from django.db.models import Count
import datetime

def home(request):
    #Used to filter most commented trade by those made in last week, otherwise older
    #trqdes with large amounts of comments ehos item has already been traded may
    #remain on the front page despite being of no interest
    date = datetime.date.today() - datetime.timedelta(days=7)
    trades_by_comments = Trade.objects.filter(date_made__gte=date).annotate(
            num_comments=Count('comment')).order_by('-num_comments')[:5]
    trades_by_newest = Trade.objects.order_by('-date_made')[:5]

    context_dict = {}
    context_dict['most_commented'] = trades_by_comments
    context_dict['most_recent'] = trades_by_newest
    visitor_cookie_handler(request)

    return render(request, 'quickswap/home.html', context=context_dict)

def about(request):
    # Spoiler: now you DO need a context dictionary!
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'quickswap/about.html', context=context_dict)


@login_required
def add_trade(request):
    #user = request.user
    form = TradeForm()
    PictureFormSet = modelformset_factory(Pictures, form=PictureForm, extra=5, min_num=1)

    if request.method == 'POST':
        form = TradeForm(request.POST, request.FILES)
        formset = PictureFormSet(request.POST, request.FILES,
                               queryset=Pictures.objects.none())


        if form.is_valid() and formset.is_valid():
            trade = form.save(commit = False)
            trade.user = request.user
            trade.save()

            user = UserProfile.objects.get_or_create(user=request.user)[0]
            user.trades_made += 1
            user.save()


            for forms in formset.cleaned_data:
                #this helps to not crash if the user
                #do not upload all the photos
                if forms:
                    picture = forms['picture']
                    image = Pictures(trade=trade, picture=picture)
                    image.save()

            return redirect('quickswap:trade', trade.slug)
        else:
            print(form.errors, formset.errors)
    else:
        form = TradeForm()
        formset = PictureFormSet(queryset=Pictures.objects.none())
    return render(request, 'quickswap/add_trade.html', {'form': form, 'formset': formset})


@login_required
def restricted(request):
    return render(request, 'quickswap/restricted.html')

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.datetime.now()))
    last_visit_time = datetime.datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits



@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('quickswap:home'))
        else:
            print(form.errors)
    context_dict = {'form': form}
    return render(request, 'quickswap/profile_registration.html', context_dict)


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'description': user_profile.description,'picture': user_profile.picture})

        return(user, user_profile, form)


    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('quickswap:home'))

        context_dict={'user_profile': user_profile,'selected_user': user,'form': form}

        return render(request,'quickswap/user.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('quickswap:home'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('quickswap:user', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,'selected_user': user,'form': form}

        return render(request,'quickswap/user.html', context_dict)




class TradeView(View):

    def get_Trade_Details(self, trade_name_slug):
        try:
            trade = Trade.objects.get(slug=trade_name_slug)
        except Trade.DoesNotExist:
            return None

        comments = Comment.objects.filter(trade = trade)
        pictures = Pictures.objects.filter(trade = trade)
        form = CommentForm()

        return(trade, comments, pictures, form)

    def get(self, request, trade_name_slug):
        try:
            (trade, comments, pictures, form) = self.get_Trade_Details(trade_name_slug)
        except TypeError:
            return redirect(reverse('quickswap:home'))

        context_dict = {'selected_trade':trade,
        'comment_list': comments,
        'picture_list': pictures,
        'comment_form': form}

        return render(request, 'quickswap/trade.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, trade_name_slug):
        try:
            (trade, comments, pictures , form) = self.get_Trade_Details(trade_name_slug)
        except TypeError:
            return redirect(reverse('quickswap:home'))

        form = CommentForm(request.POST, request.FILES)


        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.trade = trade
            form.save()
            return redirect('quickswap:trade', trade_name_slug)
        else:
            print(form.errors)

        context_dict = {'selected_trade':trade,
        'comment_list': comments,
        'picture_list': pictures,
        'comment_form': form}

        return render(request, 'quickswap/trade.html', context_dict)


class UserTradesView(View):

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            user = self.get_user(username)
        except TypeError:
            return redirect(reverse('quickswap:home'))


        trades = Trade.objects.filter(user = user)

        #This prevents a referenced before assignment error from dict
        picture_dict = {}
        comment_dict = {}
        if trades.count() != 0:
            for trade in trades:
                comment_dict[trade] = Comment.objects.filter(trade = trade).count()
                picture_dict[trade] =  (Pictures.objects.filter(trade = trade).first()).picture
            return render(request,
                    'quickswap/usertrades.html',
                    {'selected_user': user, 'trade_list': trades,'pictures':picture_dict, 'comment_num':comment_dict })

        else:
            return render(request,
                    'quickswap/usertrades.html',
                    {'selected_user': user, 'trade_list': trades})

    def get_user(self, username):
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        return(user)

class CategoryView(View):
    def get(self, request, category_name):

        trades = Trade.objects.filter(category = category_name.lower())

        picture_dict = {}
        comment_dict = {}
        if trades.count() != 0:
            for trade in trades:
                comment_dict[trade] = Comment.objects.filter(trade = trade).count()
                picture_dict[trade] =  (Pictures.objects.filter(trade = trade).first()).picture
        return render(request,
                'quickswap/category.html',
                {'selected_category': category_name,
                'trade_list': trades, 'pictures': picture_dict,
                 'comment_num':comment_dict })


class CategoriesView(View):
    def get(self, request):
        categories = {}
        categories = dict(Trade.CATEGORY_CHOICES).values()

        return render(request,
                'quickswap/categories.html',
                {'categories_list': categories})



class AllUsersView(View):
    def get(self, request):
        profiles = UserProfile.objects.all()

        return render(request,
                'quickswap/allusers.html',
                {'user_profile_list': profiles})

class AllTradesView(View):
    @method_decorator(login_required)
    def get(self, request):
        trades = Trade.objects.all()
        picture_dict = {}
        comment_dict = {}
        if trades.count() != 0:
            for trade in trades:
                comment_dict[trade] = Comment.objects.filter(trade = trade).count()
                picture_dict[trade] = (Pictures.objects.filter(trade = trade).first()).picture
        return render(request,
                'quickswap/alltrades.html',
                {'trade_list': trades, 'pictures': picture_dict, 'comment_num':comment_dict })


class ContactUsView(View):
    def get(self, request):
        return render(request, 'quickswap/contactus.html',)

class HelpdeskView(View):
    def get(self, request):
        return render(request, 'quickswap/helpdesk.html',)
