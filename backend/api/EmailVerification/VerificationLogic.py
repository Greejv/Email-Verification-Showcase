from datetime import datetime, timedelta, timezone
import jwt
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

from api.models import Email


JWT_ALGORITHM = "HS256"
secret = settings.SECRET_KEY

# vytvorenie tokenu s email_id a expiracy_time a odoslanie emailu s vytvorenym tokenom
def generate_verification(email):

    # Vytvorenie tokenu
    expiracy_time = 60 * 24
    now = datetime.now(tz=timezone.utc)
    payload = {
        "eid": email.id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expiracy_time)).timestamp()),
        "typ": "email-verify",
    }

    token = str(jwt.encode(payload, secret, algorithm=JWT_ALGORITHM))

    # Vytvorenie url pre overenie emailu
    verification_url = f"http://localhost:5173/verify?token={token}"

    # Vytvorenie obsahu emailu
    subject = "Overte si váš email"
    body = (
        "Vitajte!\n\n"
        "Prosím overte si váš email kliknutím na link dole:\n"
        f"{verification_url}\n\n"
        "Ak ste nepožiadali o overenie emailu, prosím ignorujte tento email."
    )

    # Nastavenia z Mailgun
    domain = "https://api.eu.mailgun.net/v3/mail.simonszi.me/messages"
    api_key = '0e0ffe9b3b9d7828cc7ac1b98ecfa7ea-67edcffb-9bef91ce'
    from_email = "Email Verification Showcase <postmaster@mail.simonszi.me>"

    # Odoslanie emailu
    response = requests.post(
            domain,
            auth=("api", api_key),
            data={
                "from": from_email,
                "to": [email.email],
                "subject": subject,
                "text": body,
            },
            timeout=10,
        )

    if 300 > response.status_code >= 200:
        return Response({"detail": "Email bol odoslaný."}, status=status.HTTP_200_OK)

    else:
        return Response({"detail": "Chyba pri odosielaní emailu."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# verifikacie emailu pomocou tokenu
def email_verifier(token: str):

    # Dekodovanie tokenu a overenie tokenu
    try:
        payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])

    except jwt.ExpiredSignatureError:
        return Response({"detail": "Token, už nieje platný."}, status=status.HTTP_410_GONE)

    except jwt.InvalidTokenError:
        return Response({"detail": "Nevhodný token."}, status=status.HTTP_400_BAD_REQUEST)

    email_id = payload.get("eid")

    # Premena email_id na intiger ak nieje
    try:
        email_id = int(email_id)
    except (TypeError, ValueError):
        return Response({"detail": "Nevhodný email_id v tokene."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # najdenie emailu v databaze pomocou email_id a zmana jeho stavu na verified = True
        try:
            email = Email.objects.get(id=email_id)
        except Email.DoesNotExist:
            return Response({"detail": "Email nebol nájdený."}, status=status.HTTP_404_NOT_FOUND)

        if email.verified:
            return Response({"detail": "Email, už je overený."}, status=status.HTTP_200_OK)

        email.verified = True
        email.save()
        return Response({"detail": "Email bol úspešne overený."}, status=status.HTTP_200_OK)

    except Exception as exc:
        return Response({"detail": f"Nepodarilo sa overiť email: {exc}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
