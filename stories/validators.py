from django.core.exceptions import ValidationError

MAX_MUGSHOT_BYTES = 5 * 1024 * 1024  # 5 MB in bytes


def validate_mugshot_size(image):
    if image and image.size > MAX_MUGSHOT_BYTES:
        mb = image.size / (1024 * 1024)
        raise ValidationError(
            f"That mugshot is {mb:.1f}MB. Keep it under 5MB - "
            f"we're booking a suspect, not printing a billboard."
        )