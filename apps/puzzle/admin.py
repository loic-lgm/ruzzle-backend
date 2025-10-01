from django.contrib import admin

from apps.puzzle.models import Puzzle


class PuzzleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "brand",
        "hashid",
        "piece_count",
        "description",
        "condition",
        "image",
        "status",
        "is_published",
        "created",
        "owner",
        "display_categories",
    )

    def display_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])

    display_categories.short_description = "Categories"


admin.site.register(Puzzle, PuzzleAdmin)
