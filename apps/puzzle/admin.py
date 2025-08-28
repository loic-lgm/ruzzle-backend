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
    )


admin.site.register(Puzzle, PuzzleAdmin)
