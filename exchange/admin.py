from django.contrib import admin

from exchange.models import Exchange

class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("status", "puzzle", "owner", "created", "updated")


admin.site.register(Exchange, ExchangeAdmin)
