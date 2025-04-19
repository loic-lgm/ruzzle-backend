from django.contrib import admin

from brand.models import Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Brand, BrandAdmin)
