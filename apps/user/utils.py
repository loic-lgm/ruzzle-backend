import os

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def generate_activation_link(user, request):
    """
    Generate an unique link to activate user account
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    frontend_url = os.environ.get("FRONTEND_URL")
    link = f"{frontend_url}/activation/{uid}/{token}/"
    return link
