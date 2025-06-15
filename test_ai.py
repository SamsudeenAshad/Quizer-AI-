#!/usr/bin/env python3
"""
Quick test script to verify Gemini AI integration is working
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
print(f"API Key loaded: {'Yes' if GEMINI_API_KEY else 'No'}")

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("Model configured successfully")
        
        # Test subtopics generation
        print("\n--- Testing Subtopics Generation ---")
        prompt = "Generate 5 specific subtopics for Programming at Beginner level. Return only a JSON array of strings without any additional text or formatting."
        
        response = model.generate_content(prompt)
        print(f"Response: {response.text}")
        
        # Test question generation
        print("\n--- Testing Question Generation ---")
        prompt = """Create 2 multiple choice questions about Python Programming at Beginner level.

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
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No API key found")
