from django.contrib import admin

from apps.exchange.models import Exchange

class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("status", "puzzle_asked", "puzzle_proposed", "owner", "created", "updated")


admin.site.register(Exchange, ExchangeAdmin)
