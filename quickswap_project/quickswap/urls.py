from django.urls import path
from quickswap import views

app_name = 'quickswap'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('restricted/', views.restricted, name='restricted'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('user/<username>/', views.ProfileView.as_view(), name='user'),
    path('allusers/', views.AllUsersView.as_view(), name='allusers'),
    path('contactus/', views.ContactUsView.as_view(), name='contactus'),
    path('helpdesk/', views.HelpdeskView.as_view(), name='helpdesk'),
    path('add_trade/', views.add_trade, name='add_trade'),
    path('alltrades/', views.AllTradesView.as_view(), name='alltrades'),
    path('trade/<slug:trade_name_slug>', views.TradeView.as_view(), name='trade'),
    path('usertrades/<username>/', views.UserTradesView.as_view(), name='usertrades'),
]
