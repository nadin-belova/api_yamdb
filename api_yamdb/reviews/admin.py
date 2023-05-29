from django.contrib import admin

from reviews.models import Category, Genre, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email',
        'bio', 'role')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
