from flask import Flask, jsonify, render_template, request
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template,session, redirect, url_for
import os
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = 'any random string'
conn = mysql.connector.connect(host="localhost",
                           user="root",
                           password="java",
                           db = "ayurdata")
c = conn.cursor()
@app.route("/")
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug = True, use_reloader = False)
