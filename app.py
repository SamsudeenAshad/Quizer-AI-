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
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
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
    prompt = f"Generate 8-10 specific subtopics for {category} at {level} level. Return only a JSON array of strings."
    
    try:
        response = model.generate_content(prompt)
        subtopics = json.loads(response.text)
    except:
        # Fallback subtopics if AI fails
        subtopics = [
            f"{category} Basics",
            f"{category} Fundamentals",
            f"{category} Concepts",
            f"{category} Applications",
            f"{category} Theory"
        ]
    
    return jsonify({'subtopics': subtopics})

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    data = request.json
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
    
    # Generate questions using Gemini AI
    questions = generate_questions(data)
    session['questions'] = questions
    
    return jsonify({'success': True, 'total_questions': len(questions)})

def generate_questions(config):
    title = config.get('title')
    category = config.get('category')
    level = config.get('level')
    subtopics = config.get('subtopics', [])
    count = config.get('mcq_count', 10)
    
    subtopics_str = ', '.join(subtopics)
    
    prompt = f"""
    Generate {count} multiple choice questions about {title} in the {category} category at {level} level.
    Focus on these subtopics: {subtopics_str}
    
    Return a JSON array where each question object has:
    - question: the question text
    - options: array of 4 options (A, B, C, D)
    - correct_answer: the correct option letter (A, B, C, or D)
    - explanation: detailed explanation of why the answer is correct
    
    Make sure questions are varied and cover different subtopics.
    """
    
    try:
        response = model.generate_content(prompt)
        questions = json.loads(response.text)
    except Exception as e:
        # Fallback questions if AI fails
        questions = [
            {
                "question": f"Sample question about {title}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "A",
                "explanation": "This is a sample explanation."
            }
        ]
    
    return questions

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

if __name__ == '__main__':
    app.run(debug=True)
