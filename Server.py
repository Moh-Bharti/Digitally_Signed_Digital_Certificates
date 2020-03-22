from flask import Flask,render_template,url_for,redirect,request,send_file
import sqlite3
import click
from flask import current_app,g
from flask.cli import with_appcontext
#import Crypto
from time import gmtime
from fpdf import FPDF
import base64
import hashlib



User_info = dict({'moh':[123,2016111],'abhishek':[234,2016006],'lakshay':[456,2016222],'kanha':[908,2016333]})
app = Flask(__name__,template_folder='templates')

@app.route('/')
def hello():
    #"Arre hello bol de"
    return 'Hello world'


# @app.route('/login',methods=['GET','POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         user_keys=User_info.keys()
#         user_values=User_info.values()
#         u = request.form['username']
#         p = request.form['password']
#         if user_keys.__contains__(u) and str(User_info.get(u))==p:

#             # return redirect(url_for('hello'))
#             return render_template('home.html')

#         else:

#             error = 'Invalid Username or password:' + " " + request.form['username']
#     return render_template('login.html',error=error)

#-----------------------------------------------------------------------------------------------#
def pdf(userName,userRollNumber):
    pdf = FPDF()
    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size=15)
    t = gmtime()
    
    for i in range(1, 28):
            if i == 1:
                pdf.cell(200, 10, txt=userName, ln=i, align='C')
            elif i == 2:
                pdf.cell(200, 5, txt=str(userRollNumber), ln=i, align='C')
                # pdf.cell(200,5,txt=Dict.get(name)[1],ln=i,align='R')
            # elif i == 3:
            #     pdf.cell(200, 10, txt=textuser, ln=i, align='C')
            elif i==16:
                pdf.cell(200, 10, txt="This is to certify that the student", ln=i, align='C')
            elif i==26:
                timeStamp = str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + "|" + str(
                    t.tm_mday) + "-" + str(t.tm_mon) + "-" + str(t.tm_year)

                pdf.cell(200, 10, txt=timeStamp, ln=i, align='C')
            else:
                pdf.cell(200, 10, txt="", ln=i, align='C')
    newName = userName + "_" + str(userRollNumber) + ".pdf"
    pfile=pdf.output(newName)
    return (newName,pfile)
    
@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        user_keys=User_info.keys()
        user_values=User_info.values()
        u = request.form['username']
        p = request.form['password']
        r=int(request.form['rollnumber'])
    
        if user_keys.__contains__(u) and str(User_info.get(u)[0])==p and User_info.get(u)[1]==r :
            pfile=pdf(u,r)
            # return redirect(url_for('hello'))
            # return render_template('home.html')
            return send_file('/home/abhishek2309/Documents/Digitally_Signed_Digital_Certificates/'+pfile[0],attachment_filename=pfile[0])

        else:

            # error = 'Invalid Username or password:' + " " + request.form['username']
            return render_template('home.html')
    return render_template('login.html',error=error)

if __name__== "__main__":
    app.run(debug=True)



