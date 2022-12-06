import re
import MySQLdb.cursors
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
import datetime
import requests, urllib.parse

app = Flask(__name__)


API_KEY = "[8c0bc3925af627aaea9cd0e809757e32]"
SENDER_NAME = "[]"


app.secret_key = 'kasjdbsdf'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'brgydb'
 
mysql = MySQL(app)
 
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s AND userpass = % s', (username, password, ))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM admin WHERE adname = % s AND adpassword = % s', (username, password, ))
        admin = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            f = datetime.datetime.now()
            msg = 'Login user: '+ username + f.strftime(" %A %m,%Y Time: %I:%M%p")
            return render_template('client.html', msg = msg,) 
        if admin:
            session['loggedin'] = True
            session['id'] = admin['id']
            session['username'] = admin['adname']
            f = datetime.datetime.now()
            msg = 'Login user: '+ username + f.strftime(" %A %m,%Y Time: %I:%M%p")
            return render_template('admin.html', msg = msg,) 
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))




@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s AND userpass = % s', (username, password))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password:
            msg = 'Please fill out the form !'
        else:      
            cursor.execute('INSERT INTO user VALUES (NULL,%s,%s)', (username, password,))
            mysql.connection.commit()
            msg = 'Success'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('reg_acc.html', msg = msg)




@app.route('/deleterecord', methods =['GET', 'POST'])
def deleterecord():
    msg = ''
    if request.method == 'POST' and 'username' in request.form:
        username = request.form['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            cursor.execute('DELETE FROM user WHERE username = %s', (username,))
            mysql.connection.commit()
            msg = 'successfully'
        else:
            msg = 'ACCOUNT NOT EXIST !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('delete_resident.html', msg = msg)



@app.route("/view_info")
def view():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    resultValue = cur.execute('SELECT * FROM user')
    if resultValue:
        userDetails = cur.fetchall()
        return render_template('acc_info.html',userDetails=userDetails)

@app.route("/Home")
def home():
    return render_template("admin.html")

@app.route("/Home2")
def home2():
    return url_for("youtube.com")



@app.route('/saverecord', methods =['GET', 'POST'])
def saverecord():
    msg = ''
    if request.method == 'POST' and 'fname' in request.form and 'mname' in request.form and 'lname' in request.form and 'gender' in request.form and 'age' in request.form and 'contact' in request.form and 'dob' in request.form and 'city' in request.form and 'brgy' in request.form and 'purok' in request.form and 'ps' in request.form :
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        gender = request.form['gender']
        age = request.form['age']
        con = request.form['contact']
        dob = request.form['dob']
        ci = request.form['city']
        br = request.form['brgy']
        pu = request.form['purok']
        ps = request.form['ps']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM resident')
        k = cursor.fetchone()
        if k:
            msg = 'Resident already exists !'
        else:      
            cursor.execute('INSERT INTO resident VALUES (NUll,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (fname, mname,lname,gender,age,con,dob,ci,br,pu,ps))
            mysql.connection.commit()
            msg = "Success"
    return render_template('add_resident.html', msg = msg)




@app.route("/resident_info")
def resident_info():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    resultValue = cur.execute('SELECT * FROM resident WHERE ')
    if resultValue:
        resident_info = cur.fetchall()
        return render_template('resident_info.html',resident_info=resident_info)
    else:
        return render_template('resident_info.html')



@app.route('/delete', methods =['GET', 'POST'])
def delete():
    msg = ''
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM resident')
        account = cursor.fetchone()
        if account:
            cursor.execute('DELETE FROM resident WHERE fname = %s AND lname = %s', (fname,lname))
            mysql.connection.commit()
            msg = 'successfully'
        else:
            msg = 'ACCOUNT NOT EXIST !'
    return render_template('delete.html', msg = msg)




if __name__ == "__main__":
    app.run(debug = True)  
