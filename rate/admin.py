from django.contrib import admin

from rate.models import Rate

class RateAdmin(admin.ModelAdmin):
    list_display = ("rating", "comment", "reviewer", "reviewed", "created")


admin.site.register(Rate, RateAdmin)
