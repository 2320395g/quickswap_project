from django.contrib import admin
from quickswap.models import Category, UserProfile, Trade, Comment

class TradeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(UserProfile)
admin.site.register(Trade, TradeAdmin)
admin.site.register(Comment)
