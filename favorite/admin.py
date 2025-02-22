from django.contrib import admin

from favorite.models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "puzzle")


admin.site.register(Favorite, FavoriteAdmin)
