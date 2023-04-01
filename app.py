# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 09:27:22 2023

@author: Sanford Jone
"""

from flask import Flask,request,render_template,session,url_for,redirect,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from model import recommend
import re
import pandas as pd
import model
    
app = Flask(__name__)

app.secret_key="yahoo"

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="albedo_42"
app.config["MYSQL_DB"]="dbs"

mysql=MySQL(app)

books=pd.read_csv(r"C:\Users\Sanford Jone\Downloads\Books\Books.csv")

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/dbs/',methods=['GET','POST'])
def login():
    msg=' '
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form["username"]
        password=request.form["password"]
        
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s",(username,password))
        login=cursor.fetchone()
        
        if login:
            session['loggedin'] = True
            session['username'] = login['username']
            return redirect(url_for('home'))
        else:
            msg="Invalid Credentials"
    return render_template("index.html",msg=msg)

@app.route('/dbs/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO login VALUES (%s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/dbs/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   return redirect(url_for('login'))


@app.route('/dbs/home')
def home(): 
    if 'loggedin' in session:
        languages = ["C++", "Python", "PHP", "Java", "C", "Ruby",
                     "R", "C#", "Dart", "Fortran", "Pascal", "Javascript"]
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('search')
	
    res=[]
    for i in range(706):
        res+=[model.piv.index[i]]
	
    res = [r for r in res if search.lower() in r.lower()]
    results=[]
    [results.append(x) for x in res if x not in results]
    return jsonify(results)

@app.route('/dbs/recommendations', methods=['POST'])
def recommendations():
    title = request.form['title']
    results = recommend(title)
    return render_template('recommendations.html', title=title, data=results)


if __name__=='__main__':
    app.run(host='localhost',port=5000,debug=True)