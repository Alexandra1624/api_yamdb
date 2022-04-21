from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'date_joined',
    )
    list_editable = ('role',)
    search_fields = ('email',)
    list_filter = ('date_joined',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
