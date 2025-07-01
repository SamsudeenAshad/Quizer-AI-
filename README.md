# 🧠 Quizer AI - Intelligent Quiz Generation Platform

**Quizer AI** is a modern, AI-powered Flask web application that creates personalized quizzes using Google's Gemini AI. The platform offers an intuitive step-by-step quiz creation process with real-time feedback and detailed explanations.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Gemini AI](https://img.shields.io/badge/Gemini%20AI-Powered-orange.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

## ✨ Features

### 🎯 **Smart Quiz Creation**
- **4-Step Process**: Title → Category & Level → Subtopics → Quiz Settings
- **AI-Generated Subtopics**: Dynamic subtopic suggestions based on your selections
- **Customizable Length**: Choose from 5, 10, 15, or 20 questions
- **Multiple Categories**: Science, Technology, History, Literature, Geography
- **Difficulty Levels**: Beginner, Intermediate, Advanced

### 🤖 **AI-Powered Content**
- **Google Gemini Integration**: Uses advanced AI for question generation
- **Contextual Questions**: Questions tailored to your topic and difficulty level
- **Detailed Explanations**: Every answer comes with comprehensive explanations
- **Robust Fallbacks**: Works even without AI with pre-defined question banks

### 🎮 **Interactive Quiz Experience**
- **Real-time Feedback**: Immediate response after each answer
- **Progress Tracking**: Visual progress indicator throughout the quiz
- **Smart Navigation**: Easy step-by-step navigation with validation
- **Results Analysis**: Detailed breakdown of performance with explanations

### 💻 **Modern Web Interface**
- **Responsive Design**: Perfect on desktop, tablet, and mobile devices
- **Bootstrap 5**: Clean, professional, and modern UI
- **Smooth Animations**: Enhanced user experience with CSS transitions
- **Accessibility**: Keyboard navigation and screen reader support
- **Error Handling**: User-friendly error messages and loading states

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Google Gemini API key (free at [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Quizer-AI-.git
   cd Quizer-AI-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the environment template
   cp .env.example .env
   
   # Edit .env and add your Gemini API key
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:5000`

## 🎯 How to Use

### Creating a Quiz

1. **📝 Enter Topic** 
   - Type your quiz subject (e.g., "Python Programming", "World War II", "Machine Learning")

2. **📂 Select Category & Level**
   - Choose from predefined categories
   - Select your preferred difficulty level

3. **🏷️ Choose Subtopics**
   - AI generates relevant subtopics automatically
   - Select which areas to focus on in your quiz

4. **⚙️ Configure Settings**
   - Choose number of questions (5-20)
   - Review your quiz summary

5. **🎮 Take the Quiz**
   - Answer multiple choice questions
   - Get instant feedback with detailed explanations
   - See your progress in real-time

6. **📊 Review Results**
   - View final score and percentage
   - Access detailed breakdown of all questions
   - Print or save results

## 🏗️ Project Structure

```
Quizer-AI-/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your environment variables (not in git)
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Quiz creation and taking interface
│   └── results.html     # Quiz results page
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Custom styles and animations
│   └── js/
│       └── quiz.js      # JavaScript functionality
└── README.md           # This file
```

## 🔧 Technical Details

### Backend Technologies
- **Flask 2.3.3**: Lightweight Python web framework
- **Google Gemini AI**: Advanced language model for content generation
- **Python-dotenv**: Environment variable management
- **Session Management**: Secure quiz state handling

### Frontend Technologies
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome 6**: Modern icons
- **Vanilla JavaScript**: No external JS dependencies
- **CSS Grid & Flexbox**: Modern layout techniques

### Key Features
- **Environment Variable Loading**: Secure API key management
- **Robust Error Handling**: Graceful fallbacks when AI is unavailable
- **JSON Response Cleaning**: Handles AI response formatting automatically
- **Input Validation**: Comprehensive validation on both frontend and backend
- **Loading States**: Better UX with progress indicators

## 🔑 Environment Variables

Create a `.env` file with the following variables:

```bash
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Google Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration (for future use)
DATABASE_URL=sqlite:///quizer.db
```

## 🛠️ Development

### Running in Development Mode
```bash
python app.py
```
The application runs on `http://localhost:5000` with auto-reload enabled.

### Code Quality Features
- **Error Handling**: Comprehensive try-catch blocks
- **Fallback Systems**: Works without AI when needed
- **Input Validation**: Both client and server-side validation
- **Clean Code**: Well-documented and organized code structure

## 🚦 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main quiz interface |
| `/get_categories` | POST | Retrieve available categories and levels |
| `/get_subtopics` | POST | Get AI-generated subtopics |
| `/start_quiz` | POST | Initialize quiz with generated questions |
| `/get_question` | GET | Retrieve current question |
| `/submit_answer` | POST | Submit answer and get feedback |
| `/quiz_results` | GET | Display final results |

## 🎨 Customization

### Adding New Categories
Edit the `CATEGORIES` dictionary in `app.py`:
```python
CATEGORIES = {
    'Your Category': ['Subtopic 1', 'Subtopic 2', 'Subtopic 3'],
    # ... existing categories
}
```

### Styling
Modify `static/css/style.css` to customize the appearance:
- Color schemes
- Fonts and typography
- Layout and spacing
- Animations and transitions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Roadmap

### Upcoming Features
- [ ] User authentication and profiles
- [ ] Quiz history and analytics
- [ ] Multiple quiz formats (True/False, Fill-in-the-blank)
- [ ] PDF export functionality
- [ ] Social sharing capabilities
- [ ] Mobile app version
- [ ] Custom question banks
- [ ] Collaborative quiz creation

### Technical Improvements
- [ ] Database integration for persistence
- [ ] API rate limiting
- [ ] Caching for better performance
- [ ] Unit and integration tests
- [ ] Docker containerization

## 🐛 Known Issues

- Dependency conflict warning with `langchain-google-genai` (doesn't affect functionality)
- Large quiz generation may take 10-15 seconds depending on AI response time

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent question generation
- **Bootstrap Team** for the responsive framework
- **Font Awesome** for beautiful icons
- **Flask Community** for excellent documentation

## 📞 Support

If you encounter any issues:
1. Check the terminal output for error messages
2. Verify your Gemini API key is correctly set
3. Ensure all dependencies are installed
4. Create an issue on GitHub with detailed information

---

**Made with ❤️ using Flask and Google Gemini AI**

*Last updated: July 1, 2025*
