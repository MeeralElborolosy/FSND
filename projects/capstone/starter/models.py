import os
import datetime
from sqlalchemy import ForeignKey, Column, String, Integer, Boolean, DateTime, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

database_path = os.getenv('DATABASE_URL')
print('models '+database_path)

DEFAULT_RATING = 0

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print(db)
    db.create_all()


class Project(db.Model):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.datetime.utcnow())
    end_date = Column(DateTime)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date
        }


class Participant(db.Model):
    __tablename__ = 'participant'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    skills = Column(String, nullable=False)
    rating = Column(Integer, default=DEFAULT_RATING)
    rated_by = Column(Integer, default=0)
    is_mentor = Column(Boolean, nullable=False)
    projects = relationship('Project', secondary='participant_project')

    def __init__(self, name, skills, is_mentor):
        self.name = name
        self.skills = skills
        self.is_mentor = is_mentor

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'skills': self.skills,
            'rating': self.rating,
            'rated_by': self.rated_by,
            'is_mentor': self.is_mentor
        }


class Participant_Project(db.Model):
   __tablename__ = 'participant_project'
   participant_id = Column(Integer, ForeignKey('participant.id'), primary_key=True)
   project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)
