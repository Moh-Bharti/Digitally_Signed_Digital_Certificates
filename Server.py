from flask import Flask,render_template,url_for,redirect,request
import sqlite3
import click
from flask import current_app,g
from flask.cli import with_appcontext

#import Crypto



User_info = dict({'moh':123,'abhishek':234,'lakshay':456,'kanha':908})
app = Flask(__name__,template_folder='templates')

@app.route('/')
def hello():
    #"Arre hello bol de"
    return 'Hello world'


@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        user_keys=User_info.keys()
        user_values=User_info.values()
        u = request.form['username']
        p = request.form['password']
        if user_keys.__contains__(u) and str(User_info.get(u))==p:

            # return redirect(url_for('hello'))
            return render_template('home.html')

        else:

            error = 'Invalid Username or password:' + " " + request.form['username']
    return render_template('login.html',error=error)

if __name__== "__main__":
    app.run(debug=True)



