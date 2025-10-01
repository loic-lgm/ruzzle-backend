from django.contrib import admin

from apps.category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


admin.site.register(Category, CategoryAdmin)
