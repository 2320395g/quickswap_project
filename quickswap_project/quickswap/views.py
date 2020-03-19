from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from quickswap.models import Category, Page, Trade
from quickswap.forms import CategoryForm, PageForm, UserForm, UserProfileForm, TradeForm
from datetime import datetime
from django.contrib.auth.models import User
from quickswap.models import UserProfile
from django.views.generic import View
from django.utils.decorators import method_decorator

def home(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    #user_profile=UserProfile.objects.get_or_create(user=user)[0]
    #form=UserProfileForm({'website': user_profile.website,'picture': user_profile.picture})

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    #context_dict['picture'] =


    visitor_cookie_handler(request)

    return render(request, 'quickswap/home.html', context=context_dict)

def about(request):
    # Spoiler: now you DO need a context dictionary!
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'quickswap/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'quickswap/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('quickswap:home'))
        else:
            print(form.errors)

    return render(request, 'quickswap/add_category.html', {'form': form})

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
            return redirect(reverse('quickswap:home'))
        else:
            print(form.errors)

    return render(request, 'quickswap/add_trade.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    # You cannot add a page to a Category that does not exist... DM
    if category is None:
        return redirect(reverse('quickswap:home'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('quickswap:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  # This could be better done; for the purposes of TwD, this is fine. DM.

    context_dict = {'form': form, 'category': category}
    return render(request, 'quickswap/add_page.html', context=context_dict)

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
            print(user.username)
            return redirect('quickswap:user', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,'selected_user': user,'form': form}

        return render(request,'quickswap/user.html', context_dict)

class TradeView(View):


    def get(self, request, trade_name_slug):
        context_dict = {}
        try:
            trade = Trade.objects.get(slug=trade_name_slug)
            context_dict['selected_trade'] = trade
        except Category.DoesNotExist:
            context_dict['selected_trade'] = None

        return render(request, 'quickswap/trade.html', context_dict)


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
