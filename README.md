# AGBOT - Plant Health Monitoring Web Application

## Overview
AGBOT is a web-based plant health monitoring system that uses AI to detect pests and diseases in crops. The application allows farmers to scan plant leaves, receive instant pest identification, and get treatment recommendations following Integrated Pest Management (IPM) principles.

## Features
- 📸 **Plant Scanning**: Upload or capture images of plant leaves for analysis
- 🐛 **Pest Detection**: AI-powered identification of pest damage patterns
- 📊 **Dashboard**: Real-time statistics and monitoring of plant health
- 📈 **Trend Analysis**: Track pest detection trends over time
- 📝 **History Tracking**: View past scans and assessments
- 💊 **Treatment Recommendations**: IPM-compliant treatment suggestions
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## Technology Stack
- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Image Processing**: PIL (Python Imaging Library)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. Clone or download this project to your local machine

2. Navigate to the project directory:
```bash
cd agbot_app
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure
```
agbot_app/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Dashboard/home page
│   ├── scan.html        # Plant scanning interface
│   ├── history.html     # Scan history page
│   ├── results.html     # Analysis results page
│   └── about.html       # About page
│
├── static/              # Static assets
│   ├── css/
│   │   └── style.css   # Main stylesheet
│   ├── js/
│   │   └── main.js     # JavaScript functionality
│   └── uploads/        # Uploaded images directory
```

## Usage

### Scanning a Plant
1. Navigate to the "Scan" page
2. Either:
   - Click "Take Photo" to use your camera
   - Click "Upload Image" to select an image file
3. Review the captured/uploaded image
4. Click "Analyze Plant Health"
5. View the analysis results and treatment recommendations

### Dashboard Features
- View total scans, healthy plant percentage, and detected pests
- Monitor recent detections
- Track pest detection trends over time
- Check AI model status and accuracy

### History
- Review all past plant scans
- Filter by severity level
- View weekly insights and recommendations

## Features in Development
- Real ML model integration for pest detection
- Database persistence (PostgreSQL)
- User authentication and profiles
- Export reports to PDF
- Mobile app version
- Weather integration for predictive alerts
- Multi-language support

## Team
- **Dhanya Boyapally** - Computer Vision & ML Researcher
- **Krishna Karra** - Backend & Frontend Developer
- **Jack Frater** - Frontend & UI/UX Designer
- **Biao Wang** - Machine Learning & AI Specialist

**Mentor**: Professor Noel Aloysius, University of Missouri

## Environmental Impact
- 40% reduction in pesticide use through precise diagnosis
- Protects beneficial insects and soil health
- Reduces crop losses and promotes food security
- Empowers sustainable agricultural practices

## License
This project is for educational purposes as part of the University of Missouri curriculum.

## Support
For questions or support, please contact the development team.
