from django.urls import path
from quickswap import views

app_name = 'quickswap'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('category/<category_name>/', views.CategoryView.as_view(), name='category'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('user/<username>/', views.ProfileView.as_view(), name='user'),
    path('saved_trades/', views.SavedTradesView.as_view(), name='saved_trades'),
    path('allusers/', views.AllUsersView.as_view(), name='allusers'),
    path('contactus/', views.ContactUsView.as_view(), name='contactus'),
    path('helpdesk/', views.HelpdeskView.as_view(), name='helpdesk'),
    path('add_trade/', views.add_trade, name='add_trade'),
    path('alltrades/', views.AllTradesView.as_view(), name='alltrades'),
    path('trade/<slug:trade_name_slug>', views.TradeView.as_view(), name='trade'),
    path('edit_trade/<slug:trade_name_slug>/', views.EditTradeView.as_view(), name='edit_trade'), 
	path('save_trade/', views.SaveTradeView.as_view(), name='save_trade'),
    path('usertrades/<username>/', views.UserTradesView.as_view(), name='usertrades'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
]
