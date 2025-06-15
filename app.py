from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import google.generativeai as genai
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
print(f"Debug: GEMINI_API_KEY loaded: {'Yes' if GEMINI_API_KEY else 'No'}")
if GEMINI_API_KEY:
    print(f"Debug: API Key length: {len(GEMINI_API_KEY)}")
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("Debug: Gemini AI model configured successfully")
    except Exception as e:
        print(f"Debug: Error configuring Gemini AI: {e}")
        model = None
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")
    model = None

# Sample categories and levels
CATEGORIES = {
    'Science': ['Physics', 'Chemistry', 'Biology', 'Mathematics'],
    'Technology': ['Programming', 'AI/ML', 'Web Development', 'Cybersecurity'],
    'History': ['World History', 'Ancient Civilizations', 'Modern History', 'Wars'],
    'Literature': ['English Literature', 'World Literature', 'Poetry', 'Drama'],
    'Geography': ['Physical Geography', 'Political Geography', 'Climate', 'Countries']
}

LEVELS = ['Beginner', 'Intermediate', 'Advanced']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_categories', methods=['POST'])
def get_categories():
    title = request.json.get('title', '')
    return jsonify({
        'categories': CATEGORIES,
        'levels': LEVELS
    })

@app.route('/get_subtopics', methods=['POST'])
def get_subtopics():
    data = request.json
    category = data.get('category')
    level = data.get('level')
    
    # Generate subtopics based on category using Gemini AI
    if not model:
        return jsonify({'error': 'AI service is not available. Please check your configuration.'}), 500
        
    prompt = f"Generate 8-10 specific subtopics for {category} at {level} level. Return only a JSON array of strings without any additional text or formatting."
    
    print(f"Debug: Generating subtopics for {category} at {level} level")
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        print(f"Debug: AI Response received: {response_text[:100]}...")
        
        # Clean the response text to ensure it's valid JSON
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        elif response_text.startswith('```'):
            response_text = response_text.replace('```', '').strip()
            
        subtopics = json.loads(response_text)
        print(f"Debug: Successfully parsed {len(subtopics)} subtopics")
        
        # Validate that it's a list of strings
        if isinstance(subtopics, list) and all(isinstance(item, str) for item in subtopics):
            return jsonify({'subtopics': subtopics})
        else:
            raise ValueError("Invalid response format from AI")
            
    except Exception as e:
        print(f"Error generating subtopics: {e}")
        return jsonify({'error': f'Failed to generate subtopics: {str(e)}'}), 500

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    data = request.json
    
    try:
        # Generate questions using Gemini AI
        questions = generate_questions(data)
        
        session['quiz_config'] = {
            'title': data.get('title'),
            'category': data.get('category'),
            'level': data.get('level'),
            'subtopics': data.get('subtopics'),
            'mcq_count': data.get('mcq_count', 10),
            'current_question': 0,
            'score': 0,
            'answers': []
        }
        
        session['questions'] = questions
        
        return jsonify({'success': True, 'total_questions': len(questions)})
        
    except Exception as e:
        print(f"Error starting quiz: {e}")
        return jsonify({'error': str(e)}), 500

def generate_questions(config):
    title = config.get('title')
    category = config.get('category')
    level = config.get('level')
    subtopics = config.get('subtopics', [])
    count = config.get('mcq_count', 10)
    
    if not model:
        raise Exception("AI service is not available. Please check your configuration.")
    
    # Include subtopics in the prompt for more targeted questions
    subtopics_text = ", ".join(subtopics) if subtopics else ""
    if subtopics_text:
        prompt = f"""Create {count} multiple choice questions about {title} in {category} at {level} level.
Focus on these subtopics: {subtopics_text}

Return as JSON array only, no other text:
[
  {{
    "question": "Question text?",
    "options": ["A option", "B option", "C option", "D option"],
    "correct_answer": "A",
    "explanation": "Why A is correct and others are wrong"
  }}
]

Make sure each question is unique and educational."""
    else:
        prompt = f"""Create {count} multiple choice questions about {title} in {category} at {level} level.

Return as JSON array only, no other text:
[
  {{
    "question": "Question text?",
    "options": ["A option", "B option", "C option", "D option"],
    "correct_answer": "A",
    "explanation": "Why A is correct and others are wrong"
  }}
]

Make sure each question is unique and educational."""
    
    print(f"Debug: Generating {count} questions for {title}")
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        print(f"Debug: AI Response received: {response_text[:200]}...")
        
        # Clean the response text
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        elif response_text.startswith('```'):
            response_text = response_text.replace('```', '').strip()
        
        questions = json.loads(response_text)
        print(f"Debug: Successfully parsed {len(questions)} questions")
        
        # Validate the structure
        if isinstance(questions, list) and len(questions) > 0:
            valid_questions = []
            for q in questions:
                if (isinstance(q, dict) and 
                    'question' in q and 'options' in q and 
                    'correct_answer' in q and 'explanation' in q and
                    isinstance(q['options'], list) and len(q['options']) == 4):
                    valid_questions.append(q)
            
            if len(valid_questions) > 0:
                print(f"Debug: Returning {len(valid_questions)} valid questions")
                return valid_questions[:count]
            else:
                raise Exception("No valid questions were generated by AI")
        else:
            raise Exception("AI returned invalid question format")
                
    except Exception as e:
        print(f"Error generating questions: {e}")
        raise Exception(f"Failed to generate AI questions: {str(e)}")

@app.route('/get_question', methods=['GET'])
def get_question():
    quiz_config = session.get('quiz_config')
    questions = session.get('questions', [])
    
    if not quiz_config or not questions:
        return jsonify({'error': 'No active quiz'}), 400
    
    current_q = quiz_config['current_question']
    
    if current_q >= len(questions):
        return jsonify({'quiz_complete': True})
    
    question = questions[current_q].copy()
    # Don't send the correct answer to the frontend
    question.pop('correct_answer', None)
    question.pop('explanation', None)
    
    return jsonify({
        'question': question,
        'question_number': current_q + 1,
        'total_questions': len(questions)
    })

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    selected_answer = data.get('answer')
    
    quiz_config = session.get('quiz_config')
    questions = session.get('questions', [])
    
    if not quiz_config or not questions:
        return jsonify({'error': 'No active quiz'}), 400
    
    current_q = quiz_config['current_question']
    question = questions[current_q]
    
    is_correct = selected_answer == question['correct_answer']
    
    if is_correct:
        quiz_config['score'] += 1
    
    quiz_config['answers'].append({
        'question': question['question'],
        'selected': selected_answer,
        'correct': question['correct_answer'],
        'is_correct': is_correct
    })
    
    quiz_config['current_question'] += 1
    session['quiz_config'] = quiz_config
    
    return jsonify({
        'is_correct': is_correct,
        'explanation': question['explanation'],
        'correct_answer': question['correct_answer']
    })

@app.route('/quiz_results')
def quiz_results():
    quiz_config = session.get('quiz_config')
    if not quiz_config:
        return redirect(url_for('index'))
    
    return render_template('results.html', 
                         score=quiz_config['score'],
                         total=len(session.get('questions', [])),
                         answers=quiz_config['answers'])

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return empty response with "No Content" status

if __name__ == '__main__':
    app.run(debug=True)
