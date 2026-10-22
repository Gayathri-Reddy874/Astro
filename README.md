# 🔮 Vedic Astrology AI

> A Flask web app for **Vedic (Jyotish) astrology**: sidereal birth charts, Panchanga, Guna Milan kundali matching, rule-based predictions with remedies, and an AI astrologer chat ("Cosmic Sage") powered by OpenAI.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?logo=flask&logoColor=white)
![Swiss Ephemeris](https://img.shields.io/badge/Swiss%20Ephemeris-pyswisseph-8A2BE2)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### 🪐 Birth chart (Kundali)
- Planetary positions for **Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu and Ketu**
- Sign (Rashi) in both Sanskrit and English names, degree, **Nakshatra and Pada**
- **Ascendant (Lagna)** and a **12-house** layout
- **Panchanga** summary: Tithi and Nakshatra (Yoga and Karana are simplified placeholders)
- Sidereal zodiac using the **Lahiri ayanamsa**, computed with the Swiss Ephemeris

### 💞 Kundali matching (Guna Milan)
- Eight koota scoring out of **36 points**: Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi
- **Manglik** check for both partners
- Overall compatibility band, from *Excellent* down to *Not Recommended*

### 📜 Predictions and remedies
- Rule-based signals from planetary house placements: personality, career strengths and suggested fields, relationships, spiritual growth, health focus areas, challenges and life purpose
- Matching remedies (mantras, charity, practices) for detected signals

### 🤖 AI astrologer chat
- "Cosmic Sage" persona built on the OpenAI Chat API
- Answers are grounded in your generated chart, predictions and remedies
- Short-term conversation memory per session, quick-start question suggestions and a clear-chat endpoint

### 🔌 JSON API
- Chart data and chat available over simple REST endpoints (see below)

---

## 🛠️ Tech stack

| Layer | Tools |
|---|---|
| Backend | Python, Flask |
| Astronomy | `pyswisseph` (Swiss Ephemeris), Lahiri ayanamsa |
| AI | OpenAI Chat Completions |
| Frontend | Jinja2 templates, HTML/CSS (`templates/`, `static/css/`) |
| Config | `python-dotenv` |

---

## 📁 Project structure

```
Astro/
├── app.py                # Flask app: routes, chart calculation, Panchanga, API endpoints
├── astrology_utils.py    # Guna Milan matching, prediction signals, remedies
├── ai_assistant.py       # VedicAIAssistant (OpenAI chat) + question suggestions
├── templates/            # Jinja2 pages (home, chart, matching, AI chat, about)
├── static/css/           # Styles
├── requirements.txt
└── LICENSE
```

---

## 🚀 Getting started

### 1. Clone and install

```bash
git clone https://github.com/Gayathri-Reddy874/Astro.git
cd Astro

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=change-this-to-a-long-random-string
```

> The chart and matching features work without an OpenAI key. Only the AI chat needs it; without a key the app starts and the chat endpoint returns a "service unavailable" message.

### 3. Run

```bash
python app.py
```

Open **http://localhost:5000**.

---

## 🧭 Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Birth details form |
| `/chart` | POST | Generate chart, predictions and remedies |
| `/compatibility` | GET | Kundali matching form |
| `/match` | POST | Guna Milan result |
| `/ai-chat` | GET | AI astrologer chat UI |
| `/about` | GET | About page |
| `/api/horoscope` | POST | Chart data as JSON |
| `/api/chat` | POST | Send a message to the AI astrologer |
| `/api/chat/clear` | POST | Clear conversation history |
| `/api/chat/suggestions` | GET | Suggested questions |

### Example: horoscope API

```bash
curl -X POST http://localhost:5000/api/horoscope \
  -H "Content-Type: application/json" \
  -d '{
        "year": 2000, "month": 1, "day": 1,
        "hour": 10, "minute": 30, "second": 0,
        "latitude": 12.9716, "longitude": 77.5946,
        "timezone": 5.5
      }'
```

`hour` is local time in 24h format; `timezone` is the offset from UTC in hours (default `5.5`, IST).

---

## 🧮 How it works

1. **Time conversion**: local birth time is converted to UTC and then to a Julian Day.
2. **Positions**: the Swiss Ephemeris returns planetary longitudes, converted to sign, degree, Nakshatra (27 × 13°20′) and Pada.
3. **Panchanga**: Tithi comes from the Moon–Sun longitude difference in 12° steps.
4. **Matching**: Moon Nakshatra and Rashi of each partner feed the eight kootas, summed to a score out of 36.
5. **Predictions**: house placements of key planets trigger simple rules that produce the signals and remedies shown on the chart page.
6. **AI chat**: a summary of the chart is added to the system prompt so answers are personalised.

---

## ⚠️ Limitations

- Several kootas (Vashya, Tara, Bhakoot, Nadi) use **simplified rules**, and matching currently uses the birth **date** only (Moon taken at noon), so results are indicative rather than traditional-grade.
- Yoga and Karana in the Panchanga are placeholders.
- Predictions are generic, rule-based text, not a substitute for a professional reading.
- Chat history is kept in server memory and resets on restart.

## 🗺️ Roadmap

- [ ] Full traditional koota tables and birth-time-aware matching
- [ ] Complete Panchanga (Yoga, Karana, Vara)
- [ ] Vimshottari Dasha timeline
- [ ] Divisional charts (Navamsa)
- [ ] Persistent chat storage and Docker deployment

---

## 📌 Disclaimer

This project is built for **learning and entertainment**. Astrological output is not scientific fact and must not be used for medical, legal or financial decisions.

## 📄 License

Released under the [MIT License](LICENSE).

## 👩‍💻 Author

**Mallareddygari Gayathri**
[GitHub](https://github.com/Gayathri-Reddy874) · [LinkedIn](https://linkedin.com/in/mallareddygari-gayathri)
