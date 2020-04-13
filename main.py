import os
import xlwt
import shutil
import cv2
import sys
import math
import numpy as np
import itertools
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import os



def sendmail():
    fromaddr = "decoderdefense@gmail.com"
    toaddr = "your email address"

# instance of MIMEMultipart 
    msg = MIMEMultipart() 

# storing the senders email address 
    msg['From'] = fromaddr 

# storing the receivers email address 
    msg['To'] = toaddr 

# storing the subject 
    msg['Subject'] = "Subject of the Mail"

# string to store the body of the mail 
    body = "Body_of_the_mail"

# attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 

# open the file to be sent 
    filename = "lsb_lenna.png"
    path = os.path.abspath("path to images")
    attachment=open(path,"rb")
    print(attachment)


# instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 

# To change the payload into encoded form 
    p.set_payload((attachment).read()) 

# encode into base64 
    encoders.encode_base64(p) 

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

# attach the instance 'p' to instance 'msg' 
    msg.attach(p) 

# creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 

# start TLS for security 
    s.starttls() 

# Authentication 
    s.login(fromaddr, "decoder@123") 

# Converts the Multipart msg into a string 
    text = msg.as_string() 

# sending the mail 
    s.sendmail(fromaddr, toaddr, text) 

# terminating the session 
    s.quit() 





class LSB():
    #encoding part :
    def encode_image(self,img, msg):
        length = len(msg)
        if length > 255:
            print("text too long! (don't exeed 255 characters)")
            return False
        encoded = img.copy()
        width, height = img.size
        index = 0
        for row in range(height):
            for col in range(width):
                if img.mode != 'RGB':
                    r, g, b ,a = img.getpixel((col, row))
                elif img.mode == 'RGB':
                    r, g, b = img.getpixel((col, row))
                # first value is length of msg
                if row == 0 and col == 0 and index < length:
                    asc = length
                elif index <= length:
                    c = msg[index -1]
                    asc = ord(c)
                else:
                    asc = b
                encoded.putpixel((col, row), (r, g , asc))
                index += 1
        return encoded

    #decoding part :
    def decode_image(self,img):
        width, height = img.size
        msg = ""
        index = 0
        for row in range(height):
            for col in range(width):
                if img.mode != 'RGB':
                    r, g, b ,a = img.getpixel((col, row))
                elif img.mode == 'RGB':
                    r, g, b = img.getpixel((col, row))  
                # first pixel r value is length of message
                if row == 0 and col == 0:
                    length = b
                elif index <= length:
                    msg += chr(b)
                index += 1
        lsb_decoded_image_file = "lsb_" + original_image_file
        #img.save(lsb_decoded_image_file)
        ##print("Decoded image was saved!")
        return msg


#creating new folders :
print("1. new user----2. existing user")
n= int(input())
if n==1:
    os.makedirs("Encoded_image/")
    os.makedirs("Decoded_output/")
    os.makedirs("Comparison_result/")
original_image_file = ""    # to make the file name global variable
lsb_encoded_image_file = ""
dct_encoded_image_file = ""
dwt_encoded_image_file = ""

while True:
    m = input("To encode press '1', to decode press '2', press any other button to close: ")

    if m == "1":
        os.chdir("Original_image/")
        original_image_file = input("Enter the name of the file with extension : ")
        lsb_img = Image.open(original_image_file)
        print("Description : ",lsb_img,"\nMode : ", lsb_img.mode)
        secret_msg = input("Enter the message you want to hide: ")
        print("The message length is: ",len(secret_msg))
        os.chdir("..")
        os.chdir("Encoded_image/")
        lsb_img_encoded = LSB().encode_image(lsb_img, secret_msg)
        lsb_encoded_image_file = "lsb_" + original_image_file
        lsb_img_encoded.save(lsb_encoded_image_file)
        print("Encrypting Encoded image..........")
        
        fo= open('lsb_lenna.png', "rb")
        image= fo.read()

        image= bytearray(image)

        f1= open('keys.txt',"r")
        key=int(f1.read())


        for index,value in enumerate(image):
            image[index]=value^key

        fo = open(lsb_encoded_image_file,"wb")
        fo.write(image)

        fo.close()

        print("\n")
        print("send mail")
        print("[Y/N]")
        ans= input()
        if  ans in ['Y','y']:
            sendmail()
        elif ans in ['N','n']:
            print("ENCODED DONE")
        else:
            os.chdir("..")

    elif m == "2":
        os.chdir("Encoded_image/")
        lsb_encoded_image_file = input("Enter the name of the file with extension : ")
        print("Decrypting Encoded image...........")
        
        fo= open('lsb_lenna.png', "rb")
        image= fo.read()

        image= bytearray(image)

        f1= open('keys.txt',"r")
        key=int(f1.read())


        for index,value in enumerate(image):
            image[index]=value^key

        fo = open(lsb_encoded_image_file,"wb")
        fo.write(image)

        fo.close()
        lsb_img = Image.open(lsb_encoded_image_file)
        lsb_hidden_text = LSB().decode_image(lsb_img)
#        os.chdir("Dncoded_image/")
#        file = open("lsb_hidden_text.txt","w")
#        file.write(lsb_hidden_text) # saving hidden text as text file
        print("--------------------------------------DECODED MESSAGE----------------------------------------------")
        print("\n")
        print(lsb_hidden_text)
        print("\n")
        print("---------------------------------------------------------------------------------------------------")


        
        os.chdir("..")
    else:
        print("Closed!")
        break
