from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account, Following, Group


class AccountAdmin(UserAdmin):
    list_display = ('phone_number', 'username', 'date_joined',
                    'last_login', 'is_admin', 'is_staff')
    search_fields = ('phone_number', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class FollowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower')


admin.site.register(Account, AccountAdmin)
admin.site.register(Following, FollowingAdmin)
admin.site.register(Group)
