from flask_sqlalchemy import SQLAlchemy
from main import db

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

class Specialte(db.Model):
    __tablename__ = 'specialte'

    id_spe = db.Column(db.Integer, primary_key=True)
    specialite = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Specialte {self.id_spe}>'


class Ville(db.Model):
    __tablename__ = 'ville'

    id_ville = db.Column(db.String(200), primary_key=True)
    ville = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Ville {self.id_ville}>'


class Doctor(db.Model):
    __tablename__ = 'doctor'

    id_med = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    id_ville = db.Column(db.String(200), db.ForeignKey('ville.id_ville'), nullable=False)
    adresse = db.Column(db.String(1000))
    telephone = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    abonnee = db.Column(db.String(100), nullable=False)

    ville_rel = db.relationship('Ville', backref='doctors')

    def __repr__(self):
        return f'<Doctor {self.id_med}>'


class Avoir(db.Model):
    __tablename__ = 'avoir'

    id_med = db.Column(db.Integer, db.ForeignKey('doctor.id_med'), primary_key=True)
    id_spe = db.Column(db.Integer, db.ForeignKey('specialte.id_spe'), primary_key=True)

    doctor_rel = db.relationship('Doctor', backref='specialtes')
    specialte_rel = db.relationship('Specialte', backref='doctors')

    def __repr__(self):
        return f'<Avoir {self.id_med} - {self.id_spe}>'


class RendezVous(db.Model):
    __tablename__ = 'rendez_vous'

    id_med = db.Column(db.Integer, db.ForeignKey('doctor.id_med'), primary_key=True)
    id_patient = db.Column(db.Integer, db.ForeignKey('patient.id_patient'), primary_key=True)
    date_rdv = db.Column(db.TIMESTAMP, nullable=False)

    doctor_rel = db.relationship('Doctor', backref='rendez_vous')
    patient_rel = db.relationship('Patient', backref='rendez_vous')

    def __repr__(self):
        return f'<RendezVous {self.id_med} - {self.id_patient}>'
