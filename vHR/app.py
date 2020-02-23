from flask import Flask, jsonify, render_template, request
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template,session, redirect, url_for
import os
from werkzeug import secure_filename
import fullparser as fp
app = Flask(__name__)
app.secret_key = 'any random string'
conn = mysql.connector.connect(host="localhost",
                           user="root",
                           password="java",
                           db = "vHR")
c = conn.cursor()

#def fetch_applied_candidates(hr_email):
    

@app.route("/")
def default():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        det = request.form
        user = det['user']
        pswd = det['pass']
        print("***************************", user , "   " , pswd , "*************************** " )
        query = "SELECT password,user_type from logins where email='"+user+"'"
        c.execute(query)
        
        data = c.fetchall()
        print("***************************", data , "**********************")
        if pswd == data[0][0]:
            session['userid'] = user
            session['user_type'] = data[0][1]
            if data[0][1]=='h':
                c.execute('select Name from hr_details where Email="'+user+'"')
                user_name = c.fetchall()
                session['username']= user_name[0][0]
                return redirect(url_for('hr_dashboard'))
            if data[0][1]=='c':
                c.execute('select name from candidate_details where email="'+user+'"')
                user_name = c.fetchall()
                session['username']= user_name[0][0]
                print( data[0][1])            
                return redirect(url_for('can_dashboard'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username',None)
    return redirect(url_for('login'))

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = 'D:/vHR/vHR/static/resumes'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/candidate_reg", methods=['GET','POST'])
def candidate_reg():
    if request.method == "POST":
        details = request.form
        print("**********************************************",details)
        file = request.files['resume']
        filename = secure_filename(file.filename) 
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        all_det = fp.fetch_all_details(filepath)
        print(all_det,"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    return render_template("candidate_reg.html")

@app.route("/hr_reg")
def hr_reg():
    return render_template("hr_reg.html")

@app.route("/hr_dashboard")
def hr_dashboard():
    return render_template("hr_dashboard.html")

@app.route("/hr_profile")
def hr_profile():
    return render_template("hr_profile.html")

@app.route("/post_job")
def post_job():
    return render_template("post_job.html")

if __name__ == '__main__':
    app.run(debug = True, use_reloader = False)
