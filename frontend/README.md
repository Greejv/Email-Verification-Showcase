# Email Verification Showcase – frontend (Vite + React)

Stručne: Jednoduché UI na overenie e‑mailu. Má dve screeny a calluje dva backend endpointy na `http://localhost:8000`.

Ako to funguje
- Domovská stránka `/` (SendEmailPage)
  - Používateľ zadá svoj e‑mail a klikne „Odoslať“.
  - Frontend odošle požiadavku: `POST http://localhost:8000/verifycation/send` s `{ email }`.
  - Pri úspechu sa zobrazí hláška, že overovací e‑mail bol odoslaný. Pri chybe sa ukáže kde nastala chyba.

- Overovacia stránka `/verify` (VerificationPage)
  - Po kliknutí na odkaz v e‑maile prídete na URL s parametrom `token`, napr. `/verify?token=...`.
  - Frontend automaticky pošle request: `POST http://localhost:8000/verification/verify` s `{ token }`.
  - Zobrazí výsledok overenia (úspech alebo chyba). Kým čaká na odpoveď, ukáže „Prebieha overovanie…“.

Poznámky
- Aplikácia predpokladá zapnutý backend na `http://localhost:8000`.

Spustenie frontendu:
1) `npm install`
2) `npm run dev`
