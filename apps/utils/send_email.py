from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email(
    subject: str,
    to: list[str],
    template: str,
    context: dict,
    plain_text: str = None,
    from_email: str = "Ruzzle Team <info@ruzzle.fr>",
):
    html_content = render_to_string(template, context)
    body = plain_text or f"{subject}\n\n{context}"
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_activation_email(user, activation_link: str):
    return send_email(
        subject="Active ton compte sur Ruzzle",
        to=[user.email],
        template="emails/activation.html",
        context={"user": user, "activation_link": activation_link},
        plain_text=f"Salut {user.username},\nClique sur ce lien pour activer ton compte : {activation_link}",
    )

def send_reset_password_email(user, reset_link: str):
    return send_email(
        subject="Réinitialisation de ton mot de passe sur Ruzzle",
        to=[user.email],
        template="emails/reset_password.html",
        context={"user": user, "reset_link": reset_link},
        plain_text=f"Salut {user.username},\nClique sur ce lien pour réinitialiser ton mot de passe : {reset_link}",
    )

def send_swap_requested_email(user, swap_request_link: str):
    return send_email(
        subject="Une demande d'échange t'as été proposée",
        to=[user.email],
        template="emails/swap_requested.html",
        context={"user": user, "swap_request_link": swap_request_link},
        plain_text=f"Salut {user.username},\nClique sur ce lien pour consulter tes demandes reçues : {swap_request_link}",
    )

def send_swap_accepted_email(user, swap_accepted_link: str):
    return send_email(
        subject="Ta demande d'échange a été acceptée",
        to=[user.email],
        template="emails/swap_accepted.html",
        context={"user": user, "swap_accepted_link": swap_accepted_link},
        plain_text=f"Salut {user.username},\nClique sur ce lien pour consulter tes demandes acceptées : {swap_accepted_link}",
    )


def send_swap_denied_email(user, browse_link: str):
    return send_email(
        subject="Ta demande d'échange a été refusée",
        to=[user.email],
        template="emails/swap_denied.html",
        context={"user": user, "browse_link": browse_link},
        plain_text=f"Salut {user.username},\nClique sur ce lien pour consulter les autres puzzles : {browse_link}",
    )
