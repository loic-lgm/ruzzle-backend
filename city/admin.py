from django.contrib import admin

from city.models import City


class CityeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "zip_code",
        "country",
    )


admin.site.register(City, CityeAdmin)
