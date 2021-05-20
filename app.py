from functools import reduce
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
#import flask_sqlalchemy
from datetime import datetime

from werkzeug.utils import html
import sqlite3

#render_template is used to render the html files in the template folder

app = Flask(__name__)       #creating a flask app
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False 





db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/home', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title'] #name of the for field in the index.html
        desc=request.form['desc']
        todo= Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template('index.html',alltodo=alltodo)
#app.route is used to route to different pages
@app.route('/signup', methods=['GET','POST'])
def sign_up():
    msg1=None
    if(request.method=='POST'):
        if(request.form['name']!=""  and request.form['pass']!=""):
            username=request.form['name']
            password=request.form['pass']
            #connecting with the database
            conn1 = sqlite3.connect("signup.db")
            cursor1=conn1.cursor()
            cursor1.execute("INSERT INTO person VALUES('{name}','{password}')".format(name=username,password=password))
            msg1="your account is created"
            conn1.commit()
            conn1.close()
            print(msg1)
            return redirect("/")
            print(username+"s")
            print(password+"a")
        else:
            if(request.form['name']=="" or request.form['pass']==""):
                msg1="You can't leave the fields blank"
            else:
                msg1="Something went wrong"    
    return render_template('sign_up.html',msg1=msg1)

@app.route('/', methods=['GET','POST'])
def login():
    msg2=None
    if request.method=='POST':
        name=request.form['name'] #name of the for field in the index.html
        password=request.form['pass']
        #connecting with the database
        conn2 = sqlite3.connect("signup.db")
        cursor2=conn2.cursor()
        cursor2.execute("SELECT * FROM person WHERE username=='{name}' and password=='{password}'".format(name=name,password=password))
        r=cursor2.fetchall()
        if (len(r)==1): 
            return redirect("/home")
        else:
            msg2="Please enter a valid username and password!"
            print(msg2)
    return render_template('login.html',msg2=msg2)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/home")

if __name__=="__main__":
    app.run(debug=True, port=8000)
    #debug=true is given so that the error can be desplayed in the browser
    #if you want to change the recent port, put port=8000
    #debug will be true only in the development phase
