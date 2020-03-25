from django.contrib import admin
from quickswap.models import Category, UserProfile, Trade, Comment, Pictures

class TradeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class PicturesAdmin(admin.ModelAdmin):
    list_display = ('trade', 'admin_thumbnail',)
    readonly_fields = ( 'admin_image', )

admin.site.register(UserProfile)
admin.site.register(Trade, TradeAdmin)
admin.site.register(Comment)
admin.site.register(Pictures, PicturesAdmin)
