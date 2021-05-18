from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
#import flask_sqlalchemy
from datetime import datetime

from werkzeug.utils import html

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
@app.route('/signin')
def sign_in():
    return 'This is the sign in page!'

@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form['name'] #name of the for field in the index.html
        password=request.form['pass']
        if (name=="admin" and password=="chakka"):
            return render_template('index.html')
    return render_template('login.html')


@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/home")

if __name__=="__main__":
    app.run(debug=False,host=0.0.0.0)
    #debug=true is given so that the error can be desplayed in the browser
    #if you want to change the recent port, put port=8000
    #debug will be true only in the development phase
