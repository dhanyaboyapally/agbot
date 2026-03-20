from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(10), default='en')  # en, hi, es, sw, etc.
    units = db.Column(db.String(10), default='metric')  # metric or imperial
    theme = db.Column(db.String(20), default='emerald')  # emerald, forest, ocean, sunset
    farm_name = db.Column(db.String(100), nullable=True)
    farm_size = db.Column(db.String(50), nullable=True)
    crops = db.Column(db.Text, nullable=True)  # Comma-separated crop list
    notification_email = db.Column(db.Boolean, default=True)
    notification_push = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # OAuth fields
    oauth_provider = db.Column(db.String(50), nullable=True)  # google, microsoft
    oauth_id = db.Column(db.String(255), nullable=True)

    # Relationships
    scans = db.relationship('Scan', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    feedbacks = db.relationship('Feedback', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'location': self.location,
            'language': self.language,
            'units': self.units,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Scan(db.Model):
    """Scan history model"""
    __tablename__ = 'scans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    pest_identified = db.Column(db.String(100), nullable=True)
    pest_scientific = db.Column(db.String(100), nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), nullable=True)  # Healthy, Pest Damaged
    severity = db.Column(db.String(50), nullable=True)  # Mild, Moderate, Severe
    crop_type = db.Column(db.String(100), nullable=True)
    field_name = db.Column(db.String(100), nullable=True)
    damage_pattern = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    feedbacks = db.relationship('Feedback', backref='scan', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        """Convert scan to dictionary"""
        return {
            'id': self.id,
            'pest_identified': self.pest_identified,
            'pest_scientific': self.pest_scientific,
            'confidence': self.confidence,
            'status': self.status,
            'severity': self.severity,
            'crop_type': self.crop_type,
            'field_name': self.field_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'has_feedback': self.feedbacks.count() > 0
        }


class Feedback(db.Model):
    """User feedback on scan results"""
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scan_id = db.Column(db.Integer, db.ForeignKey('scans.id'), nullable=False)

    # Feedback type
    is_correct = db.Column(db.Boolean, nullable=False)  # True if AI was correct

    # If incorrect, what was the actual pest?
    actual_pest_name = db.Column(db.String(100), nullable=True)
    actual_pest_scientific = db.Column(db.String(100), nullable=True)

    # Additional notes from user
    notes = db.Column(db.Text, nullable=True)

    # Was this feedback helpful for the user?
    helpful = db.Column(db.Boolean, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert feedback to dictionary"""
        return {
            'id': self.id,
            'is_correct': self.is_correct,
            'actual_pest_name': self.actual_pest_name,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PestDatabase(db.Model):
    """Common pests database for feedback dropdown"""
    __tablename__ = 'pests'

    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(100), nullable=False, index=True)
    scientific_name = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=True)  # insect, disease, fungal
    description = db.Column(db.Text, nullable=True)

    # Multilingual support
    name_es = db.Column(db.String(100), nullable=True)  # Spanish
    name_hi = db.Column(db.String(100), nullable=True)  # Hindi
    name_sw = db.Column(db.String(100), nullable=True)  # Swahili

    def to_dict(self, language='en'):
        """Convert pest to dictionary with language support"""
        name_field = f'name_{language}'
        localized_name = getattr(self, name_field, None) if language != 'en' else None

        return {
            'id': self.id,
            'common_name': localized_name or self.common_name,
            'scientific_name': self.scientific_name,
            'category': self.category
        }
