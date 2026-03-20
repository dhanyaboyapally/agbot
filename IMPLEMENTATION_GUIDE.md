# AGBOT Features Implementation Guide

This guide contains all the code and instructions to implement:
1. Login & Registration with OAuth
2. Feedback & Verification System
3. Settings & Localization

## Files Created
✅ models.py - Database models
✅ templates/login.html - Login page
✅ templates/register.html - Registration page
✅ translations/en.json - English translations
✅ translations/es.json - Spanish translations

## Files You Need to Create

### 1. Hindi Translation (translations/hi.json)
```json
{
  "app_name": "एग्बॉट",
  "tagline": "डेटा से फसल तक",
  "nav": {
    "home": "होम",
    "scan": "स्कैन",
    "history": "इतिहास",
    "about": "के बारे में",
    "settings": "सेटिंग्स",
    "logout": "लॉग आउट"
  },
  "auth": {
    "login": "साइन इन",
    "register": "साइन अप",
    "email": "ईमेल",
    "password": "पासवर्ड"
  },
  "feedback": {
    "title": "क्या यह सही है?",
    "yes_correct": "हां, सही लगता है",
    "no_incorrect": "नहीं, यह अलग है",
    "thank_you": "एग्बॉट को बेहतर बनाने में मदद के लिए धन्यवाद!"
  }
}
```

### 2. Swahili Translation (translations/sw.json)
```json
{
  "app_name": "AGBOT",
  "tagline": "Kutoka Kwa Data Hadi Mavuno",
  "nav": {
    "home": "Nyumbani",
    "scan": "Changanua",
    "history": "Historia",
    "about": "Kuhusu",
    "settings": "Mipangilio",
    "logout": "Toka"
  },
  "auth": {
    "login": "Ingia",
    "register": "Jisajili",
    "email": "Barua Pepe",
    "password": "Neno la siri"
  },
  "feedback": {
    "title": "Je, hii ni sahihi?",
    "yes_correct": "Ndiyo, inaonekana sahihi",
    "no_incorrect": "Hapana, ni tofauti",
    "thank_you": "Asante kwa kusaidia kuboresha AGBOT!"
  }
}
```

### 3. Settings Page (templates/settings.html)
```html
{% extends "base.html" %}
{% block title %}Settings - AGBOT{% endblock %}

{% block content %}
<div class="settings-container">
    <div class="settings-header">
        <h1><i class="fas fa-cog"></i> Settings</h1>
        <p>Manage your account and preferences</p>
    </div>

    <div class="settings-grid">
        <!-- Profile Section -->
        <div class="settings-card">
            <h2><i class="fas fa-user"></i> Profile</h2>
            <form method="POST" action="{{ url_for('update_profile') }}">
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" name="name" class="form-control" value="{{ current_user.name }}">
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" name="email" class="form-control" value="{{ current_user.email }}" readonly>
                </div>
                <div class="form-group">
                    <label>Phone</label>
                    <input type="tel" name="phone" class="form-control" value="{{ current_user.phone or '' }}">
                </div>
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" name="location" class="form-control" value="{{ current_user.location or '' }}">
                </div>
                <button type="submit" class="btn-primary">Save Changes</button>
            </form>
        </div>

        <!-- Language Section -->
        <div class="settings-card">
            <h2><i class="fas fa-language"></i> Language & Units</h2>
            <form method="POST" action="{{ url_for('update_preferences') }}">
                <div class="form-group">
                    <label>Language</label>
                    <select name="language" class="form-control" id="languageSelect">
                        <option value="en" {{ 'selected' if current_user.language == 'en' }}>English</option>
                        <option value="es" {{ 'selected' if current_user.language == 'es' }}>Español</option>
                        <option value="hi" {{ 'selected' if current_user.language == 'hi' }}>हिन्दी</option>
                        <option value="sw" {{ 'selected' if current_user.language == 'sw' }}>Kiswahili</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Units</label>
                    <select name="units" class="form-control">
                        <option value="metric" {{ 'selected' if current_user.units == 'metric' }}>Metric (kg, cm)</option>
                        <option value="imperial" {{ 'selected' if current_user.units == 'imperial' }}>Imperial (lb, in)</option>
                    </select>
                </div>
                <button type="submit" class="btn-primary">Save Changes</button>
            </form>
        </div>
    </div>
</div>

<script>
// Live language preview
document.getElementById('languageSelect').addEventListener('change', function() {
    if (confirm('Change language now?')) {
        this.form.submit();
    }
});
</script>
{% endblock %}
```

### 4. Update app.py

Add these imports at the top:
```python
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Scan, Feedback, PestDatabase
import jwt
from datetime import timedelta
import json
```

Add configuration:
```python
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'  # Change in production

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load translations
translations = {}
for lang in ['en', 'es', 'hi', 'sw']:
    with open(f'translations/{lang}.json', 'r', encoding='utf-8') as f:
        translations[lang] = json.load(f)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper function for translations
def get_translation(key, lang='en'):
    keys = key.split('.')
    value = translations.get(lang, translations['en'])
    for k in keys:
        value = value.get(k, key)
    return value
```

Add authentication routes:
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'

        user = User.query.filter((User.email == email) | (User.phone == email)).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()

            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Invalid email/phone or password', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        location = request.form.get('location')
        password = request.form.get('password')

        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))

        # Create new user
        user = User(name=name, email=email, phone=phone, location=location)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    current_user.name = request.form.get('name')
    current_user.phone = request.form.get('phone')
    current_user.location = request.form.get('location')
    db.session.commit()
    flash('Profile updated successfully', 'success')
    return redirect(url_for('settings'))

@app.route('/update_preferences', methods=['POST'])
@login_required
def update_preferences():
    current_user.language = request.form.get('language')
    current_user.units = request.form.get('units')
    db.session.commit()
    flash('Preferences updated successfully', 'success')
    return redirect(url_for('settings'))

# API endpoint for feedback
@app.route('/api/feedback', methods=['POST'])
@login_required
def submit_feedback():
    data = request.get_json()

    feedback = Feedback(
        user_id=current_user.id,
        scan_id=data.get('scan_id'),
        is_correct=data.get('is_correct'),
        actual_pest_name=data.get('actual_pest_name'),
        notes=data.get('notes')
    )

    db.session.add(feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback saved successfully'}), 200

# Get common pests for feedback dropdown
@app.route('/api/pests')
def get_pests():
    lang = request.args.get('lang', 'en')
    pests = PestDatabase.query.all()
    return jsonify([pest.to_dict(lang) for pest in pests])
```

Initialize database:
```python
with app.app_context():
    db.create_all()

    # Add sample pests
    if PestDatabase.query.count() == 0:
        pests = [
            PestDatabase(common_name='Japanese Beetle', scientific_name='Popillia japonica',
                        name_es='Escarabajo Japonés', name_hi='जापानी बीटल', name_sw='Mdudu wa Kijapani'),
            PestDatabase(common_name='Aphids', scientific_name='Aphidoidea',
                        name_es='Pulgones', name_hi='एफिड्स', name_sw='Dudu wa Majani'),
            PestDatabase(common_name='Spider Mites', scientific_name='Tetranychidae',
                        name_es='Ácaros', name_hi='मकड़ी के कण', name_sw='Panya wa Utando'),
        ]
        db.session.add_all(pests)
        db.session.commit()
```

### 5. Updated results.html with Feedback

Add this feedback section after the treatment recommendations:

```html
<!-- Feedback Section -->
{% if result.confidence < 75 %}
<div class="feedback-prompt">
    <div class="feedback-header">
        <i class="fas fa-question-circle"></i>
        <h3>Is this correct?</h3>
        <p>The AI confidence is {{ result.confidence }}%. Please help us verify this result.</p>
    </div>

    <div class="feedback-buttons">
        <button class="btn-feedback btn-correct" onclick="submitFeedback(true)">
            <i class="fas fa-check"></i>
            Yes, looks correct
        </button>
        <button class="btn-feedback btn-incorrect" onclick="showCorrectionForm()">
            <i class="fas fa-times"></i>
            No, it's different
        </button>
    </div>

    <div id="correctionForm" style="display: none;">
        <div class="form-group">
            <label>What is the correct pest?</label>
            <select id="correctPest" class="form-control">
                <option value="">Select correct pest...</option>
            </select>
        </div>
        <div class="form-group">
            <label>Additional notes (optional)</label>
            <textarea id="feedbackNotes" class="form-control" rows="3"></textarea>
        </div>
        <button class="btn-primary" onclick="submitCorrection()">Submit Feedback</button>
    </div>
</div>

<script>
let currentScanId = {{ scan_id or 'null' }};

async function loadPests() {
    const response = await fetch('/api/pests?lang={{ current_user.language if current_user else "en" }}');
    const pests = await response.json();
    const select = document.getElementById('correctPest');
    pests.forEach(pest => {
        const option = document.createElement('option');
        option.value = pest.common_name;
        option.textContent = pest.common_name;
        select.appendChild(option);
    });
}

function showCorrectionForm() {
    document.getElementById('correctionForm').style.display = 'block';
    loadPests();
}

async function submitFeedback(isCorrect) {
    const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            scan_id: currentScanId,
            is_correct: isCorrect
        })
    });

    if (response.ok) {
        showToast('Thank you for your feedback!', 'success');
        document.querySelector('.feedback-prompt').style.display = 'none';
    }
}

async function submitCorrection() {
    const actualPest = document.getElementById('correctPest').value;
    const notes = document.getElementById('feedbackNotes').value;

    const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            scan_id: currentScanId,
            is_correct: false,
            actual_pest_name: actualPest,
            notes: notes
        })
    });

    if (response.ok) {
        showToast('Thank you for helping improve AGBOT!', 'success');
        document.querySelector('.feedback-prompt').style.display = 'none';
    }
}
</script>

<style>
.feedback-prompt {
    background: #fffbeb;
    border: 2px solid #fbbf24;
    border-radius: 0.75rem;
    padding: 1.5rem;
    margin: 2rem 0;
}

.feedback-header {
    text-align: center;
    margin-bottom: 1.5rem;
}

.feedback-header i {
    font-size: 3rem;
    color: #fbbf24;
    margin-bottom: 0.5rem;
}

.feedback-buttons {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

.btn-feedback {
    flex: 1;
    padding: 1rem;
    border-radius: 0.5rem;
    border: 2px solid;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}

.btn-correct {
    background: #d1fae5;
    border-color: #10b981;
    color: #065f46;
}

.btn-correct:hover {
    background: #10b981;
    color: white;
}

.btn-incorrect {
    background: #fee2e2;
    border-color: #ef4444;
    color: #991b1b;
}

.btn-incorrect:hover {
    background: #ef4444;
    color: white;
}
</style>
{% endif %}
```

## Installation Steps

1. Install required packages:
```bash
pip install flask flask-sqlalchemy flask-login PyJWT
```

2. Initialize the database:
```bash
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

3. Run the application:
```bash
python app.py
```

## OAuth Setup (Optional)

For Google OAuth:
1. Go to Google Cloud Console
2. Create OAuth 2.0 credentials
3. Add redirect URI: http://localhost:5001/auth/google/callback

For Microsoft OAuth:
1. Go to Azure Portal
2. Register application
3. Add redirect URI: http://localhost:5001/auth/microsoft/callback

## Testing

1. Register a new user
2. Login with credentials
3. Scan a plant
4. Provide feedback on results
5. Change language in settings
6. Verify translations update

## Next Steps

- Add email verification
- Implement password reset
- Add OAuth providers
- Deploy to production
- Set up proper environment variables
