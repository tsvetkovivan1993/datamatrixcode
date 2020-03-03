#!/usr/bin/env python
import os
import glob
from subprocess import Popen
import sys
from pylibdmtx.pylibdmtx import encode
from PIL import Image
import csv
import smtplib
from smtplib import SMTP_SSL
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import os
import shutil
from zipfile import ZipFile
from os import path
from shutil import make_archive

for dirpath, dirnames, files in os.walk('/var/www/html/files'):
    if files:
        directory = '/var/www/html/files/'
        files = os.listdir(directory)
        images = filter(lambda x: x.endswith('.csv'), files)
        i = 0
        with open('/var/www/html/files/' + str(images[0])) as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                i += 1
                encoded = encode(str(row[0]))
                img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
                img.save('/home/ivan/pylibdtmx/qrman/' + str(i) + '.png')

        os.remove('/var/www/html/files/' + str(images[0]))

        # ZIP_____________________________________________
        zip_name = '/home/ivan/pylibdtmx/qrman/'
        directory_name = '/home/ivan/pylibdtmx/qrman/'
        # Create 'path\to\zip_file.zip'
        shutil.make_archive(zip_name, 'zip', directory_name)

        # ZIP_____________________________________________OFF
        # sendingEmail____________________________________OFF
        f = open('/var/www/html/email.txt')
        emailTO = f.read()
        print(emailTO)

        filepath = "/home/ivan/pylibdtmx/qrman.zip"
        basename = os.path.basename(filepath)
        address = "datamatrixod@gmail.com"
        # -----------mailTO
        TOaddress = emailTO
        # -----------------

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(filepath, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename)

        # Compose message
        msg = MIMEMultipart()
        msg['From'] = address
        msg['To'] = TOaddress
        msg['subject'] = "DataMatrixCode by Ivancvet@osnovad.ru"
        msg['BODY'] = "your files in attach"
        msg.attach(part)

        # Send mail
        smtp = SMTP_SSL()
        smtp.connect('smtp.gmail.com', 465)
        smtp.login(address, 'jguibjsbvcpuoulm')
        smtp.sendmail(address, TOaddress, msg.as_string())
        smtp.quit()
        # sendingEmail_____________________________________________OFF
        os.remove('/home/ivan/pylibdtmx/qrman.zip')
        folder3 = ('//home//ivan//pylibdtmx//qrman//')
        for the_file in os.listdir(folder3):
            file_path = os.path.join(folder3, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        if not files:
            quit()
