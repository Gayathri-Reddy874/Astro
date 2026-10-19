from flask import Flask, render_template, request, jsonify
from astrology_utils import match_dates, generate_prediction_signals, get_remedies
from datetime import datetime
import swisseph as swe
import os
from dotenv import load_dotenv
from ai_assistant import VedicAIAssistant, get_question_suggestions
from flask import session, jsonify, request
import uuid

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'vedic-astro-secret-key')

# Lahiri ayanamsa
swe.set_sid_mode(swe.SIDM_LAHIRI)

# zodiac signs
SIGNS = [
    "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
    "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
]

# English signs for better understanding
SIGNS_EN = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

TITHIS = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dvadashi",
    "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dvadashi",
    "Trayodashi", "Chaturdashi", "Amavasya"
]

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN
}

PLANET_SYMBOLS = {
    "Sun": "☉",
    "Moon": "☽",
    "Mercury": "☿",
    "Venus": "♀",
    "Mars": "♂",
    "Jupiter": "♃",
    "Saturn": "♄",
    "Rahu": "☊",
    "Ketu": "☋"
}

def zodiac(lon):
    sign_index = int(lon / 30)
    sign = SIGNS[sign_index]
    sign_en = SIGNS_EN[sign_index]
    deg = lon % 30
    return sign, sign_en, round(deg, 2)

def nakshatra_calc(lon):
    n = lon / (360/27)
    index = int(n)
    pada = int((n - index) * 4) + 1
    return NAKSHATRAS[index], pada

def planet_positions(jd):
    data = {}
    for name, p in PLANETS.items():
        lon = swe.calc_ut(jd, p, swe.FLG_SIDEREAL)[0][0]
        sign, sign_en, deg = zodiac(lon)
        nak, pada = nakshatra_calc(lon)

        data[name] = {
            "longitude": round(lon, 3),
            "sign": sign,
            "sign_en": sign_en,
            "degree": deg,
            "nakshatra": nak,
            "pada": pada,
            "symbol": PLANET_SYMBOLS.get(name, "")
        }

    # Rahu & Ketu
    rahu = swe.calc_ut(jd, swe.MEAN_NODE)[0][0]
    ketu = (rahu + 180) % 360
    
    rahu_sign, rahu_sign_en, _ = zodiac(rahu)
    ketu_sign, ketu_sign_en, _ = zodiac(ketu)

    data["Rahu"] = {
        "longitude": round(rahu, 3),
        "sign": rahu_sign,
        "sign_en": rahu_sign_en,
        "symbol": PLANET_SYMBOLS["Rahu"]
    }
    data["Ketu"] = {
        "longitude": round(ketu, 3),
        "sign": ketu_sign,
        "sign_en": ketu_sign_en,
        "symbol": PLANET_SYMBOLS["Ketu"]
    }

    return data

def ascendant(jd, lat, lon):
    houses = swe.houses(jd, lat, lon)
    asc = houses[1][0]
    sign, sign_en, deg = zodiac(asc)

    return {
        "longitude": round(asc, 3),
        "sign": sign,
        "sign_en": sign_en,
        "degree": deg
    }

def house_system(jd, lat, lon):
    houses = swe.houses(jd, lat, lon)
    cusps = houses[0]

    result = {}

    for i, c in enumerate(cusps):
        sign, sign_en, deg = zodiac(c)
        result[f"House {i+1}"] = {
            "sign": sign,
            "sign_en": sign_en,
            "degree": deg
        }

    return result

def panchanga(jd):
    sun = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
    moon = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]

    diff = (moon - sun) % 360
    tithi_index = int(diff / 12)
    tithi = TITHIS[tithi_index]

    nak, pada = nakshatra_calc(moon)

    # Calculate yoga and karana (simplified)
    yoga_index = int((sun + moon) / (360/27)) % 27
    karana_index = tithi_index * 2

    return {
        "Tithi": tithi,
        "Tithi_Index": tithi_index + 1,
        "Nakshatra": nak,
        "Pada": pada,
        "Yoga": f"Yoga {yoga_index + 1}",
        "Karana": f"Karana {karana_index + 1}"
    }

def vedic_horoscope(year, month, day, hour, lat, lon):
    jd = swe.julday(year, month, day, hour)

    chart = {
        "Ascendant": ascendant(jd, lat, lon),
        "Planets": planet_positions(jd),
        "Houses": house_system(jd, lat, lon),
        "Panchanga": panchanga(jd),
        "JulianDay": jd
    }

    return chart

@app.route('/')
def index():
    """Home page with birth details form"""
    return render_template('index.html', 
                         title='Vedic Astrology - Cosmic Green',
                         current_year=datetime.now().year)

# Add these imports at the top
from astrology_utils import match_dates, generate_prediction_signals, get_remedies

# Add these new routes

@app.route('/compatibility')
def compatibility():
    """Compatibility matching page"""
    return render_template('compatibility.html',
                         title='Kundali Matching - Cosmic Green',
                         current_year=datetime.now().year)

@app.route('/match', methods=['POST'])
def match_kundalis():
    """Perform compatibility matching"""
    try:
        # Get boy's details
        boy_year = int(request.form.get('boy_year'))
        boy_month = int(request.form.get('boy_month'))
        boy_day = int(request.form.get('boy_day'))
        boy_name = request.form.get('boy_name', 'Boy')
        
        # Get girl's details
        girl_year = int(request.form.get('girl_year'))
        girl_month = int(request.form.get('girl_month'))
        girl_day = int(request.form.get('girl_day'))
        girl_name = request.form.get('girl_name', 'Girl')
        
        # Location (same for both)
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
        
        # Create date tuples
        boy_date = (boy_year, boy_month, boy_day)
        girl_date = (girl_year, girl_month, girl_day)
        
        # Perform matching
        match_result = match_dates(boy_date, girl_date, latitude, longitude)
        
        return render_template('match_result.html',
                             title='Matching Results - Cosmic Green',
                             boy_name=boy_name,
                             girl_name=girl_name,
                             match=match_result,
                             current_year=datetime.now().year)
    
    except Exception as e:
        return render_template('compatibility.html',
                             error=f"Error in matching: {str(e)}",
                             current_year=datetime.now().year)

@app.route('/predictions/<path:chart_data>')
def show_predictions(chart_data):
    """Show personalized predictions based on chart"""
    try:
        # This would normally receive chart data from session
        # For now, we'll use a placeholder
        return render_template('predictions.html',
                             title='Personal Predictions - Cosmic Green',
                             current_year=datetime.now().year)
    
    except Exception as e:
        return render_template('index.html',
                             error=f"Error generating predictions: {str(e)}",
                             current_year=datetime.now().year)

# Update the chart route to include prediction signals
@app.route('/chart', methods=['POST'])
def chart():
    """Generate and display horoscope chart with predictions"""
    try:
        # Get form data
        name = request.form.get('name', '')
        year = int(request.form.get('year'))
        month = int(request.form.get('month'))
        day = int(request.form.get('day'))
        hour = float(request.form.get('hour'))
        minute = float(request.form.get('minute', 0))
        second = float(request.form.get('second', 0))
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
        timezone = float(request.form.get('timezone', 5.5))

        # Convert to UTC
        hour_utc = hour - timezone
        hour_decimal = hour_utc + minute/60 + second/3600

        # Generate horoscope
        chart_data = vedic_horoscope(year, month, day, hour_decimal, latitude, longitude)
        
        # Generate prediction signals
        predictions = generate_prediction_signals(chart_data)
        remedies = get_remedies(predictions)

        # Store chart data in session for AI to use
        session['last_chart_data'] = chart_data
        session['last_predictions'] = predictions
        session['last_remedies'] = remedies

        return render_template('chart.html',
                             title=f'{name}\'s Chart - Cosmic Green',
                             name=name,
                             birth_details={
                                 'date': f"{day:02d}/{month:02d}/{year}",
                                 'time': f"{int(hour):02d}:{int(minute):02d}:{int(second):02d}",
                                 'timezone': f"GMT{timezone:+.1f}",
                                 'latitude': latitude,
                                 'longitude': longitude
                             },
                             chart=chart_data,
                             predictions=predictions,
                             remedies=remedies,
                             current_year=datetime.now().year)
    

    except Exception as e:
        return render_template('index.html', 
                             error=f"Error generating chart: {str(e)}",
                             current_year=datetime.now().year)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html',
                         title='About - Vedic Astrology',
                         current_year=datetime.now().year)


# Initialize AI Assistant
try:
    ai_assistant = VedicAIAssistant()
except Exception as e:
    print(f"Warning: AI Assistant not initialized - {e}")
    ai_assistant = None

# Add session configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'vedic-astro-secret-key')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Add these new routes

@app.route('/ai-chat')
def ai_chat():
    """AI Chat interface"""
    # Generate or get user session ID
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    # Get question suggestions
    suggestions = get_question_suggestions()
    
    return render_template('ai_chat.html',
                         title='AI Astrologer - Cosmic Green',
                         suggestions=suggestions,
                         current_year=datetime.now().year)

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """API endpoint for AI chat"""
    if not ai_assistant:
        return jsonify({
            'success': False,
            'error': 'AI assistant not available',
            'response': 'The AI service is currently unavailable. Please try again later.'
        }), 503
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Empty message',
                'response': 'Please ask a question.'
            }), 400
        
        # Get user ID from session
        user_id = session.get('user_id', 'anonymous')
        
        # Get chart data from session if available
        chart_data = session.get('last_chart_data')
        predictions = session.get('last_predictions')
        remedies = session.get('last_remedies')
        
        # Get AI response
        response = ai_assistant.get_response(
            user_id=user_id,
            user_message=user_message,
            chart_data=chart_data,
            predictions=predictions,
            remedies=remedies
        )
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'response': 'An error occurred while processing your question.'
        }), 500

@app.route('/api/chat/clear', methods=['POST'])
def clear_chat():
    """Clear conversation history"""
    if ai_assistant:
        user_id = session.get('user_id', 'anonymous')
        result = ai_assistant.clear_conversation(user_id)
        return jsonify(result)
    return jsonify({'success': False, 'error': 'AI assistant not available'}), 503

@app.route('/api/chat/suggestions', methods=['GET'])
def get_suggestions():
    """Get personalized question suggestions"""
    chart_data = session.get('last_chart_data')
    suggestions = get_question_suggestions(chart_data)
    return jsonify({'success': True, 'suggestions': suggestions})


@app.route('/api/horoscope', methods=['POST'])
def api_horoscope():
    """API endpoint for horoscope data"""
    try:
        data = request.get_json()
        
        year = int(data['year'])
        month = int(data['month'])
        day = int(data['day'])
        hour = float(data['hour'])
        minute = float(data.get('minute', 0))
        second = float(data.get('second', 0))
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        timezone = float(data.get('timezone', 5.5))

        hour_utc = hour - timezone
        hour_decimal = hour_utc + minute/60 + second/3600

        chart_data = vedic_horoscope(year, month, day, hour_decimal, latitude, longitude)
        
        return jsonify({'success': True, 'data': chart_data})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)