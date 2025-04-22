from django.contrib import admin

from apps.rate.models import Rate

class RateAdmin(admin.ModelAdmin):
    list_display = ("rating", "comment", "owner", "reviewed", "created")


admin.site.register(Rate, RateAdmin)
