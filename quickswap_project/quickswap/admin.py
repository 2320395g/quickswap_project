from django.contrib import admin
from quickswap.models import UserProfile, Trade, Comment, Pictures
from mapbox_location_field.admin import MapAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse

class TradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',)
    prepopulated_fields = {'slug': ('name',)}
    #This is readonly and not just a field as it cannot be edited and will cause an error otherwise
    readonly_fields = ('date_made', )

class TradeAdminWithMap(TradeAdmin, MapAdmin):
    pass

class PicturesAdmin(admin.ModelAdmin):
    list_display = ('trade', 'admin_user', 'admin_thumbnail',)
    readonly_fields = ('admin_image', )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('trade', 'user', 'admin_thumbnail', )
    readonly_fields = ('admin_image','date_made', )

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin_thumbnail',)
    readonly_fields = ('admin_image', )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Trade, TradeAdminWithMap)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Pictures, PicturesAdmin)
