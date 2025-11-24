# Email Verification Showcase – stručný popis

**Stručne:** Jednoduchý Django server na ukážku logiky pre overenie e-mailov. Ma ukázať logiku overovania: `VerificationLogic.py`,
ktorá obsahuje dve funckie: `generate_verification` a `email_verifier`.

## Priebeh:
1. Použivateľ odošle e‑mail na endpoint: `api/verification/send/`.
2. Server uloží e-mail do databázy a callne funkciu: `generate_verification` s e-mailom.
3. Funkcia `generate_verification` vytvorý JWT Token, ktorý obsahuje id, pod ktorým je uložený email a pošle e-mail použivateľovi s linkom.
4. Po kliknutí na link: `http://localhost:5173/verify?token={token}` sa použivateľ dostane na frontend stránku, ktorá token odošle na endpoint: `api/verification/verify/`
5. Server token extrahuje s requestu a callne s ním funkciu: `email_verifier`.
6. Funkcia `email_verifier` dekóduje token, extrahuje id, pod ktorým bol email uložený, najde ho v databáze a upravý stav na: `verified = True`

## Endpointy:
- POST /api/verification/send/
  - View: `send_email`
  - Vstup (JSON): { "email": "user@example.com" }
  - Správanie: Uloží e-mail do databázy, a callne funkciu `generate_verification` s e-mailom, ktorý bol práve uložený.
  - Výstup: Uložené údaje a HTTP_201_CREATED.


- POST /api/verification/verify/
  - View: `verify_token`
  - Vstup: (JSON): { "token": "{token}" }
  - Správanie: Callne funkciu `email_verifier` s tokenom z requestu.
  - Výstup: Výstup z funkcie posunie ďalej.

## Hlavná pointa:
- Hlavnou pointou, tohto backendu je ukázať funkcie: **generate_verification** a **email_verifier**
- **Čo robia:**

  - generate_verification(email):
    - Vygeneruje JWT Token s id e-mailu, ktorý dostal pri callnutí a s dobou expirácie.
    - Zostaví overovací link a odošle e‑mail cez Mailgun API.
  - email_verifier(token):
    - Dekóduje a overí token (expirácia, signature, typ).
    - Extrahuje id e-mailu.
    - Najde e-mail v databáze pomocou id, a nastaví pole "verified" na True


- kód je jasne okomentovaný, takže sa v ňom dá ľahko zorientovať.

## Dôležité info:

- Logika overovania (funkcie), môžu byť spustené hocikedy a hocičím.
- Ich účel može byť jednoducho upravý podľa potreby. V tomto prípade overujeme e-maily v databáze pomocou id e-mailov, ale môžme overiť napr. použivateľov pomocou ich id's.
- V tomto prípade sa po overení tokenu zmení pole "verified" na True pri danom e-maily, ale može sa spraviť hocičo potrebné.


## Súbory:
- **Model:** api/models.py (Email: email, verified)
- **Serializér:** api/serializers.py
- **Endpoints:** api/views.py, api/urls.py
- **Logika Overovania:** api/EmailVerification/VerificationLogic.py

## Záver:

- Server ukazuje využitie funkcii: `generate_verification` a `email_verifier`.
- Funkcie sa dajú využiť hocikde, a dajú sa jednoducho upraviť podľa potreby.


## Ako spustiť server:
 **1. Vytvorte a spustite venv:**

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

MacOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**2. Nainštalujte requirements:**

```bash
pip install -r requirements.txt
```

**3. Vytvorenie lokálnej databázy:**

Windows:
```bash
python manage.py migrate
```

MacOS:
```bash
python3 manage.py migrate
```

**4. Spustite Django server:**

Windows:
```bash
python manage.py runserver
```

MacOS:
```bash
python3 manage.py runserver
```