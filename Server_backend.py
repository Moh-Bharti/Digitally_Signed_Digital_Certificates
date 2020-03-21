from time import gmtime
from fpdf import FPDF
import crypto
from crypto.PublicKey import RSA
from crypto import Random
import base64
import PyPDF2
import hashlib
import text_to_image
from PIL import Image,ImageDraw, ImageFilter,ImageFont

registrar_privatekey, registrar_publickey = rsa_keys()
director_privatekey , director_publickey = rsa_keys()
director = "Prof. Ranjan bose"
registrar = "Dr. Ashok Kumar Solanki"

def rsa_keys():
    length=1024
    private = RSA.generate(length,Random.new().read())
    public = private.publickey()
    return private, public

def encrypt(private_key,text):
    hashtext = hashlib.sha3_512(text.encode())
    ciphertext = private_key.encrypt(hashtext,32)[0]
    b64cipher = base64.encode(ciphertext)

    return b64cipher

def decrypt(public_key,cipher):
    decode_cipher = base64.b64decode(cipher)
    plaintext = public_key.decrypt(decode_cipher)
    return plaintext

def pdf():
    pdf = FPDF()
    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size=15)

    # lets just say we are having a dictionary of users name as key and its roo number as its value
    Dict = {}
    Dict["john bandit"] = [12345, "21-10-1985"]
    Dict["tonny moore"] = [54321, "02-01-1995"]
    Dict["diana cliff"] = [24680, "11-07-1979"]
    print(Dict)
    # taking the user name from the user
    t = gmtime()
    name = 'john bandit'
    if name not in Dict.keys():
        print("User is not registered")
    else:
        for i in range(1, 28):
            if i == 1:
                pdf.cell(200, 10, txt=name, ln=i, align='C')
            elif i == 2:
                pdf.cell(200, 5, txt=str(Dict.get(name)[0]), ln=i, align='C')
                # pdf.cell(200,5,txt=Dict.get(name)[1],ln=i,align='R')
            elif i == 3:
                pdf.cell(200, 10, txt=Dict.get(name)[1], ln=i, align='C')
            elif i==16:
                pdf.cell(200, 10, txt="This is to certify that the student", ln=i, align='C')
            elif i==26:
                timeStamp = str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + "|" + str(
                    t.tm_mday) + "-" + str(t.tm_mon) + "-" + str(t.tm_year)

                pdf.cell(200, 10, txt=timeStamp, ln=i, align='C')
            else:
                pdf.cell(200, 10, txt="", ln=i, align='C')
    newName = name + "_" + str(Dict.get(name)[0]) + ".pdf"
    pdf.output(newName)
    watermark(t,newName)
    
def watermarker(t):
    timeStamp = str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + "|" + str(
        t.tm_mday) + "-" + str(t.tm_mon) + "-" + str(t.tm_year)
    font = ImageFont.truetype("arial.ttf", 20)
    enc_image = Image.new('RGB', (200, 200), (255, 255, 255))
    d = ImageDraw.Draw(enc_image)
    d.text((20, 20), timeStamp + "\n" + "IIITD", font=font, fill=(220, 220, 220, 128), align="center")

    enc_image.save('image.png')
    img = Image.open('image.png')
    im = img.copy()
    im.putalpha(0)
    im1 = img.convert('RGB')
    im1.save('watermark.pdf')

def watermark(t,pdf_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    watermarker(t)
    watermarked = open("watermark.pdf",'rb')
    input_file = open(pdf_file,'rb')
    merge_file = "merge.pdf"
    input_pdf = PyPDF2.PdfFileReader(pdf_file)
    page = input_pdf.getPage(0)
    watermark_pdf = PyPDF2.PdfFileReader(watermarked)
    watermark_page = watermark_pdf.getPage(0)
    page.mergePage(watermark_page)
    out = PyPDF2.PdfFileWriter()
    out.addPage(page)
    merge_file = open(merge_file,'wb')
    out.write(merge_file)
    merge_file.close()
    watermarked.close()
    input_file.close()



if __name__=='__main__':
    pdf()