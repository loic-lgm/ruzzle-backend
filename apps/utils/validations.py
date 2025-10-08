from io import BytesIO
from PIL import Image as PilImage
from django.core.files.base import ContentFile

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
except ImportError:
    pass


def process_image(
    image_file,
    max_width=500,
    max_height=800,
    max_size=5 * 1024 * 1024,
    allowed_formats=("JPEG", "PNG", "WEBP", "HEIC", "HEIF", "AVIF"),
):
    if not image_file:
        return None
    if image_file.size > max_size:
        raise ValueError("La taille de l'image ne doit pas dépasser 5Mo.")
    try:
        image = PilImage.open(image_file)
    except Exception:
        raise ValueError("Fichier image invalide.")
    if image.format not in allowed_formats:
        raise ValueError(
            f"Format {image.format} non supporté. "
            f"Formats autorisés : {allowed_formats}."
        )
    image = image.convert("RGB")
    format_to_use = "JPEG"
    file_ext = "jpg"
    if image.width > max_width or image.height > max_height:
        image.thumbnail((max_width, max_height))
    buffer = BytesIO()
    image.save(buffer, format=format_to_use, quality=85, optimize=True)
    file_ext = "jpg" if format_to_use == "JPEG" else "png"
    filename = f"{image_file.name.rsplit('.', 1)[0]}.{file_ext}"

    return ContentFile(buffer.getvalue(), name=filename)
