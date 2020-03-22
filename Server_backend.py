from time import gmtime
from fpdf import FPDF
import base64
import PyPDF2
import hashlib
import text_to_image
from PIL import Image,ImageDraw, ImageFilter,ImageFont
from base64 import b64decode,b64encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import re

def rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048,backend=default_backend())
    public_key = private_key.public_key()
    return private_key,public_key

def encrypt(private_key,text):
    byte = text.encode()
    h = hashlib.sha256()
    h.update(byte)
    hashtext = h.digest()

    ciphertext = private_key.encrypt(hashtext,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

    return b64encode(ciphertext),hashtext


def decrypt(public_key,cipher):
    hashtext = public_key.decrypt(cipher,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return hashtext




def watermarker(t):
    timeStamp = str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + "|" + str(
        t.tm_mday) + "-" + str(t.tm_mon) + "-" + str(t.tm_year)
    font = ImageFont.truetype("arial.ttf", 15)
    enc_image = Image.new('RGB', (200, 200), (255, 255, 255))
    d = ImageDraw.Draw(enc_image)
    d.text((0, 0), timeStamp + "\n" + "IIITD", font=font, fill=(220, 220, 220, 128), align="center")

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
    merge_file = pdf_file
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

def digital_signature():
    registrar_privatekey, registrar_publickey = rsa_keys()
    director_privatekey, director_publickey = rsa_keys()
    director = "Prof. Ranjan Bose"
    registrar = "Dr. Ashok Kumar Solanki"
    c1,h1 = encrypt(registrar_publickey, registrar)
    c1= c1.decode('utf-8')
    c2,h2 = encrypt(director_publickey,director)
    c2=c2.decode('utf-8')
    signature =  c1+ '\n' + c2
    return signature,registrar_privatekey,director_privatekey

def verify(data):
    signature, registrar_privatekey, director_privatekey = digital_signature()
    sign = signature.split("\n")
    sign1 = b64decode(sign[0])
    sign2 = b64decode(sign[1])
    data1 = decrypt(registrar_privatekey, sign1)
    data2 = decrypt(director_privatekey, sign2)


if __name__=='__main__':


    print(data1)
    print(data2)

