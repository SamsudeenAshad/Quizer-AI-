#!/usr/bin/env python3
"""
Test to check AI response format for correct_answer with improved prompt
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

Return as JSON array only, no other text. IMPORTANT: correct_answer must be exactly "A", "B", "C", or "D":
[
  {
    "question": "Question text?",
    "options": ["Option 1 text", "Option 2 text", "Option 3 text", "Option 4 text"],
    "correct_answer": "A",
    "explanation": "Why A is correct and others are wrong"
  }
]

Rules:
- Each question must have exactly 4 options
- Options should be just the text, no letters like "A)" or "B)"
- correct_answer must be "A", "B", "C", or "D" only
- Make sure each question is unique and educational."""
        
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
            print(f"Is it A, B, C, or D? {question['correct_answer'] in ['A', 'B', 'C', 'D']}")
        
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No API key found")
