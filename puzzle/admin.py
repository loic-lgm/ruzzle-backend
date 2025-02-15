from django.contrib import admin

from puzzle.models import Puzzle


class PuzzleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "piece_count",
        "piece_count",
        "description",
        "condition",
        "image_url",
        "status",
        "is_published",
        "created",
        "owner",
    )


admin.site.register(Puzzle, PuzzleAdmin)
