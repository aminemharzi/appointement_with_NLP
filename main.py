
from flask import Flask, render_template, request, redirect, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import folium
import datetime
import calendar
import joblib
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import secrets
from sqlalchemy import func


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@127.0.0.1:5432/CabMed'
db = SQLAlchemy(app)
secret_key = secrets.token_hex(16)
app.secret_key =secret_key


#Les table dans la base de données
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
    long_pat = db.Column(db.String(200), nullable=True)
    lat_pat = db.Column(db.String(200), nullable=True)

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
    description_maladie = db.Column(db.String(5000), nullable=False)
    date_rdv = db.Column(db.TIMESTAMP, nullable=False)
    doctor_rel = db.relationship('Doctor', backref='rendez_vous')
    patient_rel = db.relationship('Patient', backref='rendez_vous')

    def __repr__(self):
        return f'<RendezVous {self.id_med} - {self.id_patient}>'


pipeline = joblib.load('model/pipeline.pkl')
dabadoc_doctors = pd.read_excel("DabaDoc_Abonnee.xlsx", engine='openpyxl')
listes_rdv = pd.read_excel("listes_rdv.xlsx", engine='openpyxl')

def get_list_speciality(text):
    predicted_speciality = pipeline.predict([text])[0]
    # Generate predictions or probabilities for each class
    probabilities = pipeline.predict_proba([text])
    # Get the probability values for each class
    class_probabilities = probabilities[0]
    class_labels = []
    class_probs = []
    # Print the probabilities for each class
    for i, class_prob in enumerate(class_probabilities):
        class_label = pipeline.classes_[i]
        class_labels.append(class_label)
        test = str(class_prob * 100).split('.')[0]
        class_probs.append(class_prob)
    proba_df = pd.DataFrame({
        'Label': class_labels,
        'Proba': class_probs
    })
    sorted_df = proba_df.sort_values(by='Proba', ascending=False)
    sorted_df['Proba'] = (sorted_df['Proba'] * 100).astype(int)
    return  sorted_df[:6]



def distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula to calculate distance between two points
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of the Earth in kilometers
    return c * r

def find_nearest_doctor(patient_lat, patient_lon, df):

    # Calculate distance between patient and all doctors
    df['distance'] = df.apply(lambda row: distance(patient_lat, patient_lon, row['Latitude'], row['Longitude']), axis=1)

    # Sort doctors by distance and return the nearest one
    nearest_doctor = df.sort_values(by=['distance']).iloc[0]

    return nearest_doctor

def localisation(lat, lon):
    user_location = 'toi'

    # create a map with the location marker
    map = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], popup=user_location).add_to(map)

    map_html = map._repr_html_()
    return map_html
def near_localisation(lat, lon, another_lat,another_lon, name):

    user_location = 'toi'
    # create a map with the location marker
    map = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], popup=user_location).add_to(map)
    folium.Marker([another_lat, another_lon], popup=name, icon=folium.Icon(color="red")).add_to(map)
    map_html = map._repr_html_()
    return map_html

def doc_loca():

    user_location = 'toi'
    # create a map with the location marker
    medcin = Doctor.query.filter_by(id_med=session['id_doc']).first()

    map = folium.Map(location=[medcin.latitude, medcin.longitude], zoom_start=13)
    folium.Marker([medcin.latitude, medcin.longitude], popup=user_location).add_to(map)
    rendezvous_data = RendezVous.query.filter_by(id_med=session['id_doc']).all()
    for element in rendezvous_data:
        try:

            folium.Marker([float(element.patient_rel.lat_pat), float(element.patient_rel.long_pat)], popup=element.patient_rel.nom+" "+element.patient_rel.prenom, icon=folium.Icon(color="red")).add_to(map)
        except Exception as e :
            print(e)

    map_html = map._repr_html_()
    return map_html


def rdv_function(description_demandee, date_demandee, heure_demandee, patient_lat, patient_lon, ville_selectionee):
    list_long = []
    list_lat = []
    list_adresse = []
    list_tele = []
    list_ville = []
    list_id=[]


    predicted_speciality = pipeline.predict([description_demandee])[0]

    # Charger la base de données des médecins (DabaDoc)

    list_names = []

    for index, row in dabadoc_doctors.iterrows():
        spe = row['specialite']
        name = row['Name']
        list_spe = spe.split(',')
        for speciia in list_spe:
            if speciia.strip() == predicted_speciality:
                list_names.append(name)
                list_lat.append(row['Latitude'])
                list_long.append(row['Longitude'])
                list_tele.append(row['Telephone'])
                list_adresse.append(row['Adresse'])
                list_ville.append(row['Ville'])
                list_id.append(str(row['id_med']))
    #             print(speciia.strip())
    # les medcines dans votre spécialité
    specialite_selectionne = listes_rdv[listes_rdv['Nom_doc'].isin(list_names)]
    print("specialite_selectionne",specialite_selectionne)
    ville_selectionne = listes_rdv[
        (listes_rdv['Ville'] == ville_selectionee) & (listes_rdv['Nom_doc'].isin(specialite_selectionne['Nom_doc']))]
    print("ville_selectionne", ville_selectionne)
    date_cond = listes_rdv[
        (listes_rdv['Date'] == date_demandee) & (listes_rdv['Nom_doc'].isin(ville_selectionne['Nom_doc']))]
    print("date_cond", date_cond)
    heure_selectionne = listes_rdv[
        (listes_rdv['Heure'] == heure_demandee) & (listes_rdv['Nom_doc'].isin(date_cond['Nom_doc']))]
    print("heure_selectionne", heure_selectionne)

    if specialite_selectionne.empty:
        print("Sorry the speciality for u")
        return "Specialite"
    elif ville_selectionne.empty:
        print("Ville insdisp")
        return "Ville"
    elif date_cond.empty:
        print("date")
        return "date"
    elif heure_selectionne.empty:
        print("heur selectionne empty")
        return "heur"
    else:

    # Filtrer les médecins disponibles à la date et l'heure demandées

        available_doctors = heure_selectionne

        all_specialite_df = pd.DataFrame({
            'Name': list_names,
            'Latitude': list_lat,
            'Longitude': list_long,
            'Adresse': list_adresse,
            'Tele': list_tele,
            'ville': list_ville,
            'ID':list_id
        })

        all_specialite_df = all_specialite_df[all_specialite_df['Name'].isin(available_doctors['Nom_doc'])]
            # Find the nearest doctor
        nearest_doctor = find_nearest_doctor(patient_lat, patient_lon, all_specialite_df)


        return nearest_doctor

def generate_calendar(month , year):
    cal = calendar.monthcalendar(year, month)

    # Organize the days into weeks

    # Calculate the previous and next month and year
    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year
    # Get the calendar matrix for the specified year and month
    weeks = []
    for week in cal:
        days = []
        for day in week:
            if day == 0:
                days.append('')
            else:
                days.append(day)
        weeks.append(days)
    # Organize the days into weeks
    return month, year, prev_month, prev_year,next_month, next_year,weeks





@app.route('/')
def redirect_to_patient():
    return redirect('/login/patient')

@app.route('/patient',methods=['POST','GET'])
def index():
    if request.method == "POST":
        description = request.form['description_maladie']
        date_selectionne= request.form['date']
        heure_selectionne = request.form['heure']
        latitude=float(request.form['lat'])
        longetude=float(request.form['long'])
        ville_selected=request.form['ville']
        verification = description.split(" ")
        if len(verification)< 10:
            latitude = 33.589886
            longitude = -7.603869
            lat, lon = latitude, longitude
            # create a map with the location marker

            map_html = localisation(lat, lon)
            now = datetime.datetime.now()
            month, year, prev_month, prev_year, next_month, next_year, weeks = generate_calendar(now.month,now.year)
            message = "le longeur de Texte est pas favorable merci de bien remplir le champs"
            return render_template('index.html', month=month, year=year,
                                   prev_month=prev_month, prev_year=prev_year,
                                   next_month=next_month, next_year=next_year,
                                   weeks=weeks, map_html=map_html,message=message)

        else:

            date=""
            for i in date_selectionne.split("-"):
                if len(i)==2:
                    date=date+i+"-"
                elif len(i)==1:
                    date = date+"0"+i + "-"
                else:
                    date=date+i
            dd=""
            for i in date.split("-"):
                dd=i+'-'+dd
            try:
                result = rdv_function(description, dd[:-1], heure_selectionne, latitude, longetude,ville_selected)

                if isinstance(result, str) and result == "heur":
                    latitude = 33.589886
                    longitude = -7.603869
                    user_location = 'you'
                    lat, lon = latitude, longitude
                    # create a map with the location marker

                    map_html = localisation(lat, lon)
                    now = datetime.datetime.now()
                    month, year, prev_month, prev_year, next_month, next_year, weeks = generate_calendar(now.month,
                                                                                                         now.year)
                    return render_template('index.html', map_html=map_html, month=month, year=year,
                                           prev_month=prev_month, prev_year=prev_year,
                                           next_month=next_month, next_year=next_year,
                                           weeks=weeks, message="Il n y a pas des une heur disponible ")
                elif isinstance(result, str) and result == "Specialite":
                    latitude = 33.589886
                    longitude = -7.603869
                    user_location = 'you'
                    lat, lon = latitude, longitude
                    # create a map with the location marker

                    map_html = localisation(lat, lon)
                    now = datetime.datetime.now()
                    month, year, prev_month, prev_year, next_month, next_year, weeks = generate_calendar(now.month,
                                                                                                         now.year)
                    return render_template('index.html', map_html=map_html, month=month, year=year,
                                           prev_month=prev_month, prev_year=prev_year,
                                           next_month=next_month, next_year=next_year,
                                           weeks=weeks, message="Pardon il n'y a pas une medecin pour voutre malade")
                elif isinstance(result, str) and result == "Ville":
                    latitude = 33.589886
                    longitude = -7.603869
                    user_location = 'you'
                    lat, lon = latitude, longitude
                    # create a map with the location marker

                    map_html = localisation(lat, lon)
                    now = datetime.datetime.now()
                    month, year, prev_month, prev_year, next_month, next_year, weeks = generate_calendar(now.month,
                                                                                                         now.year)
                    return render_template('index.html', map_html=map_html, month=month, year=year,
                                           prev_month=prev_month, prev_year=prev_year,
                                           next_month=next_month, next_year=next_year,
                                           weeks=weeks, message="Pardon il n'y a pas une medecin dans "+ville_selected)
                elif isinstance(result, str) and result == "date":
                    latitude = 33.589886
                    longitude = -7.603869
                    lat, lon = latitude, longitude
                    # create a map with the location marker

                    map_html = localisation(lat, lon)
                    now = datetime.datetime.now()
                    month, year, prev_month, prev_year, next_month, next_year, weeks = generate_calendar(now.month,
                                                                                                         now.year)
                    return render_template('index.html', map_html=map_html, month=month, year=year,
                                           prev_month=prev_month, prev_year=prev_year,
                                           next_month=next_month, next_year=next_year,
                                           weeks=weeks, message="Pardon il n'y a pas une rendez vous avec la date selectionne "+dd[:-1])
                else:

                    result=rdv_function(description, dd[:-1], heure_selectionne, latitude, longetude,ville_selected)
                    name = result['Name']

                    another_lat = result['Latitude']

                    another_lon = result['Longitude']

                    adresse=result['Adresse']

                    tele= result['Tele']
                    
                    ville = result['ville']
                    id_me = result['ID']

                    map_html=near_localisation(latitude, longetude, float(another_lat), float(another_lon), name)
                    predicted_speciality = pipeline.predict([description])[0]
                    patient = Patient.query.filter_by(email=session['email']).first()

                    # Update the values

                    patient.long_pat = str(longetude)
                    patient.lat_pat = str(latitude)

                    # Commit the changes to the database
                    db.session.commit()

                    session['id_med']=id_me
                    session['description_maladie']=description
                    session['Date_rdv']=date_selectionne+" "+heure_selectionne

                    return render_template('reservation.html',
                                           map_html=map_html ,specialite=predicted_speciality,doctor_name=name, ville=ville,adresse= adresse,telephone=tele )
            except Exception as e :
                print(e)
                latitude = 33.589886
                longitude = -7.603869
                lat, lon = latitude, longitude
                # create a map with the location marker

                map_html = localisation(lat, lon)
                now = datetime.datetime.now()
                month, year, prev_month, prev_year, next_month, next_year, weeks = generate_calendar(now.month,
                                                                                                     now.year)
                return render_template('index.html', map_html=map_html, month=month, year=year,
                           prev_month=prev_month, prev_year=prev_year,
                           next_month=next_month, next_year=next_year,
                           weeks=weeks , message="Il n y a pas des rendez vous disponible merci")


    else:

        try:
            now = datetime.datetime.now()
            month = int(request.args.get('month', now.month))
            year = int(request.args.get('year', now.year))
            latitude = 33.589886
            longitude = -7.603869
            user_location = 'you'
            lat, lon = latitude,longitude
            # create a map with the location marker
            map = folium.Map(location=[lat, lon], zoom_start=13)
            folium.Marker([lat, lon], popup=user_location).add_to(map)
            map_html = map._repr_html_()
            month,year,prev_month,prev_year,next_month,next_year,weeks=generate_calendar(month,year)

            return render_template('index.html', month=month, year=year,
                           prev_month=prev_month, prev_year=prev_year,
                           next_month=next_month, next_year=next_year,
                           weeks=weeks ,map_html=map_html)
        except Exception as e :
            print(e)
            return "Il y a un erreur"

@app.route('/medcin', methods=['GET'])
def medcin():
    # Handle the /medcin request with id_patient parameter
    # Your logic here
    try:
        session['id_doc']
    except Exception as e:
        return redirect('/login/medcin')

    rendezvous_data = RendezVous.query.filter_by(id_med=session['id_doc']).order_by(
        RendezVous.date_rdv.desc()).all()
    # Fetch patient names for each RendezVous record
    rendezvous_dates = {}
    for rendezvous in rendezvous_data:
        date = rendezvous.date_rdv.date()
        if date not in rendezvous_dates:
            rendezvous_dates[date] = []
        rendezvous_dates[date].append(rendezvous)


    speciality_percent = get_list_speciality(rendezvous_data[0].description_maladie)
    full_name = rendezvous_data[0].patient_rel.nom + " " + rendezvous_data[0].patient_rel.prenom

    now = datetime.datetime.now()
    month, year, prev_month, prev_year, next_month, next_year, weeks = generate_calendar(now.month, now.year)
    cal = calendar.monthcalendar(year, month)
    # Organize the rendezvous dates into a structure that aligns with the calendar template
    map_html=doc_loca()

    weeks = []
    for week in cal:

        formatted_week = []
        for day in week:

            if day == 0:
                formatted_week.append('')
            else:
                date_to_check = datetime.date(year, month, day)

                if date_to_check in rendezvous_dates:
                    appointments = rendezvous_dates[date_to_check]
                    appointments_info = []
                    for appointment in appointments:
                        patient_name = appointment.patient_rel.nom + " " + appointment.patient_rel.prenom
                        rdv_temps = appointment.date_rdv.time()
                        rdv_temps_str = rdv_temps.strftime('%H:%M')

                        appointments_info.append({'patient_name': patient_name, 'temps': rdv_temps_str})

                    formatted_week.append({'day': day, 'has_rendezvous': True, 'appointments': appointments_info})

                else:
                    formatted_week.append({'day': day, 'has_rendezvous': False})
        weeks.append(formatted_week)


    return render_template('medcin.html', weeks=weeks, month=month, year=year, prev_month=prev_month,
                           prev_year=prev_year, next_month=next_month, next_year=next_year,
                           rendezvous_data=rendezvous_data,
                           speciality_percent=speciality_percent,full_name=full_name, id_patient=rendezvous_data[0].id_patient,
                           map_html=map_html)






@app.route('/medcin/<int:id_patient>', methods=['GET'])
def medcin_with_id(id_patient):
    # Handle the /medcin request with id_patient parameter
    # Your logic here
    try:
        session['id_doc']
    except Exception as e:
        return redirect('/login/medcin')




    try:
        map_html = doc_loca()
        now = datetime.datetime.now()
        month = int(request.args.get('month', now.month))
        year = int(request.args.get('year', now.year))
        month, year, prev_month, prev_year, next_month, next_year, weeks = generate_calendar(month, year)
        cal = calendar.monthcalendar(year, month)
        # Organize the rendezvous dates into a structure that aligns with the calendar template
        rendezvous_data = RendezVous.query.filter_by(id_med=session['id_doc']).order_by(
            RendezVous.date_rdv.desc()).all()
        # Fetch patient names for each RendezVous record
        rendezvous_dates = {}
        for rendezvous in rendezvous_data:
            date = rendezvous.date_rdv.date()
            if date not in rendezvous_dates:
                rendezvous_dates[date] = []
            rendezvous_dates[date].append(rendezvous)
        selected_patient = RendezVous.query.filter_by(id_med=session['id_doc'], id_patient=id_patient).first()
        full_name = selected_patient.patient_rel.nom + " " + selected_patient.patient_rel.prenom

        speciality_percent = get_list_speciality(selected_patient.description_maladie)

        weeks = []
        for week in cal:
            formatted_week = []
            for day in week:
                if day == 0:
                    formatted_week.append('')
                else:
                    date_to_check = datetime.date(year, month, day)
                    if date_to_check in rendezvous_dates:
                        appointments = rendezvous_dates[date_to_check]
                        appointments_info = []
                        for appointment in appointments:
                            patient_name = appointment.patient_rel.nom + " " + appointment.patient_rel.prenom
                            rdv_temps = appointment.date_rdv.time()
                            rdv_temps_str = rdv_temps.strftime('%H:%M')
                            appointments_info.append({'patient_name': patient_name, 'temps': rdv_temps_str})

                        formatted_week.append({'day': day, 'has_rendezvous': True, 'appointments': appointments_info})
                    else:
                        formatted_week.append({'day': day, 'has_rendezvous': False})
            weeks.append(formatted_week)

        return render_template('medcin.html', weeks=weeks, month=month, year=year, prev_month=prev_month,
                               prev_year=prev_year, next_month=next_month, next_year=next_year,
                               rendezvous_data=rendezvous_data, full_name=full_name,
                               speciality_percent=speciality_percent,
                               description_patient=selected_patient.description_maladie, id_patient=id_patient,map_html=map_html)



    except Exception as e :


        rendezvous_data = RendezVous.query.filter_by(id_med=session['id_doc']).order_by(
            RendezVous.date_rdv.desc()).all()
        # Fetch patient names for each RendezVous record
        rendezvous_dates = {}
        for rendezvous in rendezvous_data:
            date = rendezvous.date_rdv.date()
            if date not in rendezvous_dates:
                rendezvous_dates[date] = []
            rendezvous_dates[date].append(rendezvous)
        selected_patient = RendezVous.query.filter_by(id_med=session['id_doc'], id_patient=id_patient).first()
        full_name = selected_patient.patient_rel.nom + " " + selected_patient.patient_rel.prenom

        speciality_percent = get_list_speciality(selected_patient.description_maladie)

        now = datetime.datetime.now()
        month, year, prev_month, prev_year, next_month, next_year, weeks = generate_calendar(now.month, now.year)
        cal = calendar.monthcalendar(year, month)
        # Organize the rendezvous dates into a structure that aligns with the calendar template

        weeks = []
        for week in cal:
            formatted_week = []
            for day in week:
                if day == 0:
                    formatted_week.append('')
                else:
                    date_to_check = datetime.date(year, month, day)
                    if date_to_check in rendezvous_dates:
                        appointments = rendezvous_dates[date_to_check]
                        appointments_info = []
                        for appointment in appointments:
                            patient_name = appointment.patient_rel.nom + " " + appointment.patient_rel.prenom
                            rdv_temps = appointment.date_rdv.time()
                            rdv_temps_str = rdv_temps.strftime('%H:%M')
                            appointments_info.append({'patient_name': patient_name, 'temps': rdv_temps_str})

                        formatted_week.append({'day': day, 'has_rendezvous': True, 'appointments': appointments_info})
                    else:
                        formatted_week.append({'day': day, 'has_rendezvous': False})
            weeks.append(formatted_week)

        return render_template('medcin.html', weeks=weeks, month=month, year=year, prev_month=prev_month,
                               prev_year=prev_year, next_month=next_month, next_year=next_year,
                               rendezvous_data=rendezvous_data,full_name=full_name,
                               speciality_percent=speciality_percent, description_patient=selected_patient.description_maladie,
                               id_patient=id_patient,map_html=map_html)


@app.route('/login/medcin', methods=['POST', 'GET'])
def login_medcin():
    if request.method == "POST":
        name = request.form.get('email')
        id_doc = request.form.get('password')
        # Query the patient by email and password

        doctor = Doctor.query.filter_by(name=name, id_med=id_doc).first()

        if doctor:
            # Login successful
            session['id_doc'] = id_doc
            session['nom_med'] = name
            return redirect('/medcin')

        else:
            # Invalid credentials
            return render_template('login.html',type="med" ,message="le nom ou mot de passe invalidée")
    else:

        return render_template('login.html',type="med")


@app.route('/appointments_data')
def appointments_data():
    # Your logic to retrieve the appointment data
    # This could involve querying the database or processing some data

    # For example, let's assume you have a list of tuples containing month and appointment count:
    now = datetime.datetime.now()
    month = int(request.args.get('month', now.month))
    year = int(request.args.get('year', now.year))
    month, year, prev_month, prev_year, next_month, next_year, weeks = generate_calendar(month,year)


    cal = calendar.monthcalendar(year, month)
    # Organize the rendezvous dates into a structure that aligns with the calendar template
    rendezvous_data = RendezVous.query.filter_by(id_med=session['id_doc']).order_by(
        RendezVous.date_rdv.desc()).all()
    # Fetch patient names for each RendezVous record
    rendezvous_dates = {}
    for rendezvous in rendezvous_data:
        date = rendezvous.date_rdv.date()
        if date not in rendezvous_dates:
            rendezvous_dates[date] = []
        rendezvous_dates[date].append(rendezvous)


    my_data=[]
    weeks = []
    for week in cal:
        formatted_week = []
        for day in week:
            if day != 0:

                date_to_check = datetime.date(year, month, day)
                if date_to_check in rendezvous_dates:
                    appointments = rendezvous_dates[date_to_check]
                    appointments_info = []
                    for appointment in appointments:
                        patient_name = appointment.patient_rel.nom + " " + appointment.patient_rel.prenom
                        rdv_temps = appointment.date_rdv.time()
                        rdv_temps_str = rdv_temps.strftime('%H:%M')
                        appointments_info.append({'patient_name': patient_name, 'temps': rdv_temps_str})


                    formatted_week.append({'day': day, 'has_rendezvous': True, 'appointments': appointments_info})
                    my_data.append((day, len(appointments_info)))
                else:
                    formatted_week.append({'day': day, 'has_rendezvous': False})
                    my_data.append((day, 0))
        weeks.append(formatted_week)
        js={
            'next_year':year+1,
            'previous_year':year-1,
            'next_month':next_month,
            'previous_month':prev_month,
            'month':month,
            'year':year,
            'data':my_data

        }

    return jsonify(js)  # Return the data as JSON

@app.route('/login/patient', methods=['POST', 'GET'])
def login_patient():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # Query the patient by email and password
        patient = Patient.query.filter_by(email=email, password=password).first()


        if patient:
            # Login successful
            session['email'] = email
            return redirect('/patient')

        else:
            # Invalid credentials
            return render_template('login.html', message="Email ou mot de passe invalidée")
    else:

        return render_template('login.html')

@app.route('/signin/patient', methods=['POST', 'GET'])
def Signin_patient():
    if request.method == "POST":
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        telephone = request.form.get('telephone')
        age = request.form.get('age')
        adresse = request.form.get('adresse')
        password = request.form.get('password')
        email = request.form.get('email')
        sexe = request.form.get('sexe')
        # Query the patient by email and password
        patient = Patient.query.filter_by(email=email).first()

        if patient:
            return render_template('sign_in.html', message="L'email est déjà utilisé")
            # Login successful
            #return jsonify({'message': 'l email est deja utilisé', 'patient_id': patient.id_patient})
        else:
            new_patient = Patient(
                nom=nom,
                prenom=prenom,
                adresse=adresse,
                telephone=telephone,
                age=age,
                sexe=sexe,
                email=email,
                password=password,
                long_pat="",
                lat_pat=""
            )
            db.session.add(new_patient)
            db.session.commit()
            session['email'] = email

            # Invalid credentials


            return redirect('/patient')
    else:

        return render_template('sign_in.html')
@app.route("/rendez_vous", methods =['GET', 'POST'])
def rendez_vous():
    now = datetime.datetime.now()
    latitude = 33.589886
    longitude = -7.603869
    user_location = 'you'
    lat, lon = latitude, longitude
    # create a map with the location marker
    map = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], popup=user_location).add_to(map)
    map_html = map._repr_html_()
    month, year, prev_month, prev_year, next_month, next_year, weeks = generate_calendar(now.month, now.year)
    if request.method=='POST':
        try:

            id_med=session['id_med']
            email =session['email']
            date_rdv=session['Date_rdv']
            description_demandee= session['description_maladie']



            patient = Patient.query.filter_by(email=email).first()
            if patient:

                rendez_vous = RendezVous(id_med=id_med, id_patient=patient.id_patient, description_maladie=description_demandee,date_rdv=date_rdv)

                # Add the Rendez_vous to the database
                db.session.add(rendez_vous)
                db.session.commit()


                return render_template('index.html', month=month, year=year,
                                       prev_month=prev_month, prev_year=prev_year,
                                       next_month=next_month, next_year=next_year,
                                       weeks=weeks, map_html=map_html,message_succes="Votre rendez-vous est bien enregistré")

            else:
                 return redirect('/login/patient')
        except Exception as e :
            print(e)
            return jsonify({"message":"Il y a un erreur" +e})

    else:
        return render_template('index.html', month=month, year=year,
                               prev_month=prev_month, prev_year=prev_year,
                               next_month=next_month, next_year=next_year,
                               weeks=weeks, map_html=map_html, message="Il y a un probleme")



if __name__ =='__main__':
    app.run(debug=True)



