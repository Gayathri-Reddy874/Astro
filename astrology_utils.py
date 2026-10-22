"""
Astrology Utilities for Vedic Compatibility and Predictions
Contains functions for Kundali matching (Guna Milan) and personalized predictions
"""

import swisseph as swe

# Nakshatras list
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

# Nakshatra lords (for reference)
NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter",
    "Saturn", "Mercury", "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun",
    "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]

# Rashi lords
RASHI_LORD = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"
]

# Planet friendship
FRIENDS = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"]
}

# Neutral planets
NEUTRAL = {
    "Sun": ["Mercury"],
    "Moon": ["Mars", "Jupiter", "Venus", "Saturn"],
    "Mars": ["Mercury", "Venus", "Saturn"],
    "Mercury": ["Mars", "Jupiter", "Saturn"],
    "Jupiter": ["Mercury", "Venus", "Saturn"],
    "Venus": ["Sun", "Moon", "Jupiter"],
    "Saturn": ["Sun", "Moon", "Mars"]
}

# Enemies
ENEMIES = {
    "Sun": ["Venus", "Saturn"],
    "Moon": ["Rahu", "Ketu"],
    "Mars": ["Rahu", "Ketu"],
    "Mercury": ["Moon"],
    "Jupiter": ["Mercury", "Venus"],
    "Venus": ["Mars", "Jupiter"],
    "Saturn": ["Jupiter", "Venus"]
}

# Gana groups
GANA = [
    "Deva", "Manushya", "Rakshasa", "Manushya", "Deva", "Manushya",
    "Deva", "Deva", "Rakshasa", "Rakshasa", "Manushya", "Manushya",
    "Deva", "Rakshasa", "Deva", "Rakshasa", "Deva", "Rakshasa",
    "Rakshasa", "Manushya", "Manushya", "Deva", "Rakshasa",
    "Rakshasa", "Manushya", "Manushya", "Deva"
]

# Yoni animals with compatibility
YONI = [
    "Horse", "Elephant", "Sheep", "Serpent", "Serpent", "Dog",
    "Cat", "Sheep", "Cat", "Rat", "Rat", "Cow", "Buffalo",
    "Tiger", "Buffalo", "Tiger", "Deer", "Deer", "Dog",
    "Monkey", "Monkey", "Lion", "Horse", "Lion", "Cow",
    "Elephant", "Lion"
]

# Yoni compatibility matrix (simplified)
YONI_COMPATIBLE = {
    "Horse": ["Horse", "Buffalo"],
    "Elephant": ["Elephant", "Lion"],
    "Sheep": ["Sheep", "Deer"],
    "Serpent": ["Serpent"],
    "Dog": ["Dog", "Tiger"],
    "Cat": ["Cat"],
    "Rat": ["Rat", "Cow"],
    "Cow": ["Cow", "Rat", "Buffalo"],
    "Buffalo": ["Buffalo", "Cow", "Horse"],
    "Tiger": ["Tiger", "Dog"],
    "Deer": ["Deer", "Sheep"],
    "Monkey": ["Monkey"],
    "Lion": ["Lion", "Elephant"]
}

# Nadi groups
NADI = ["Adi", "Madhya", "Antya"] * 9

# Varna by rashi
VARNA = ["Brahmin", "Kshatriya", "Vaishya", "Shudra"] * 3

# Varna order for compatibility
VARNA_ORDER = {
    "Brahmin": 1,
    "Kshatriya": 2,
    "Vaishya": 3,
    "Shudra": 4
}

# Bhakoot incompatible pairs
BHAKOOT_BAD = [2, 6, 8, 12]  # Differences that are incompatible

# Tara good stars
TARA_GOOD = [0, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25]

def moon_data(year, month, day):
    """Calculate Moon's nakshatra and rashi for a given date"""
    jd = swe.julday(year, month, day, 12)
    moon = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
    
    nak = int(moon / (360/27))
    rashi = int(moon / 30)
    
    return nak, rashi

def get_nakshatra_details(nak_index):
    """Get detailed information about a nakshatra"""
    return {
        "name": NAKSHATRAS[nak_index],
        "lord": NAKSHATRA_LORDS[nak_index],
        "gana": GANA[nak_index],
        "yoni": YONI[nak_index],
        "nadi": NADI[nak_index % 3]
    }

def varna_koota(boy_rashi, girl_rashi):
    """Varna Koota - 1 point for higher or equal varna"""
    boy_varna = VARNA[boy_rashi]
    girl_varna = VARNA[girl_rashi]
    
    if VARNA_ORDER[boy_varna] >= VARNA_ORDER[girl_varna]:
        return 1
    return 0

def vashya_koota(boy_rashi, girl_rashi):
    """Vashya Koota - 2 points for compatibility"""
    # Simplified - full implementation would check mutual vashya
    # Common compatible pairs
    compatible_pairs = [
        (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11),
        # Add more compatible cross pairs here
    ]
    
    if (boy_rashi, girl_rashi) in compatible_pairs or (girl_rashi, boy_rashi) in compatible_pairs:
        return 2
    return 1

def tara_koota(boy_nak, girl_nak):
    """Tara Koota - 3 points for good star compatibility"""
    diff = (girl_nak - boy_nak) % 27
    
    if diff in TARA_GOOD:
        return 3
    return 0

def yoni_koota(boy_nak, girl_nak):
    """Yoni Koota - 4 points for same or compatible yoni"""
    boy_yoni = YONI[boy_nak]
    girl_yoni = YONI[girl_nak]
    
    if boy_yoni == girl_yoni:
        return 4
    elif girl_yoni in YONI_COMPATIBLE.get(boy_yoni, []):
        return 3
    elif boy_yoni in YONI_COMPATIBLE.get(girl_yoni, []):
        return 3
    else:
        return 0

def graha_maitri(boy_rashi, girl_rashi):
    """Graha Maitri - 5 points for planetary friendship"""
    b_lord = RASHI_LORD[boy_rashi]
    g_lord = RASHI_LORD[girl_rashi]
    
    if b_lord == g_lord:
        return 5
    elif g_lord in FRIENDS.get(b_lord, []):
        return 5
    elif g_lord in NEUTRAL.get(b_lord, []):
        return 3
    else:
        return 1

def gana_koota(boy_nak, girl_nak):
    """Gana Koota - 6 points for same gana"""
    boy_gana = GANA[boy_nak]
    girl_gana = GANA[girl_nak]
    
    if boy_gana == girl_gana:
        return 6
    
    # Rakshasa with Deva/Manushya gives 1 point
    if "Rakshasa" in (boy_gana, girl_gana):
        return 1
    
    # Deva-Manushya gives 5 points
    return 5

def bhakoot_koota(boy_rashi, girl_rashi):
    """Bhakoot Koota - 7 points for compatible rashis"""
    diff = abs(boy_rashi - girl_rashi)
    
    if diff in BHAKOOT_BAD:
        return 0
    return 7

def nadi_koota(boy_nak, girl_nak):
    """Nadi Koota - 8 points for different nadi"""
    boy_nadi = NADI[boy_nak % 3]
    girl_nadi = NADI[girl_nak % 3]
    
    if boy_nadi != girl_nadi:
        return 8
    return 0

def manglik_check(year, month, day, lat, lon, hour=12):
    """Check if a person is manglik based on Mars position"""
    jd = swe.julday(year, month, day, hour)
    
    mars_lon = swe.calc_ut(jd, swe.MARS, swe.FLG_SIDEREAL)[0][0]
    houses = swe.houses(jd, lat, lon)
    cusps = houses[0]
    
    # Find which house Mars is in
    house = 1
    for i in range(12):
        start = cusps[i]
        end = cusps[(i+1) % 12]
        
        if start < end:
            if start <= mars_lon < end:
                house = i + 1
                break
        else:
            if mars_lon >= start or mars_lon < end:
                house = i + 1
                break
    
    # Manglik houses: 1, 2, 4, 7, 8, 12
    manglik = house in [1, 2, 4, 7, 8, 12]
    
    return manglik, house

def match_dates(boy_date, girl_date, lat, lon):
    """
    Perform Kundali matching (Guna Milan) between two dates
    
    Parameters:
    boy_date: tuple (year, month, day)
    girl_date: tuple (year, month, day)
    lat, lon: location coordinates
    
    Returns:
    Dictionary with compatibility scores
    """
    by, bm, bd = boy_date
    gy, gm, gd = girl_date
    
    # Get nakshatra and rashi for both
    boy_nak, boy_rashi = moon_data(by, bm, bd)
    girl_nak, girl_rashi = moon_data(gy, gm, gd)
    
    # Get nakshatra details
    boy_nak_details = get_nakshatra_details(boy_nak)
    girl_nak_details = get_nakshatra_details(girl_nak)
    
    # Calculate all kootas
    scores = {}
    
    scores["Varna"] = varna_koota(boy_rashi, girl_rashi)
    scores["Vashya"] = vashya_koota(boy_rashi, girl_rashi)
    scores["Tara"] = tara_koota(boy_nak, girl_nak)
    scores["Yoni"] = yoni_koota(boy_nak, girl_nak)
    scores["Graha Maitri"] = graha_maitri(boy_rashi, girl_rashi)
    scores["Gana"] = gana_koota(boy_nak, girl_nak)
    scores["Bhakoot"] = bhakoot_koota(boy_rashi, girl_rashi)
    scores["Nadi"] = nadi_koota(boy_nak, girl_nak)
    
    # Calculate total (maximum 36)
    total = sum(scores.values())
    
    # Manglik check
    boy_manglik, boy_house = manglik_check(by, bm, bd, lat, lon)
    girl_manglik, girl_house = manglik_check(gy, gm, gd, lat, lon)
    
    # Determine compatibility level
    if total >= 32:
        compatibility = "Excellent"
    elif total >= 28:
        compatibility = "Very Good"
    elif total >= 24:
        compatibility = "Good"
    elif total >= 18:
        compatibility = "Average"
    elif total >= 12:
        compatibility = "Below Average"
    else:
        compatibility = "Not Recommended"
    
    # Build result
    result = {
        "scores": scores,
        "total": total,
        "max_score": 36,
        "compatibility": compatibility,
        "boy": {
            "nakshatra": boy_nak_details["name"],
            "nakshatra_index": boy_nak,
            "nakshatra_lord": boy_nak_details["lord"],
            "rashi": boy_rashi,
            "gana": boy_nak_details["gana"],
            "yoni": boy_nak_details["yoni"],
            "nadi": boy_nak_details["nadi"],
            "manglik": boy_manglik,
            "manglik_house": boy_house
        },
        "girl": {
            "nakshatra": girl_nak_details["name"],
            "nakshatra_index": girl_nak,
            "nakshatra_lord": girl_nak_details["lord"],
            "rashi": girl_rashi,
            "gana": girl_nak_details["gana"],
            "yoni": girl_nak_details["yoni"],
            "nadi": girl_nak_details["nadi"],
            "manglik": girl_manglik,
            "manglik_house": girl_house
        }
    }
    
    # Add manglik dosha info
    if boy_manglik != girl_manglik:
        result["manglik_dosha"] = "Present - One partner is manglik while the other is not"
        result["manglik_remedy"] = "Consider performing manglik shanti puja or matching with another manglik"
    else:
        result["manglik_dosha"] = "Cancelled - Both partners have similar manglik status"
    
    return result

def generate_prediction_signals(chart):
    """
    Generate personalized prediction signals from a birth chart
    
    Parameters:
    chart: Dictionary containing complete horoscope data
    
    Returns:
    Dictionary with various prediction signals
    """
    planets = chart["Planets"]
    houses = chart["Houses"]
    ascendant = chart["Ascendant"]
    
    # Find house of each planet
    planet_house = {}
    planet_sign = {}
    
    for planet, pdata in planets.items():
        sign = pdata["sign"]
        planet_sign[planet] = sign
        
        # Find which house this sign falls in
        for h, hdata in houses.items():
            if hdata["sign"] == sign:
                planet_house[planet] = int(h.split()[1])
                break
    
    # Get house numbers for key planets
    sun_house = planet_house.get("Sun", 0)
    moon_house = planet_house.get("Moon", 0)
    mars_house = planet_house.get("Mars", 0)
    mercury_house = planet_house.get("Mercury", 0)
    jupiter_house = planet_house.get("Jupiter", 0)
    venus_house = planet_house.get("Venus", 0)
    saturn_house = planet_house.get("Saturn", 0)
    rahu_house = planet_house.get("Rahu", 0)
    ketu_house = planet_house.get("Ketu", 0)
    
    # Signals dictionary
    signals = {
        "core_identity": {},
        "personality": {},
        "career": {},
        "relationships": {},
        "spiritual": {},
        "health": {},
        "challenges": {},
        "strengths": []
    }
    
    # Core Identity
    signals["core_identity"]["ascendant"] = ascendant["sign"]
    signals["core_identity"]["ascendant_en"] = ascendant["sign_en"]
    signals["core_identity"]["moon_sign"] = planets["Moon"]["sign"]
    signals["core_identity"]["moon_nakshatra"] = planets["Moon"]["nakshatra"]
    
    # Personality based on Lagna (Ascendant)
    lagna_type = {
        "Mesha": "dynamic and pioneering",
        "Vrishabha": "stable and sensual",
        "Mithuna": "communicative and adaptable",
        "Karka": "emotional and nurturing",
        "Simha": "confident and creative",
        "Kanya": "analytical and practical",
        "Tula": "diplomatic and balanced",
        "Vrischika": "intense and transformative",
        "Dhanu": "optimistic and philosophical",
        "Makara": "ambitious and disciplined",
        "Kumbha": "innovative and humanitarian",
        "Meena": "compassionate and intuitive"
    }
    
    signals["personality"]["lagna_nature"] = lagna_type.get(ascendant["sign"], "unique")
    
    # Moon sign influence
    moon_influence = {
        "Mesha": "quick emotions",
        "Vrishabha": "stable emotions",
        "Mithuna": "changeable emotions",
        "Karka": "deep emotions",
        "Simha": "dramatic emotions",
        "Kanya": "analytical emotions",
        "Tula": "balanced emotions",
        "Vrischika": "intense emotions",
        "Dhanu": "optimistic emotions",
        "Makara": "cautious emotions",
        "Kumbha": "detached emotions",
        "Meena": "compassionate emotions"
    }
    
    signals["personality"]["emotional_nature"] = moon_influence.get(planets["Moon"]["sign"], "balanced")
    
    # Career indicators
    signals["career"]["strength"] = "moderate"
    if jupiter_house in [1, 2, 5, 9, 10, 11]:
        signals["career"]["strength"] = "high"
        signals["strengths"].append("Strong Jupiter placement indicates career success")
    
    if sun_house in [10]:
        signals["career"]["leadership"] = True
        signals["strengths"].append("Sun in 10th house - natural leadership abilities")
    
    if mercury_house in [3, 6, 10]:
        signals["career"]["communication"] = True
        signals["strengths"].append("Strong Mercury - excellent communication skills")
    
    # Career fields based on planetary placements
    career_fields = []
    if sun_house in [1, 5, 9]:
        career_fields.append("Government/Leadership")
    if moon_house in [4, 7]:
        career_fields.append("Public relations/Counseling")
    if mars_house in [3, 6, 10]:
        career_fields.append("Engineering/Military/Sports")
    if mercury_house in [3, 6]:
        career_fields.append("Writing/Teaching/Business")
    if jupiter_house in [5, 9]:
        career_fields.append("Teaching/Law/Spiritual")
    if venus_house in [7, 11]:
        career_fields.append("Arts/Creative/Finance")
    if saturn_house in [10]:
        career_fields.append("Management/Administration")
    
    signals["career"]["suggested_fields"] = career_fields[:3]  # Top 3
    
    # Relationship indicators
    signals["relationships"]["focus"] = "moderate"
    if venus_house == 7:
        signals["relationships"]["focus"] = "high"
        signals["strengths"].append("Venus in 7th house - strong relationship potential")
    
    if venus_house in [1, 2, 3, 4, 5]:
        signals["relationships"]["early_marriage"] = True
    
    if saturn_house == 7:
        signals["relationships"]["delayed_marriage"] = True
        signals["relationships"]["focus"] = "delayed but stable"
    
    # Multiple marriages indicator
    if jupiter_house == 7 and venus_house in [2, 7]:
        signals["relationships"]["multiple_marriages"] = "possible"
    
    # Spiritual growth
    signals["spiritual"]["growth"] = False
    if jupiter_house == 9:
        signals["spiritual"]["growth"] = True
        signals["strengths"].append("Jupiter in 9th house - strong spiritual inclination")
    
    if ketu_house in [9, 12]:
        signals["spiritual"]["past_life"] = True
        signals["strengths"].append("Ketu in spiritual houses - past life spiritual practices")
    
    if rahu_house in [8, 12]:
        signals["spiritual"]["intense_quest"] = True
    
    # Health indicators
    signals["health"]["focus_areas"] = []
    
    # Sun health
    if sun_house in [6, 8, 12]:
        signals["health"]["focus_areas"].append("Heart/Circulation")
    
    # Moon health
    if moon_house in [6, 8]:
        signals["health"]["focus_areas"].append("Mind/Emotions")
    
    # Mars health
    if mars_house in [6, 8]:
        signals["health"]["focus_areas"].append("Blood/Energy")
    
    # Saturn health
    if saturn_house in [6, 8]:
        signals["health"]["focus_areas"].append("Bones/Joints")
    
    if not signals["health"]["focus_areas"]:
        signals["health"]["focus_areas"] = ["General wellness"]
    
    # Life challenges
    signals["challenges"]["areas"] = []
    
    if saturn_house == 1:
        signals["challenges"]["areas"].append("Self-discipline and responsibility")
    
    if saturn_house == 8:
        signals["challenges"]["areas"].append("Transformational challenges")
    
    if rahu_house == 8:
        signals["challenges"]["areas"].append("Sudden changes and mysteries")
    
    if ketu_house == 8:
        signals["challenges"]["areas"].append("Letting go of attachments")
    
    if mars_house == 8:
        signals["challenges"]["areas"].append("Managing anger and intensity")
    
    # Manglik status
    signals["challenges"]["manglik"] = mars_house in [1, 2, 4, 7, 8, 12]
    
    if signals["challenges"]["manglik"]:
        signals["challenges"]["manglik_house"] = mars_house
    
    # Lucky areas
    lucky_houses = []
    if jupiter_house:
        lucky_houses.append(f"House {jupiter_house} (Jupiter)")
    if venus_house:
        lucky_houses.append(f"House {venus_house} (Venus)")
    
    signals["strengths"].append(f"Lucky areas: {', '.join(lucky_houses)}")
    
    # Life purpose
    purpose_indicators = []
    
    if sun_house in [1, 5, 9]:
        purpose_indicators.append("Self-expression and leadership")
    if moon_house in [4, 7]:
        purpose_indicators.append("Nurturing and connecting with others")
    if jupiter_house in [9, 12]:
        purpose_indicators.append("Wisdom and spiritual growth")
    if saturn_house in [10]:
        purpose_indicators.append("Career achievement and discipline")
    if rahu_house in [11]:
        purpose_indicators.append("Material success and innovation")
    
    if purpose_indicators:
        signals["life_purpose"] = purpose_indicators[0]
    else:
        signals["life_purpose"] = "Balanced personal development"
    
    return signals

def get_remedies(signals):
    """
    Suggest remedies based on prediction signals
    """
    remedies = []
    
    # Manglik remedies
    if signals["challenges"].get("manglik", False):
        remedies.append({
            "type": "Manglik Dosha",
            "remedy": "Perform Hanuman Chalisa on Tuesdays, donate red items"
        })
    
    # Saturn challenges
    if "Self-discipline" in str(signals["challenges"]["areas"]):
        remedies.append({
            "type": "Saturn",
            "remedy": "Serve elders, donate black items on Saturdays"
        })
    
    # Rahu challenges
    if "Sudden changes" in str(signals["challenges"]["areas"]):
        remedies.append({
            "type": "Rahu",
            "remedy": "Feed dogs, donate blankets, chant Rahu mantra"
        })
    
    # Ketu challenges
    if "Letting go" in str(signals["challenges"]["areas"]):
        remedies.append({
            "type": "Ketu",
            "remedy": "Spiritual practices, meditation, donate white items"
        })
    
    # Health remedies based on focus areas
    for area in signals["health"]["focus_areas"]:
        if "Heart" in area:
            remedies.append({
                "type": "Heart Health",
                "remedy": "Sun salutations, copper water, respect father/father figures"
            })
        if "Mind" in area:
            remedies.append({
                "type": "Mental Peace",
                "remedy": "Meditation, moon-related practices, cool foods"
            })
    
    # General remedies
    if not remedies:
        remedies.append({
            "type": "General",
            "remedy": "Regular worship, charity, and positive thinking"
        })
    
    return remedies
