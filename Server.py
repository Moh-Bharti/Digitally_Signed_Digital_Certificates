from flask import Flask,render_template,url_for,redirect,request,send_file
import sqlite3
import click
from flask import current_app,g
from flask.cli import with_appcontext
import hashlib
from fpdf import FPDF
from time import gmtime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from Server_backend import *
import textwrap
from zipfile import *
import os
from PyPDF2 import *


app = Flask(__name__,template_folder='templates')

#password of users which have been hashed first before storing them in the database for better security
mohPassword=hashlib.sha3_512("123".encode()).hexdigest()
abhishekPassword=hashlib.sha3_512("234".encode()).hexdigest()
lakshayPassword=hashlib.sha3_512("456".encode()).hexdigest()
kanhaPassword=hashlib.sha3_512("908".encode()).hexdigest()
User_info = dict({'moh':[mohPassword,2016247],'abhishek':[abhishekPassword,2016006],'lakshay':[lakshayPassword,2016222],'kanha':[kanhaPassword,2016333]})
print(User_info.keys())
print(User_info.values())

# @app.route('/certificate',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def certificate():
    #"Arre hello bol de"
    error = None
    if request.method == 'POST':
        user_keys = User_info.keys()
        user_values = User_info.values()
        u = request.form['username']
        p = hashlib.sha3_512((request.form['password']).encode()).hexdigest()
        # r = str(hashlib.sha3_512(str(request.form['rollnumber']).encode())).encode()
        r=int(request.form['rollnumber'])

        if user_keys.__contains__(u) and (User_info.get(u)[0]==p) and User_info.get(u)[1] == r:
            pfile = pdf_file(u,r)
            # return redirect(url_for('hello'))
            # return render_template('home.html')
            return send_file('/home/abhishek2309/Documents/Network Security/ass3/Digitally_Signed_Digital_Certificates/' + pfile[0],attachment_filename=pfile[0])

        else:

            # error = 'Invalid Username or password:' + " " + request.form['username']
            return render_template('error.html')
    return render_template('Download.html', error=error)


def pdf_file(userName, userRollNumber):
    pdf = FPDF('L','mm','A4')
    # Add a page
    pdf.add_page(orientation='L')
    pdf.set_auto_page_break(0)
    has,r,d = digital_signature()
    # set style and size of font
    # that you want in the pdf
    h = has.split('\n')

    pdf.set_font("Times", size=12, style='b')
    t = gmtime()

    wrapper = textwrap.TextWrapper(width=50)
    word1 = wrapper.wrap(text=h[0])
    word2 = wrapper.wrap(text=h[1])
    print(word1)
    print(word2)
    for i in range(1, 30):
        if i == 1:
            pdf.set_font("Times",size=20,style='b')
            pdf.cell(200, 10, txt="Certificate Of Graduation", ln=i, align='C')
        elif i == 4:
            pdf.set_font("Courier", size=15, style='b')
            pdf.cell(200, 5, txt="IIITD", ln=i, align='C')
            # pdf.cell(200,5,txt=Dict.get(name)[1],ln=i,align='R')
        # elif i == 3:
        #     pdf.cell(200, 10, txt=textuser, ln=i, align='C')
        elif i == 6:
            pdf.set_font("Arial", size=12, style='b')
            pdf.cell(200, 10, txt="This graduation certificate is presented to those who has fulfilled all", ln=i, align='C')
        elif i == 7:
            pdf.set_font("Arial", size=12, style='b')
            pdf.cell(200, 10, txt="the requirements of the program of study", ln=i, align='C')

        elif i == 12:
            pdf.set_font("Arial", size=12, style='b')
            pdf.cell(200, 10, txt="Name of the Student-:"+" "+userName, ln=i, align='L')

        elif i == 13:
            pdf.set_font("Arial", size=12, style='b')
            pdf.cell(200, 10, txt="Roll No.-:"+" "+str(userRollNumber), ln=i, align='R')

        elif i == 18:
            pdf.set_font("Arial", size=12, style='b')
            timeStamp = str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + "|" + str(
                t.tm_mday) + "-" + str(t.tm_mon) + "-" + str(t.tm_year)
            pdf.cell(200, 10, txt="Date & Time-"+timeStamp, ln=i, align='R')


        else:
            pdf.set_font("Arial", size=12, style='b')
            pdf.cell(200, 10, txt="", ln=i, align='C')

    pdf1 = FPDF('L', 'mm', 'A4')
    # Add a page
    pdf1.add_page(orientation='L')
    pdf1.set_auto_page_break(0)
    pdf1.set_font("Arial", size=12, style='b')
    for i in range(1,28):
        if i == 2:

             pdf1.cell(200, 10, txt="Digital Signature of Registrar-", ln=i, align='C')

        elif i == 3:
            pdf1.set_font("Arial", size=8, style='b')
            for j in range(7):
                pdf1.cell(400, 10, txt=word1[j], ln=i + j, align='C')
        elif i == 12:
            pdf1.set_font("Arial", size=12, style='b')
            pdf1.cell(200, 10, txt="Digital Signature of Director-", ln=i, align='C')
        elif i == 13:
            pdf1.set_font("Arial", size=8, style='b')
            for j in range(7):
                pdf1.cell(400, 10, txt=word2[j], ln=i + j, align='C')



    newName = userName + "_" + str(userRollNumber) + ".pdf"
    pfile = pdf.output(newName)
    watermark(t,newName)
    pfile1 = pdf1.output("Signature"+".pdf")
    watermark(t,"Signature.pdf")
    loc = "/home/abhishek2309/Documents/Network Security/ass3/Digitally_Signed_Digital_Certificates/"
    x = [loc+"\\"+a for a in os.listdir(loc) if a.endswith(".pdf")]
    merger = PdfFileMerger()

    merger.append(open(newName,'rb'))
    merger.append(open("Signature.pdf",'rb'))

    with open(userName + "_" + str(userRollNumber)+ ".pdf","wb") as fout:
        merger.write(fout)
    #Zipname = str(userRollNumber)+".zip"
    #file_path =[]
    #directory = "./"+str(userRollNumber)



    return (newName, pfile)


# @app.route('/login',methods=['GET','POST'])
# def login():
# @app.route('/download',methods=['GET','POST'])
# def download():
#     error = None
#     if request.method == 'POST':
#         user_keys=User_info.keys()
#         user_values=User_info.values()
#         u = request.form['username']
#         p = request.form['password']
#         if user_keys.__contains__(u) and str(User_info.get(u)[0])==p:

#             return redirect(url_for('certificate'))

#         else:

#             error = 'Invalid Username or password:' + " " + request.form['username']
#     return render_template('Download.html',error=error)

if __name__== "__main__":
    app.run(debug=True)



