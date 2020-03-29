from django.contrib import admin
from quickswap.models import UserProfile, Trade, Comment, Pictures
from mapbox_location_field.admin import MapAdmin

class TradeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class TradeAdminWithMap(TradeAdmin, MapAdmin):
    pass

class PicturesAdmin(admin.ModelAdmin):
    list_display = ('trade', 'admin_thumbnail',)
    readonly_fields = ( 'admin_image', )

admin.site.register(UserProfile)
admin.site.register(Trade, TradeAdminWithMap)
admin.site.register(Comment)
admin.site.register(Pictures, PicturesAdmin)
