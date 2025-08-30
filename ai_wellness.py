import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import random

load_dotenv()

class GeminiWellnessAI:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_wellness_plan(self, user_data, feelings_description=""):
        """Generate personalized wellness plan using Gemini AI"""
        
        age = user_data.get('age', 'Not specified')
        fitness_level = user_data.get('fitness_level', 'Not specified')
        health_goals = user_data.get('health_goals', 'Not specified')
        mood_score = user_data.get('mood_score', 5)
        stress_level = user_data.get('stress_level', 5)
        energy_level = user_data.get('energy_level', 5)
        
        prompt = f'''You are an advanced AI wellness coach from the year 2070 with access to cutting-edge health technology.
Create a personalized wellness plan based on the following user data:

USER PROFILE:
- Age: {age}
- Fitness Level: {fitness_level}
- Health Goals: {health_goals}

CURRENT STATE:
- Mood Score: {mood_score}/10
- Stress Level: {stress_level}/10
- Energy Level: {energy_level}/10

DETAILED FEELINGS DESCRIPTION:
"{feelings_description}"

Based on this information, create a comprehensive wellness plan with futuristic 2070 technology elements.
Please respond with ONLY a JSON object in this exact format:

{{
    "mental_health": [
        "specific mental health recommendation 1",
        "specific mental health recommendation 2",
        "specific mental health recommendation 3"
    ],
    "fitness": [
        "specific fitness recommendation 1",
        "specific fitness recommendation 2", 
        "specific fitness recommendation 3"
    ],
    "nutrition": [
        "specific nutrition recommendation 1",
        "specific nutrition recommendation 2",
        "specific nutrition recommendation 3"
    ],
    "personalized_insights": "A paragraph with personalized insights based on their feelings and current state",
    "motivation_message": "An encouraging message tailored to their situation"
}}

Include futuristic elements like neural-feedback systems, holographic trainers, AI-powered biometric monitoring, quantum wellness optimization, smart molecular nutrition, VR/AR therapy environments, and brain-computer interfaces for wellness.'''

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up the response text
            if 'json' in response_text.lower():
                lines = response_text.split('\n')
                json_lines = []
                inside_json = False
                
                for line in lines:
                    if '{' in line:
                        inside_json = True
                    if inside_json:
                        json_lines.append(line)
                    if '}' in line and inside_json:
                        break
                
                response_text = '\n'.join(json_lines)
            
            # Find JSON object
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_text = response_text[start_idx:end_idx]
                plan = json.loads(json_text)
                return plan
            else:
                return self._get_fallback_plan(user_data, feelings_description)
            
        except Exception as e:
            print(f"Gemini AI Error: {e}")
            return self._get_fallback_plan(user_data, feelings_description)
    
    def analyze_feelings(self, feelings_text):
        """Analyze user's feelings description and provide insights"""
        
        prompt = f'''As an advanced AI emotional wellness analyzer from 2070, analyze these feelings and provide insights:

USER FEELINGS: "{feelings_text}"

Please respond with ONLY a JSON object in this format:
{{
    "emotional_state": "primary emotion detected",
    "stress_indicators": ["indicator1", "indicator2"],
    "recommended_focus_areas": ["area1", "area2", "area3"],
    "empathy_message": "An empathetic response to their feelings"
}}'''
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up the response
            if 'json' in response_text.lower():
                lines = response_text.split('\n')
                json_lines = []
                inside_json = False
                
                for line in lines:
                    if '{' in line:
                        inside_json = True
                    if inside_json:
                        json_lines.append(line)
                    if '}' in line and inside_json:
                        break
                
                response_text = '\n'.join(json_lines)
            
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_text = response_text[start_idx:end_idx]
                return json.loads(json_text)
            else:
                return self._get_fallback_feelings_analysis()
            
        except Exception as e:
            print(f"Feelings analysis error: {e}")
            return self._get_fallback_feelings_analysis()
    
    def _get_fallback_feelings_analysis(self):
        """Fallback feelings analysis if AI fails"""
        return {
            "emotional_state": "complex emotions detected",
            "stress_indicators": ["Multiple stressors identified", "Emotional processing needed"],
            "recommended_focus_areas": ["Mental wellness", "Stress management", "Self-care"],
            "empathy_message": "I understand you're going through something challenging. Let's work together to improve your wellness step by step."
        }
    
    def _get_fallback_plan(self, user_data, feelings_description):
        """Enhanced fallback wellness plan if AI fails"""
        
        mood_score = user_data.get('mood_score', 5)
        stress_level = user_data.get('stress_level', 5)
        energy_level = user_data.get('energy_level', 5)
        
        # Mental health based on stress and mood
        if stress_level >= 7:
            mental_health = [
                "Daily neural-feedback meditation with VR forest environment",
                "AI-guided deep breathing exercises with biometric monitoring", 
                "Virtual therapy sessions with holographic wellness counselor"
            ]
        elif mood_score <= 4:
            mental_health = [
                "Mood-enhancing light therapy with circadian rhythm optimization",
                "AI-powered journaling with sentiment analysis feedback",
                "Brain-wave entrainment sessions for emotional balance"
            ]
        else:
            mental_health = [
                "Daily mindfulness practice with augmented reality guides",
                "Neural interface meditation for optimal brain-wave patterns",
                "Personalized affirmation therapy via AI voice synthesis"
            ]
        
        # Fitness based on energy level
        if energy_level <= 3:
            fitness = [
                "Gentle movement therapy with robotic assistance",
                "Energy-building exercises with real-time biometric feedback",
                "Restorative yoga with holographic instructor adaptation"
            ]
        elif energy_level >= 8:
            fitness = [
                "High-intensity quantum-enhanced training protocols",
                "Advanced biometric optimization with AI form correction",
                "Competitive VR fitness challenges with neural reward systems"
            ]
        else:
            fitness = [
                "Personalized workout routines with holographic personal trainer",
                "Smart recovery protocols using nanotechnology sensors",
                "Mixed-reality fitness games for sustained motivation"
            ]
        
        # Nutrition based on overall wellness needs
        if stress_level >= 6:
            nutrition = [
                "Stress-reducing adaptogenic meal plans via molecular gastronomy",
                "Real-time cortisol monitoring with smart nutrition adjustments",
                "AI-optimized gut microbiome restoration protocols"
            ]
        else:
            nutrition = [
                "Personalized meal optimization based on genetic markers",
                "Smart hydration monitoring with electrolyte balance tracking", 
                "3D-printed custom supplements delivered via drone network"
            ]
        
        # Generate personalized insights
        insights = f"Based on your mood score of {mood_score}/10, stress level of {stress_level}/10, and energy level of {energy_level}/10, "
        
        if feelings_description:
            insights += "along with your personal feelings description, our advanced AI has detected patterns that suggest focusing on "
            if stress_level >= 6:
                insights += "stress management and emotional regulation. "
            elif energy_level <= 4:
                insights += "energy restoration and gentle activation. "
            else:
                insights += "maintaining balance while optimizing your wellness journey. "
        else:
            insights += "our 2070 wellness algorithms recommend a balanced approach to your mental, physical, and nutritional needs. "
        
        insights += "Your plan adapts in real-time based on your biometric feedback and neural patterns."
        
        # Generate motivation message
        motivation_messages = [
            "Your wellness journey is unique, and our quantum-enhanced AI is here to support every step forward!",
            "Every day is an opportunity to optimize your well-being with cutting-edge 2070 technology at your service.",
            "Your commitment to wellness activates our most advanced algorithms - together we'll achieve optimal health!",
            "Neural patterns show great potential for growth - let's unlock your wellness achievements together!"
        ]
        
        motivation = random.choice(motivation_messages)
        
        return {
            "mental_health": mental_health,
            "fitness": fitness,
            "nutrition": nutrition,
            "personalized_insights": insights,
            "motivation_message": motivation
        }
