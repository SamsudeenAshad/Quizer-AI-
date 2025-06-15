#!/usr/bin/env python3
"""
Test to check AI response format for correct_answer
"""

import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("--- Testing Question Generation Format ---")
        prompt = """Create 1 multiple choice question about Python Programming at Beginner level.

Return as JSON array only, no other text:
[
  {
    "question": "Question text?",
    "options": ["A option", "B option", "C option", "D option"],
    "correct_answer": "A",
    "explanation": "Why A is correct and others are wrong"
  }
]

Make sure each question is unique and educational."""
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean the response text
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        elif response_text.startswith('```'):
            response_text = response_text.replace('```', '').strip()
        
        questions = json.loads(response_text)
        print("Raw AI Response:")
        print(json.dumps(questions, indent=2))
        
        if questions and len(questions) > 0:
            question = questions[0]
            print(f"\nCorrect Answer from AI: '{question['correct_answer']}'")
            print(f"Type: {type(question['correct_answer'])}")
            print(f"Length: {len(question['correct_answer'])}")
            
            # Test comparison
            frontend_answer = "A"  # What frontend sends
            ai_answer = question['correct_answer']
            
            print(f"\nComparison Test:")
            print(f"Frontend sends: '{frontend_answer}' (type: {type(frontend_answer)})")
            print(f"AI returns: '{ai_answer}' (type: {type(ai_answer)})")
            print(f"Equal? {frontend_answer == ai_answer}")
            print(f"Equal (case insensitive)? {frontend_answer.upper() == ai_answer.upper()}")
        
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No API key found")
