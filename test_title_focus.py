#!/usr/bin/env python3
"""
Test the updated prompt to see how it handles title vs category
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
        
        print("--- Testing Title-Focused Prompt ---")
        title = "JavaScript Arrow Functions"
        category = "Technology"
        level = "Intermediate"
        count = 2
        
        prompt = f"""Create {count} multiple choice questions about "{title}" at {level} level.
Consider the category "{category}" for context and difficulty.

Return as JSON array only, no other text. IMPORTANT: correct_answer must be exactly "A", "B", "C", or "D":
[
  {{
    "question": "Question text?",
    "options": ["Option 1 text", "Option 2 text", "Option 3 text", "Option 4 text"],
    "correct_answer": "A",
    "explanation": "Why A is correct and others are wrong"
  }}
]

Rules:
- Each question must have exactly 4 options
- Options should be just the text, no letters like "A)" or "B)"
- correct_answer must be "A", "B", "C", or "D" only
- Primary focus should be on the topic "{title}"
- Use the category "{category}" and level "{level}" as guidance for difficulty and context
- Make sure each question is unique and educational."""
        
        print(f"Topic: {title}")
        print(f"Category: {category}")
        print(f"Level: {level}")
        print()
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean the response text
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        elif response_text.startswith('```'):
            response_text = response_text.replace('```', '').strip()
        
        questions = json.loads(response_text)
        
        for i, question in enumerate(questions, 1):
            print(f"Question {i}: {question['question']}")
            print(f"Correct Answer: {question['correct_answer']}")
            print()
        
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No API key found")
