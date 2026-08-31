from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resumes = db.relationship("Resume", backref="owner", lazy=True, cascade="all, delete-orphan")
    analyses = db.relationship("Analysis", backref="owner", lazy=True, cascade="all, delete-orphan")

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    @property
    def first_name(self):
        return (self.name or "").split(" ")[0]

    @property
    def initial(self):
        return (self.name or "?")[:1].upper()


class Resume(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=True,index=True); name=db.Column(db.String(150),nullable=False); email=db.Column(db.String(150)); phone=db.Column(db.String(50)); role=db.Column(db.String(150)); summary=db.Column(db.Text); education=db.Column(db.Text); skills=db.Column(db.Text); experience=db.Column(db.Text); projects=db.Column(db.Text); certifications=db.Column(db.Text); template=db.Column(db.String(50),default="classic"); generated_text=db.Column(db.Text); created_at=db.Column(db.DateTime,default=datetime.utcnow)
    analyses=db.relationship("Analysis",backref="resume",lazy=True,cascade="all, delete-orphan")

class Analysis(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=True,index=True); resume_id=db.Column(db.Integer,db.ForeignKey("resume.id"),nullable=True); filename=db.Column(db.String(255)); score=db.Column(db.Integer,default=0); ats_score=db.Column(db.Integer,default=0); job_match_score=db.Column(db.Integer,default=0); strengths=db.Column(db.Text); weaknesses=db.Column(db.Text); suggestions=db.Column(db.Text); matched_keywords=db.Column(db.Text); missing_keywords=db.Column(db.Text); extracted_text=db.Column(db.Text); created_at=db.Column(db.DateTime,default=datetime.utcnow)
