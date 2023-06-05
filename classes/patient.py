from flask_sqlalchemy import SQLAlchemy
from app import db

class Patient(db.Model):
    __tablename__ = 'patient'

    id_patient = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    telephone = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sexe = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Patient {self.nom}>'
