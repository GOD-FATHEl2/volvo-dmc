# VOLVO DMC Generator (Data Matrix Code)

En modern mobilvänlig app för att generera och exportera unika DMC-koder (Data Matrix Codes) för industriellt bruk.

## 🛠 Funktioner

- Inloggning med användarnamn och lösenord
- Välj prefix (bokstav/siffra) via dropdown
- Automatisk kodgenerering: prefix + datum + tid (t.ex. `A7725640`)
- Genererar 30 koder i en 5x6 layout
- Exportera som PDF eller Excel
- Utskriftsvänlig sida
- Endast vit, grå, mörkgrå stil (Apple-lik design)
- Historik lagras i `database.json`
- Stöd för mobil och desktop

## 📦 Teknologi

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **DMC-generator**: `pylibdmtx`
- **PDF/Excel-export**: `reportlab`, `openpyxl`
- **Databas**: JSON-fil (ingen SQL behövs)
- **Delning**: via `ngrok` eller lokal server

## 🚀 Starta projektet

1. Installera beroenden:
   ```bash
   pip install flask pylibdmtx reportlab openpyxl
   ```

## 👤 Skapad av

**Nawoar Ekkou**

Volvo Cars Torslanda © 2025
