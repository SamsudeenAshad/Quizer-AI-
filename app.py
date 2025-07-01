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
    'Geography': ['Physical Geography', 'Political Geography', 'Climate', 'Countries'],
    'Other': ['other topics', 'Miscellaneous', 'General Knowledge', 'Current Events']
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
        raise Exception("AI service is not available. Please check your configuration.")    # Include subtopics in the prompt for more targeted questions
    subtopics_text = ", ".join(subtopics) if subtopics else ""
    if subtopics_text:
        prompt = f"""Create {count} multiple choice questions about "{title}" at {level} level.
Consider the category "{category}" and focus on these subtopics: {subtopics_text}

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
    else:
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
                    
                    # Fix correct_answer if it's not A, B, C, D
                    correct_answer = q['correct_answer'].strip()
                    if correct_answer not in ['A', 'B', 'C', 'D']:
                        # Find which option matches the correct answer text
                        for i, option in enumerate(q['options']):
                            if option.strip().lower() == correct_answer.lower():
                                q['correct_answer'] = chr(65 + i)  # Convert to A, B, C, D
                                print(f"Debug: Fixed question - converted '{correct_answer}' to '{q['correct_answer']}'")
                                break
                        else:
                            # If no exact match, try partial matching
                            for i, option in enumerate(q['options']):
                                if correct_answer.lower() in option.strip().lower():
                                    q['correct_answer'] = chr(65 + i)
                                    print(f"Debug: Partial fix - converted '{correct_answer}' to '{q['correct_answer']}'")
                                    break
                            else:
                                # Skip this question if we can't fix it
                                print(f"Debug: Skipping invalid question - can't match '{correct_answer}' to options: {q['options']}")
                                continue
                    
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
    
    # Debug logging for answer validation
    print(f"Debug: Question: {question['question'][:50]}...")
    print(f"Debug: Options: {question['options']}")
    print(f"Debug: AI correct_answer: '{question['correct_answer']}'")
    print(f"Debug: User selected: '{selected_answer}'")
      # Check if AI returned the option text instead of letter
    correct_answer = question['correct_answer'].strip()
    
    # If the correct answer is not A, B, C, or D, try to find the matching option
    if correct_answer not in ['A', 'B', 'C', 'D']:
        # Find which option matches the correct answer text
        for i, option in enumerate(question['options']):
            if option.strip().lower() == correct_answer.lower():
                correct_answer = chr(65 + i)  # Convert index to A, B, C, D
                print(f"Debug: Converted correct answer from '{question['correct_answer']}' to '{correct_answer}'")
                break
        else:
            # If no exact match, try partial matching
            for i, option in enumerate(question['options']):
                if correct_answer.lower() in option.strip().lower() or option.strip().lower() in correct_answer.lower():
                    correct_answer = chr(65 + i)
                    print(f"Debug: Partial match - converted correct answer to '{correct_answer}'")
                    break
            else:
                # If still no match, default to A and log the issue
                print(f"Debug: WARNING - Could not match '{question['correct_answer']}' to any option. Defaulting to A.")
                print(f"Debug: Available options: {question['options']}")
                correct_answer = 'A'
    
    is_correct = selected_answer == correct_answer
    
    print(f"Debug: Final comparison - User: '{selected_answer}' vs Correct: '{correct_answer}' = {is_correct}")
    
    if is_correct:
        quiz_config['score'] += 1
    
    quiz_config['answers'].append({
        'question': question['question'],
        'selected': selected_answer,
        'correct': correct_answer,  # Store the normalized correct answer
        'is_correct': is_correct
    })
    
    quiz_config['current_question'] += 1
    session['quiz_config'] = quiz_config
    
    return jsonify({
        'is_correct': is_correct,
        'explanation': question['explanation'],
        'correct_answer': correct_answer  # Return the normalized correct answer
    })

@app.route('/quiz_results')
def quiz_results():
    quiz_config = session.get('quiz_config')
    if not quiz_config:
        return redirect(url_for('index'))
    
    # Get data with defaults to prevent errors
    score = quiz_config.get('score', 0)
    questions = session.get('questions', [])
    total = len(questions)
    answers = quiz_config.get('answers', [])
    
    # Ensure we have valid data
    if total == 0:
        return redirect(url_for('index'))
    
    return render_template('results.html', 
                         score=score,
                         total=total,
                         answers=answers)

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return empty response with "No Content" status

if __name__ == '__main__':
    app.run(debug=True)
