"""
AI Assistant for Vedic Astrology - Provides intelligent responses to user queries
Integrates with OpenAI's API and uses astrological data for personalized answers
"""

import openai
from datetime import datetime
import json
import os
from functools import lru_cache

class VedicAIAssistant:
    def __init__(self, api_key=None):
        """Initialize the AI assistant with OpenAI API key"""
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        openai.api_key = self.api_key
        self.conversation_history = {}
        
    def _prepare_astrology_context(self, chart_data, predictions, remedies):
        """Prepare astrological context for the AI"""
        context = f"""
ASTROLOGICAL CONTEXT:
---------------------
Birth Details:
- Ascendant: {chart_data.get('Ascendant', {}).get('sign', 'Unknown')} ({chart_data.get('Ascendant', {}).get('sign_en', 'Unknown')})
- Moon Sign: {chart_data.get('Planets', {}).get('Moon', {}).get('sign', 'Unknown')}
- Moon Nakshatra: {chart_data.get('Planets', {}).get('Moon', {}).get('nakshatra', 'Unknown')}

Planetary Positions:
"""
        # Add top 5 planets for context
        planets = chart_data.get('Planets', {})
        for planet in ['Sun', 'Moon', 'Mars', 'Jupiter', 'Saturn']:
            if planet in planets:
                pdata = planets[planet]
                context += f"- {planet}: {pdata.get('sign', 'Unknown')} ({pdata.get('degree', 0)}°), Nakshatra: {pdata.get('nakshatra', 'Unknown')}\n"
        
        context += f"""
\nPredictions Summary:
- Personality: {predictions.get('personality', {}).get('lagna_nature', 'Unknown')}
- Career Strength: {predictions.get('career', {}).get('strength', 'Unknown')}
- Relationship Focus: {predictions.get('relationships', {}).get('focus', 'Unknown')}
- Life Purpose: {predictions.get('life_purpose', 'Unknown')}

Key Strengths:
"""
        for strength in predictions.get('strengths', [])[:3]:
            context += f"- {strength}\n"
        
        return context

    def _prepare_system_prompt(self, chart_data=None, predictions=None):
        """Create system prompt for the AI"""
        base_prompt = """You are a wise Vedic astrologer AI assistant named "Cosmic Sage". You have deep knowledge of Vedic astrology, including:
- Planetary influences and their meanings
- Nakshatras and their characteristics
- Houses and their significance
- Yogas and combinations
- Remedial measures
- Spiritual guidance

Your responses should be:
1. Compassionate and wise
2. Based on Vedic astrological principles
3. Practical and actionable
4. Uplifting and encouraging
5. Culturally respectful

When answering questions:
- Connect answers to the person's chart when available
- Provide both spiritual and practical insights
- Suggest remedies when appropriate
- Keep responses meaningful but concise (3-4 paragraphs max)

Remember: You are helping people on their spiritual journey through the wisdom of Vedic astrology.
"""

        if chart_data and predictions:
            astro_context = self._prepare_astrology_context(chart_data, predictions)
            base_prompt += f"\n\n{astro_context}"
        
        return base_prompt

    def get_response(self, user_id, user_message, chart_data=None, predictions=None, remedies=None):
        """Get AI response for user query"""
        try:
            # Prepare messages
            messages = [
                {"role": "system", "content": self._prepare_system_prompt(chart_data, predictions)}
            ]
            
            # Add conversation history if exists
            if user_id in self.conversation_history:
                messages.extend(self.conversation_history[user_id][-5:])  # Last 5 messages
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Get response from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or "gpt-3.5-turbo" for lower cost
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                presence_penalty=0.3,
                frequency_penalty=0.3
            )
            
            ai_response = response.choices[0].message.content
            
            # Update conversation history
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            self.conversation_history[user_id].append({"role": "user", "content": user_message})
            self.conversation_history[user_id].append({"role": "assistant", "content": ai_response})
            
            # Keep history manageable
            if len(self.conversation_history[user_id]) > 20:
                self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
            
            return {
                "success": True,
                "response": ai_response,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, but I'm having trouble connecting to my wisdom right now. Please try again in a moment."
            }

    def clear_conversation(self, user_id):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
        return {"success": True, "message": "Conversation cleared"}

    @lru_cache(maxsize=100)
    def get_planet_meaning(self, planet):
        """Get cached meaning of a planet"""
        meanings = {
            "Sun": "Soul, ego, authority, father, vitality",
            "Moon": "Mind, emotions, mother, nurturing, public",
            "Mars": "Energy, courage, siblings, actions, aggression",
            "Mercury": "Intellect, communication, commerce, speech",
            "Jupiter": "Wisdom, knowledge, luck, spirituality, children",
            "Venus": "Love, luxury, arts, relationships, wealth",
            "Saturn": "Discipline, karma, longevity, service, delays",
            "Rahu": "Ambition, obsession, foreign, technology, illusions",
            "Ketu": "Spirituality, detachment, past life, liberation"
        }
        return meanings.get(planet, "Mystical influence")

    def get_remedy_suggestion(self, issue, chart_data=None):
        """Get AI-powered remedy suggestion for specific issues"""
        prompt = f"""Based on Vedic astrology, suggest practical remedies for: {issue}
        
        Consider:
        - Mantras and chanting
        - Gemstones (if appropriate)
        - Charity and donations
        - Rituals and practices
        - Lifestyle changes
        
        Provide 3 specific, actionable remedies."""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable Vedic astrologer providing practical remedies."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.5
            )
            return response.choices[0].message.content
        except:
            return "Please consult with a qualified astrologer for personalized remedies."

# Predefined questions for quick access
PREDEFINED_QUESTIONS = [
    "What is my life purpose based on my chart?",
    "When is the best time for career growth?",
    "How can I improve my relationships?",
    "What are my karmic lessons?",
    "Which gemstone should I wear?",
    "How can I reduce stress and anxiety?",
    "What does my 7th house say about marriage?",
    "Is this a good time to start a business?",
    "How can I strengthen my Jupiter?",
    "What remedies can help with Saturn return?"
]

def get_question_suggestions(chart_data=None):
    """Get personalized question suggestions based on chart"""
    if not chart_data:
        return PREDEFINED_QUESTIONS
    
    suggestions = []
    planets = chart_data.get('Planets', {})
    predictions = chart_data.get('predictions', {})
    
    # Personalized suggestions based on chart
    if predictions.get('career', {}).get('strength') == 'challenging':
        suggestions.append("How can I improve my career prospects?")
    
    if predictions.get('challenges', {}).get('manglik', False):
        suggestions.append("What are the effects of my Manglik dosha?")
    
    if predictions.get('relationships', {}).get('focus') == 'high':
        suggestions.append("How can I make my relationship more harmonious?")
    
    # Add planet-specific suggestions
    for planet in ['Saturn', 'Rahu', 'Ketu']:
        if planet in planets:
            suggestions.append(f"How can I balance the energy of {planet} in my life?")
    
    # Add default suggestions
    suggestions.extend([
        "What is my life purpose?",
        "Which career path suits me best?",
        "How can I improve my spiritual practice?",
        "What are my relationship strengths and challenges?"
    ])
    
    return list(set(suggestions))[:8]  # Return unique suggestions, max 8