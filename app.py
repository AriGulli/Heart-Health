from flask import Flask, render_template, request, redirect, url_for, flash, session
from static.database.databases import get_db
import joblib


app = Flask(__name__)
app.secret_key='sdjk0543wdfghjkl'


# Load your machine learning model
model = joblib.load('newMultiModel.pkl')

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/home")
def home2():
    return render_template("home.html")


@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    if request.method == "POST":

        age = int(request.form["Age"])
        gender = int(request.form["Sex"])
        chest_pain = int(request.form["Chest Pain Type"])
        resting_blood_pressure=int(request.form['Resting Blood Pressure'])
        Cholesterol = int(request.form["Cholesterol"])
        Fasting_Blood_Sugar = int(request.form["Fasting Blood Sugar"])
        Rest_ECG = int(request.form["Rest ECG"])
        Max_Heart_Rate_Achieved = int(request.form["Max Heart Rate Achieved"])
        Exercise_Induced_Angina = int(request.form["Exercise Induced Angina"])
        ST_Depression = float(request.form["ST Depression"])
        ST_Slope = int(request.form["ST Slope"])
        Num_Major_Vessels = int(request.form["Num Major Vessels"])
        Thalassemia = int(request.form["Thalassemia"])


        # Get input values from the form and store them in the session
        session['age'] = age
        session['gender'] = gender
        session['chest_pain'] = chest_pain
        session['resting_blood_pressure']=resting_blood_pressure
        session['Cholesterol'] = Cholesterol
        session['Fasting_Blood_Sugar'] = Fasting_Blood_Sugar
        session['Rest_ECG'] = Rest_ECG
        session['Max_Heart_Rate_Achieved'] = Max_Heart_Rate_Achieved
        session['Exercise_Induced_Angina'] = Exercise_Induced_Angina
        session['ST_Depression'] = ST_Depression
        session['ST_Slope'] = ST_Slope
        session['Num_Major_Vessels'] = Num_Major_Vessels
        session['Thalassemia'] = Thalassemia

        # Predict using the model
        input_features=[age,gender,chest_pain,resting_blood_pressure,Cholesterol,Fasting_Blood_Sugar,Rest_ECG,Max_Heart_Rate_Achieved,Exercise_Induced_Angina,ST_Depression,ST_Slope,Num_Major_Vessels,Thalassemia]
        prediction = model.predict([input_features])
        result = prediction[0]
        
        # Store the prediction results in session variable
        session["prediction"] = prediction[0]

        # Render template with prediction
        return redirect(url_for("report"))
    return render_template("prediction.html")


@app.route("/report")
def report():

    # Assuming that all these values are set in session, otherwise provide a default value
    prediction = session.get('prediction', 'No prediction made')
    data = {
        'age': session.get('age'),
        'gender': session.get('gender'),
        'chest_pain': session.get('chest_pain'),
        'resting_blood_pressure': session.get('resting_blood_pressure'),
        'cholesterol': session.get('cholesterol'),
        'fasting_blood_sugar': session.get('fasting_blood_sugar'),
        'rest_ecg': session.get('rest_ecg'),
        'max_heart_rate_achieved': session.get('max_heart_rate_achieved'),
        'exercise_induced_angina': session.get('exercise_induced_angina'),
        'st_depression': session.get('st_depression'),
        'st_slope': session.get('st_slope'),
        'num_major_vessels': session.get('num_major_vessels'),
        'thalassemia': session.get('thalassemia'),
        'prediction': prediction
    }
    return render_template("report.html",data=data)


@app.route('/submit_email', methods=['GET', 'POST'])
def submit_email():
    message = None
    message_type = None

    if request.method == 'POST':
        email = request.form.get('email')
        db = get_db()
        if db.insert_email(email):
            message = 'Email successfully added'
            message_type = 'success'
        else:
            message = 'Email already exists'
            message_type = 'error'

    return render_template('submit_email.html', message=message, message_type=message_type)





if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0")
