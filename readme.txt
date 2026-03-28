# 🎭 EmotionReco - AI-Powered Emotion Detection System

![Django](https://img.shields.io/badge/Django-4.2.11-green) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.0-orange) ![License](https://img.shields.io/badge/License-MIT-yellow)

A comprehensive emotion recognition system that detects emotions from **facial expressions** and **voice analysis** using advanced AI and machine learning models. Built with Django, TensorFlow, and modern web technologies.

---

## 📦 REQUIREMENTS.txt

Create a file named `requirements.txt` with this content:

Django==4.2.11
django-crispy-forms==2.1
crispy-bootstrap5==2.0.0
psycopg2-binary==2.9.9
tensorflow==2.15.0
keras==2.15.0
numpy==1.24.3
opencv-python==4.9.0.80
opencv-contrib-python==4.9.0.80
scikit-learn==1.3.2
pandas==2.1.4
matplotlib==3.8.2
seaborn==0.13.1
deepface==0.0.86
tf-keras==2.15.0
librosa==0.10.1
soundfile==0.12.1
pydub==0.25.1
requests==2.31.0
assemblyai==0.22.0
Pillow==10.2.0
python-dateutil==2.8.2
pytz==2023.3
pytest==7.4.4
pytest-django==4.7.0
python-dotenv==1.0.0

---

## 🚀 QUICK START GUIDE

### 1. Prerequisites
- Python 3.10.9 or higher
- pip (Python package manager)
- Webcam (for facial detection)
- Microphone (for voice analysis)
- Modern web browser (Chrome/Firefox/Edge)

### 2. Installation Steps

# Step 1: Navigate to project directory
cd emotion_recommendation_system

# Step 2: Create virtual environment
python -m venv venv

# Step 3: Activate virtual environment
# For Windows:
venv\Scripts\activate

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Setup database
python manage.py makemigrations
python manage.py migrate

# Step 6: Create admin user
python manage.py createsuperuser

# Step 7: Run development server
python manage.py runserver

# Step 8: Access application
# Open browser and visit: http://127.0.0.1:8000/

---

## 🌟 FEATURES

### 👤 USER FEATURES
✅ Real-time Facial Emotion Detection - Detect emotions from webcam feed
✅ Voice Emotion Analysis - Analyze emotions from audio recordings
✅ Personal Dashboard - Track your emotion history and trends
✅ Personalized Recommendations - Get AI-powered wellness suggestions
✅ Interactive Charts - Visualize your emotional patterns over time (7-day activity, emotion distribution pie chart)
✅ Emotion History - View detailed logs of all detections with filters
✅ Profile Management - Manage your account settings

### 🛡️ ADMIN FEATURES
✅ Admin Dashboard - Comprehensive system analytics with key metrics
✅ User Management - Manage all registered users with search and filter
✅ Analytics & Reports - View system-wide emotion trends (30-day chart, peak hours)
✅ Feedback Management - Monitor user feedback and ratings
✅ Data Visualization - Interactive charts and graphs (Chart.js powered)
✅ User Leaderboard - See most active users
✅ Real-time Activity Feed - Monitor live system activity

### 🎯 TECHNICAL FEATURES
✅ Facial Recognition: DeepFace with TensorFlow backend
✅ Voice Analysis: AssemblyAI API integration
✅ Real-time Detection: WebRTC for live video streaming
✅ Modern UI: Bootstrap 5 with custom gradient designs
✅ Responsive Design: Works on mobile, tablet, and desktop
✅ Interactive Charts: Chart.js for data visualization
✅ Secure Authentication: Django built-in auth system

---

## 📁 PROJECT STRUCTURE

emotion_recommendation_system/
├── emotion_project/           # Main project settings (settings.py, urls.py, wsgi.py)
├── accounts/                  # User authentication (register, login, profile)
├── facial_emotion/            # Facial emotion detection module
│   ├── emotion_detector.py    # DeepFace integration
│   ├── models.py              # FacialEmotionCapture model
│   ├── views.py               # Detection views
│   └── templates/             # Detection page templates
├── voice_emotion/             # Voice emotion analysis module
│   ├── voice_analyzer.py      # AssemblyAI integration
│   ├── models.py              # VoiceEmotionAnalysis model
│   ├── views.py               # Analysis views
│   └── templates/             # Analysis page templates
├── user_dashboard/            # User dashboard with charts
│   ├── views.py               # Dashboard logic with statistics
│   └── templates/             # Dashboard HTML with Chart.js
├── admin_panel/               # Admin dashboard and management
│   ├── views.py               # Admin views with analytics
│   └── templates/             # Admin panel templates
├── recommendations/           # Recommendation engine
│   ├── recommendation_engine.py  # AI recommendation logic
│   ├── models.py              # Recommendation models
│   └── views.py               # Recommendation views
├── templates/                 # Base templates (base.html)
├── static/                    # Static files (CSS, JS, images)
├── media/                     # User uploaded files (audio, images)
├── requirements.txt           # Python dependencies
├── manage.py                  # Django management script
└── README.md                  # This file

---

## 🎮 HOW TO USE

### FOR REGULAR USERS

**1. Register/Login**
- Navigate to homepage (http://127.0.0.1:8000/)
- Click "Sign Up" to create a new account
- Fill in username, email, and password
- Or login with existing credentials

**2. Facial Emotion Detection**
- Click "Facial" in the navigation bar
- Click "Start Detection" button
- Allow camera permissions when prompted
- Face the camera - emotions detected in real-time
- Results are automatically saved to your history
- View confidence scores for each emotion

**3. Voice Emotion Analysis**
- Click "Voice" in the navigation bar
- Option 1: Click "Record" to capture live audio
- Option 2: Upload an audio file (WAV, MP3, M4A formats)
- Click "Analyze" button
- View emotion results with confidence scores
- Results saved to your history

**4. View Your Dashboard**
- Click "Dashboard" in navigation
- See your statistics: Total facial scans, voice analyses, dominant emotion, average confidence
- View 7-day activity chart (line graph showing daily detections)
- Check emotion distribution pie chart
- Read personalized AI-powered recommendations
- View recent activity feed

**5. Check History**
- Click "History" in navigation bar
- View all past emotion detections
- Filter by type: Facial or Voice
- Filter by date: Today, This Week, This Month
- See detailed logs with timestamps and confidence scores

### FOR ADMINISTRATORS

**1. Access Admin Panel**
- Login with admin/superuser account (created during setup)
- Navigate to /admin-panel/ URL
- Or click "Admin Dashboard" if you have admin privileges

**2. Admin Dashboard Overview**
- View key metrics: Total users, active users, total detections
- See today's activity statistics
- Monitor average system confidence score
- View top 5 detected emotions with counts
- Check 7-day system activity chart
- View user activity leaderboard (top 10 users)
- Monitor real-time activity feed

**3. User Management**
- Click "Users" in admin navigation
- View all registered users with statistics
- Search users by name or email (real-time search)
- Filter by status: Active, Inactive, Staff only
- Sort by: Recent, Most Active, Name (A-Z)
- View user details: Join date, last login, activity stats
- Action buttons: View details, Send message, Deactivate

**4. Analytics Page**
- Click "Analytics" in admin navigation
- View 30-day activity trend (line chart)
- See system-wide emotion distribution (doughnut chart)
- Check peak usage hours (bar chart)
- View detection type comparison (Facial vs Voice)
- See top detected emotions table with percentages
- Export reports (future feature)

**5. Manage Feedback**
- Click "Feedback" in admin navigation
- View all user feedback submissions
- See ratings (1-5 stars) and comments
- Monitor average rating score
- Filter and sort feedback

---

## 🎨 SUPPORTED EMOTIONS

The system can detect the following 7 emotions:

| Emotion   | Icon | Description                    | Color Scheme      |
|-----------|------|--------------------------------|-------------------|
| Happy     | 😊   | Joy, pleasure, contentment     | Yellow/Gold       |
| Sad       | 😢   | Sorrow, grief, melancholy      | Blue              |
| Angry     | 😡   | Rage, frustration, irritation  | Red               |
| Surprise  | 😮   | Amazement, shock, wonder       | Pink              |
| Fear      | 😨   | Anxiety, terror, apprehension  | Purple            |
| Disgust   | 🤢   | Revulsion, aversion, dislike   | Green             |
| Neutral   | 😐   | Calm, composed, emotionless    | Gray              |

---

## 🔧 CONFIGURATION

### Database Configuration
Edit `emotion_project/settings.py`:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

For production, use PostgreSQL:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'emotionreco_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

### API Keys Setup (Optional)
For voice analysis with AssemblyAI, add your API key:

In settings.py:
ASSEMBLYAI_API_KEY = 'your_api_key_here'

Or use environment variable:
# Windows:
set ASSEMBLYAI_API_KEY=your_key_here
# Mac/Linux:
export ASSEMBLYAI_API_KEY=your_key_here

### Static and Media Files

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

---

## 🐛 TROUBLESHOOTING

### Camera Not Working
**Problem:** Webcam not detected or permission denied
**Solutions:**
- Check browser permissions: Settings → Privacy & Security → Camera
- Make sure no other application is using the camera (Zoom, Teams, etc.)
- Try a different browser (Chrome recommended)
- On Windows: Check Camera privacy settings in Windows Settings
- Clear browser cache and try again
- Use HTTPS for production (camera requires secure context)

### Charts Not Displaying
**Problem:** Blank dashboard or analytics page
**Solutions:**
- Clear browser cache: Ctrl + Shift + Delete
- Open browser console (F12) and check for JavaScript errors
- Verify Chart.js is loaded in base.html: <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
- Check internet connection (Chart.js loads from CDN)
- Make sure you have emotion data in database (create some detections first)
- Check console logs for "Chart is not defined" error

### Voice Analysis Not Working
**Problem:** Audio upload or analysis fails
**Solutions:**
- Verify AssemblyAI API key is correct and active
- Check internet connection for API calls
- Ensure audio file format is supported: WAV, MP3, M4A
- File size should be under 10MB
- Check microphone permissions for recording
- Verify MEDIA_ROOT directory exists and is writable

### Database Errors
**Problem:** Migration errors or database locked
**Solutions:**
# Reset database completely:
python manage.py flush
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Or delete database and recreate:
# Delete db.sqlite3 file
python manage.py migrate
python manage.py createsuperuser

### Import Errors
**Problem:** ModuleNotFoundError or ImportError
**Solutions:**
# Upgrade pip first:
pip install --upgrade pip

# Reinstall all dependencies:
pip install -r requirements.txt --force-reinstall

# Install specific problematic package:
pip install tensorflow==2.15.0
pip install deepface==0.0.86

### Port Already in Use
**Problem:** Address already in use: 127.0.0.1:8000
**Solutions:**
# Use different port:
python manage.py runserver 8080

# Or kill process using port 8000 (Windows):
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux:
lsof -i :8000
kill -9 <PID_NUMBER>

### Slow Performance
**Problem:** Application running slowly
**Solutions:**
- Use PostgreSQL instead of SQLite for production
- Enable Django caching with Redis
- Optimize database queries with select_related() and prefetch_related()
- Reduce image/video quality for faster processing
- Use production server (Gunicorn/uWSGI) instead of development server

---

## 📊 DATABASE MODELS

### User Model (Django built-in)
- username: Unique username
- email: Email address
- password: Hashed password
- is_staff: Admin status
- is_superuser: Superuser status
- is_active: Account active status
- date_joined: Registration date
- last_login: Last login timestamp

### FacialEmotionCapture
- user: ForeignKey to User
- detected_emotion: CharField (happy, sad, angry, etc.)
- confidence_score: FloatField (0-100)
- image_data: TextField (base64 encoded)
- captured_at: DateTimeField (auto_now_add=True)

### VoiceEmotionAnalysis
- user: ForeignKey to User
- detected_emotion: CharField
- confidence_score: FloatField
- audio_file: FileField
- analyzed_at: DateTimeField (auto_now_add=True)

### UserRecommendation
- user: ForeignKey to User
- item: ForeignKey to RecommendationItem
- recommended_at: DateTimeField
- is_viewed: BooleanField

### RecommendationItem
- title: CharField
- description: TextField
- category: CharField
- content_url: URLField
- is_active: BooleanField

### UserFeedback
- user: ForeignKey to User
- rating: IntegerField (1-5)
- comment: TextField
- created_at: DateTimeField

---

## 🔐 SECURITY BEST PRACTICES

### For Production Deployment

**1. Change SECRET_KEY**
# Generate new secret key:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

In settings.py:
SECRET_KEY = 'your-new-generated-secret-key-here'

**2. Disable DEBUG Mode**
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

**3. Enable HTTPS**
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

**4. Use Environment Variables**
# Install python-dotenv:
pip install python-dotenv

# Create .env file:
SECRET_KEY=your_secret_key
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/dbname
ASSEMBLYAI_API_KEY=your_api_key

# In settings.py:
from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

**5. Database Backup**
# Backup database:
python manage.py dumpdata > backup.json

# Restore database:
python manage.py loaddata backup.json

**6. Enable CSRF Protection**
# Already enabled by default in Django
# Make sure CSRF token in all POST forms

---

## 🚀 DEPLOYMENT

### Deploy to Heroku

# Install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku:
heroku login

# Create new app:
heroku create emotionreco-app

# Add PostgreSQL addon:
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables:
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False

# Deploy:
git push heroku main

# Run migrations:
heroku run python manage.py migrate

# Create superuser:
heroku run python manage.py createsuperuser

# Open app:
heroku open

### Deploy to PythonAnywhere

1. Create account at pythonanywhere.com
2. Upload code via Git or file upload
3. Create virtual environment:
mkvirtualenv --python=/usr/bin/python3.10 emotionreco
4. Install requirements:
pip install -r requirements.txt
5. Configure WSGI file
6. Set static files path
7. Run migrations
8. Create superuser
9. Reload web app

### Deploy to AWS/DigitalOcean

1. Setup Ubuntu 20.04 server
2. Install dependencies:
sudo apt update
sudo apt install python3.10 python3-pip postgresql nginx
3. Clone repository
4. Setup virtual environment
5. Install requirements
6. Configure Gunicorn
7. Setup Nginx reverse proxy
8. Configure SSL with Let's Encrypt
9. Setup systemd service for auto-start

---

## 📈 PERFORMANCE OPTIMIZATION

**1. Use PostgreSQL**
- Replace SQLite with PostgreSQL for better performance
- Supports concurrent connections
- Better for production workloads

**2. Enable Caching**
# Install Redis:
pip install django-redis

# Configure cache in settings.py:
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}

**3. Optimize Database Queries**
# Use select_related() for ForeignKey:
emotions = FacialEmotionCapture.objects.select_related('user').all()

# Use prefetch_related() for ManyToMany:
users = User.objects.prefetch_related('facial_emotions').all()

**4. Compress Static Files**
# Install whitenoise:
pip install whitenoise

# Add to MIDDLEWARE:
'whitenoise.middleware.WhiteNoiseMiddleware',

**5. Use CDN**
- Serve static files from CDN (Cloudflare, AWS CloudFront)
- Faster loading times globally

**6. Image Optimization**
- Compress images before saving
- Use WebP format
- Lazy load images

---

## 🤝 CONTRIBUTING

Want to contribute? Great! Here's how:

**1. Fork the Repository**
- Click "Fork" button on GitHub
- Clone your fork: git clone https://github.com/yourusername/emotionreco.git

**2. Create Feature Branch**
git checkout -b feature/AmazingFeature

**3. Make Changes**
- Write clean, documented code
- Follow PEP 8 style guide
- Add tests for new features

**4. Commit Changes**
git add .
git commit -m 'Add some AmazingFeature'

**5. Push to Branch**
git push origin feature/AmazingFeature

**6. Open Pull Request**
- Go to your fork on GitHub
- Click "New Pull Request"
- Describe your changes

---

## 📄 LICENSE

MIT License

Copyright (c) 2025 EmotionReco

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 🙏 ACKNOWLEDGMENTS

- **DeepFace** - Facial emotion recognition library (https://github.com/serengil/deepface)
- **AssemblyAI** - Voice analysis API (https://www.assemblyai.com/)
- **Django** - Web framework (https://www.djangoproject.com/)
- **TensorFlow** - Machine learning framework (https://www.tensorflow.org/)
- **Bootstrap 5** - Frontend UI framework (https://getbootstrap.com/)
- **Chart.js** - Data visualization library (https://www.chartjs.org/)
- **OpenCV** - Computer vision library (https://opencv.org/)
- **Librosa** - Audio analysis library (https://librosa.org/)

---



## 📝 CHANGELOG

### Version 1.0.0 (November 14, 2025)
✅ Initial release
✅ Facial emotion detection with DeepFace
✅ Voice emotion analysis with AssemblyAI
✅ User dashboard with interactive charts
✅ Admin panel with comprehensive analytics
✅ Modern Bootstrap 5 UI with gradients
✅ User authentication and authorization
✅ Recommendation engine
✅ Emotion history with filters
✅ Real-time detection capabilities
✅ Responsive design for all devices

---

## 🎯 FUTURE ROADMAP

**Planned Features:**
- [ ] Mobile app (React Native) for iOS and Android
- [ ] Multi-language support (Spanish, French, German, Hindi)
- [ ] Advanced ML insights with trend predictions
- [ ] Integration with wearable devices (Apple Watch, Fitbit)
- [ ] Real-time emotion tracking dashboard
- [ ] Export data to CSV/PDF reports
- [ ] Social features (share emotions with friends, groups)
- [ ] Gamification (achievements, badges, leaderboards)
- [ ] Dark mode toggle
- [ ] Email notifications for emotion patterns
- [ ] Calendar view of emotion history
- [ ] API endpoints for third-party integrations
- [ ] Slack/Discord bot integration
- [ ] Voice assistant integration (Alexa, Google Assistant)

---

## 💻 SYSTEM REQUIREMENTS

**Minimum Requirements:**
- Operating System: Windows 10, macOS 10.14, Ubuntu 18.04 or higher
- RAM: 4GB
- Storage: 2GB free space
- Python: 3.10 or higher
- Browser: Chrome 90+, Firefox 88+, Edge 90+
- Internet: Required for API calls and CDN resources

**Recommended Requirements:**
- RAM: 8GB or higher
- Storage: 5GB free space
- GPU: NVIDIA GPU with CUDA support (for faster ML processing)
- Webcam: 720p or higher resolution
- Microphone: Built-in or external USB microphone
- SSD: For faster database operations

---

## 🧪 TESTING

### Run Tests

# Run all tests:
python manage.py test

# Run specific app tests:
python manage.py test facial_emotion
python manage.py test voice_emotion

# Run with coverage:
pip install coverage
coverage run manage.py test
coverage report
coverage html

### Manual Testing Checklist

**User Registration & Login:**
- [ ] Register new user successfully
- [ ] Login with correct credentials
- [ ] Login fails with wrong credentials
- [ ] Logout successfully

**Facial Detection:**
- [ ] Camera permission requested
- [ ] Real-time detection works
- [ ] Emotion results display correctly
- [ ] Confidence scores show accurately
- [ ] Results save to database

**Voice Analysis:**
- [ ] Audio recording works
- [ ] File upload accepts valid formats
- [ ] Analysis returns results
- [ ] Results save to history

**Dashboard:**
- [ ] Statistics display correctly
- [ ] Charts render properly
- [ ] Data updates in real-time
- [ ] Filters work correctly

**Admin Panel:**
- [ ] Admin can access panel
- [ ] User management works
- [ ] Analytics display correctly
- [ ] Charts render properly

---

## 📚 ADDITIONAL RESOURCES

**Documentation:**
- Django Documentation: https://docs.djangoproject.com/
- TensorFlow Guide: https://www.tensorflow.org/guide
- DeepFace GitHub: https://github.com/serengil/deepface
- AssemblyAI Docs: https://www.assemblyai.com/docs

**Tutorials:**
- Django for Beginners: https://djangoforbeginners.com/
- Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course
- Bootstrap 5 Documentation: https://getbootstrap.com/docs/5.3/

**Community:**
- Django Forum: https://forum.djangoproject.com/
- Stack Overflow: https://stackoverflow.com/questions/tagged/django
- Reddit r/django: https://www.reddit.com/r/django/

---

**⭐ If you like this project, please give it a star on GitHub!**

**Made with ❤️ using Django, TensorFlow & AI**

_Project Version: 1.0.0_
_Last Updated: November 14, 2025_
_Author: technoriders
_License: MIT_

---
# Emotion Recommendation System

This project is a Django-based Emotion Recommendation System that detects emotions using facial and voice inputs and provides recommendations.

## Features
- Facial Emotion Detection
- Voice Emotion Recognition
- User Dashboard
- Admin Panel
- Recommendation System

## Technologies Used
- Python
- Django
- TensorFlow
- HTML, CSS
- SQLite

## How to Run

1. Install requirements:
pip install -r requirements.txt

2. Run server:
python manage.py runserver
# Emotion Recommendation System using AI

## 📌 Project Overview
This project is an AI-based Emotion Recommendation System developed using Django. 
It detects emotions using facial and voice inputs and provides suitable recommendations.

## 🎯 Objectives
- Detect human emotions using facial expressions
- Recognize emotions from voice input
- Provide personalized recommendations
- Maintain user and admin dashboards

## 🧰 Technologies Used
- Python
- Django Framework
- TensorFlow / Machine Learning
- HTML, CSS
- SQLite Database

## 📂 Modules
- User Dashboard
- Admin Panel
- Facial Emotion Detection
- Voice Emotion Detection
- Recommendation System
- Model Training Module

## ▶️ How to Run the Project

1. Install dependencies:
pip install -r requirements.txt

2. Run migrations:
python manage.py migrate

3. Start server:
python manage.py runserver

4. Open browser:
http://127.0.0.1:8000/

## 👨‍💻 Developed By
Kishore Naidu  
Final Year Project

END OF README
