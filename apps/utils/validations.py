from PIL import Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile


def process_image(
    image_file,
    max_width=1000,
    max_height=1000,
    max_size=2 * 1024 * 1024,
    allowed_formats=["JPEG", "PNG"],
):
    if image_file.size > max_size:
        raise ValueError(
            "La taille de l'image ne doit pas dépasser 2MB."
        )

    try:
        image = PilImage.open(image_file)
    except Exception:
        raise ValueError("Fichier image invalide.")

    if image.format not in allowed_formats:
        raise ValueError(
            f"Format {image.format} non supporté. Formats autorisés : {allowed_formats}."
        )

    if image.width > max_width or image.height > max_height:
        image.thumbnail((max_width, max_height))
        buffer = BytesIO()
        format_to_use = "JPEG" if image.format == "JPEG" else "PNG"
        image.save(buffer, format=format_to_use, quality=85, optimize=True)

        return ContentFile(buffer.getvalue(), name=image_file.name)

    return image_file


def validate_image(value, serializers):
    try:
        return process_image(value)
    except ValueError as e:
        raise serializers.ValidationError(str(e))
