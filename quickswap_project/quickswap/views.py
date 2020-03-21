from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from quickswap.models import Category, Page, Trade, Comment
from quickswap.forms import CategoryForm, PageForm, UserForm, UserProfileForm, TradeForm, CommentForm
from datetime import datetime
from django.contrib.auth.models import User
from quickswap.models import UserProfile
from django.views.generic import View
from django.utils.decorators import method_decorator

def home(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

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

    if request.method == 'POST':
        form = TradeForm(request.POST, request.FILES)

        if form.is_valid():
            trade = form.save(commit=True)
            trade.user = request.user
            #trade.user = user
            trade.save()
            return redirect('quickswap:trade', trade.slug)
        else:
            print(form.errors)

    return render(request, 'quickswap/add_trade.html', {'form': form})


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
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
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
        form = CommentForm()

        return(trade, comments, form)

    def get(self, request, trade_name_slug):
        try:
            (trade, comments, form) = self.get_Trade_Details(trade_name_slug)
        except TypeError:
            return redirect(reverse('quickswap:home'))

        context_dict = {'selected_trade':trade,
        'comment_list': comments,
        'comment_form': form}

        return render(request, 'quickswap/trade.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, trade_name_slug):
        print('!!!', trade_name_slug)
        try:
            (trade, comments, form) = self.get_Trade_Details(trade_name_slug)
        except TypeError:
            return redirect(reverse('quickswap:home'))

        print(trade, comments, form)

        form = CommentForm(request.POST, request.FILES)


        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            print(request.user.id)
            comment.trade = trade
            print(trade)
            form.save()
            return redirect('quickswap:trade', trade_name_slug)
        else:
            print(form.errors)

        context_dict = {'selected_trade':trade,
        'comment_list': comments,
        'comment_form': form}

        return render(request, 'quickswap/trade.html', context_dict)


class UserTradesView(View):
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            user = self.get_user(username)
        except TypeError:
            return redirect(reverse('quickswap:home'))

        return render(request,
                'quickswap/usertrades.html',
                {'selected_user': user, 'trade_list': Trade.objects.filter(user = user)})

    def get_user(self, username):
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        return(user)

class CategoryView(View):
    def get(self, request, category_name):
        print('!!!', category_name)
        return render(request,
                'quickswap/category.html',
                {'selected_category': category_name, 'trade_list': Trade.objects.filter(category = category_name.lower())})


class CategoriesView(View):

    def get(self, request):
        categories = {}
        categories = dict(Trade.CATEGORY_CHOICES).values()


        print('!!!', categories)
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

        return render(request,
                'quickswap/alltrades.html',
                {'trade_list': trades})



class ContactUsView(View):
    def get(self, request):

        return render(request, 'quickswap/contactus.html',)

class HelpdeskView(View):
    def get(self, request):

        return render(request, 'quickswap/helpdesk.html',)
