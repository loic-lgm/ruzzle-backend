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
    max_width=800,
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
    if image.width > max_width or image.height > max_height:
        image.thumbnail((max_width, max_height), PilImage.Resampling.LANCZOS)
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=85, optimize=True)
    filename = f"{image_file.name.rsplit('.', 1)[0]}.jpg"
    return ContentFile(buffer.getvalue(), name=filename)
