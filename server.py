from flask import Flask, request, redirect, render_template, flash
from mysqlconnection import MySQLConnector
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
mysql = MySQLConnector(app,'emaildb')
app.secret_key = 'thisIsASecretKeepItThatWay'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')

def submitEmail():
    query = "SELECT email FROM email"
    emails = mysql.query_db(query)
    return render_template('success.html', all_emails = emails)

@app.route('/email', methods=['POST'])

def displayEmails():
    print request.form['email']
    
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email address!')
        return redirect('/')
    else:
        query = 'INSERT INTO email (email, created_at, updated_at) VALUES (:email, NOW(), NOW())'
        data = {
            'email': request.form['email']
            }
        emails = mysql.query_db(query, data)
    return redirect('/success')

app.run(debug=True)