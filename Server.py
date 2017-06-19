import os
import cgi
import subprocess
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, redirect, request, render_template, jsonify
from ghost import Ghost
import sqlite3
import logging

DATABASE = 'smile.db'

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'php'])

@app.route("/hello")
def list():
    print("Hello world")
    # res_filter = getFilter()
    resourceUrl = getResources()
    img = getImage()
    return render_template('index.html', url = resourceUrl, imageName=img, msg = '')


@app.route("/load/Video")
def loadVideo():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT url FROM tbl_Resources WHERE Genre = 'Video' ")
    data = cur.fetchall()
    conn.close()
    img=getImage()
    return render_template('resources.html', url = data, imageName=img)

@app.route("/load/Article")
def loadArticle():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT url FROM tbl_Resources WHERE Genre = 'Article' ")
    data = cur.fetchall()
    conn.close()
    img=getImage()
    return render_template('resources.html', url = data, imageName=img)

@app.route("/load/Images")
def loadImage():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT url FROM tbl_Resources WHERE Genre = 'Image' ")
    data = cur.fetchall()
    conn.close()
    img=getImage()
    return render_template('resources.html', url = data, imageName=img)

@app.route("/load/Sound")
def loadSound():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT url FROM tbl_Resources WHERE Genre = 'Sound' ")
    data = cur.fetchall()
    conn.close()
    img=getImage()
    return render_template('resources.html', url = data, imageName=img)

@app.route("/load/All")
def loadAll():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT url FROM tbl_Resources")
    data = cur.fetchall()
    conn.close()
    img=getImage()
    return render_template('resources.html', url = data, imageName=img)

@app.route("/GetEmailLogs")
def getLogs():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT Email FROM tbl_Patient")
    data = cur.fetchall()
    conn.close()
    return render_template("emailLogs.html", email = data)

@app.route("/SendEmail", methods=['POST'])
def email():

    from_email = "ReyadTesting@gmail.com"
    from_pwd = "hi123456"
    to_email = request.form.get('Email', default="Error")

    msg = MIMEMultipart('html')
    msg['Subject'] = "Blocs"
    msg['From'] = from_email
    msg['To'] = to_email

    html = """\
    <html>
    <head></head>
      <body>
        <p>Your Blocs.<br>
           <b>Please take the time to look through these resources</b><br>
        </p>
        <article>

        </article>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))
    print(msg)
    # May want to add some error checks here
    # Change these based on the SMTP params of your mail provider
    mail = smtplib.SMTP('outlook.office365.com', 587)

    msg.attach(MIMEText(html, 'html'))
    print(msg)

    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()
    mail.starttls()
    mail.login(from_email, from_pwd)
    mail.sendmail(from_email, to_email, msg.as_string())
    print("email sent")
    mail.quit()

    return render_template('email.html')
    return "email sent"

@app.route("/hello/addEmail", methods=['POST', 'GET'])
def addUsrEmail():
    email = request.form.get('Email', default="Error")
    test_dentistID = 1
    try:
        con = sqlite3.connect(DATABASE)
        c = con.cursor()
        c.execute("INSERT INTO tbl_Patient ('DentistID', 'Email') \
                    VALUES (?,?)", (test_dentistID, email))
        con.commit()
        msg = "Added email successfully"
    except:
        con.rollback()
        msg = "Error adding email"
    finally:
        return msg
        con.close()

profile = []
@app.route("/hello/profile", methods=["GET", "POST"])
def profile():
    # console.log("hello")
    logging.info("Entry")
    if request.method == 'GET':
        return render_template("home.html")
    elif request.method == 'POST':
        msg = 'complete'
        userName = request.form.get("userName")
        socialMedia = request.form.get("socialMedia")
        Establishments = request.form.get("CompanyName")
        Qualifications = request.form.get("Qualifications")
        WebsiteUrl = request.form.get("Url")
        profileLogo = request.form.get("logo")
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO tbl_dentist ('Establisments', 'PostALevelQualificationa', 'WebsiteUrl', 'ProfileLogo', 'socialMedia', 'userName')\
                         VALUES (?,?,?,?,?,?)",(Establishments, Qualifications, WebsiteUrl, profileLogo, socialMedia, userName) )
        conn.commit()
        conn.close()
    return msg

@app.route("/hello/AddBloc", methods=["POST", "GET"])
def AddBloc():
    logging.info("Entry")
    if request.method == "GET":
        return render_template("home.html")
    elif request.method == "POST":
        msg = "Record successfully added"
        blocUrl = request.form.get("blocUrl")
        blocTitle = request.form.get("blocTitle")
        Genre = request.form.get("genre")
        image = request.form.get("blocLogo")
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO tbl_Resources ('url', 'Genre', 'Name', 'image')\
                    VALUES (?,?,?,?)",(blocUrl, Genre, blocTitle, image) )
        conn.commit()
        conn.close()
        image = str(image)
        # resourceUrl = getResources()
        # img = getImage()
        resourceUrl = getResources()
        img = getImage()

    return (render_template('home.html', image = image, url = resourceUrl, imageName=img))
    # return render_template("home.html")
    # return =""

Admin = []
@app.route("/login", methods=["POST", "GET"])
def login():
    # logging.info("Entry")
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        print(email)
        print(password)
        cur.execute("SELECT * FROM Admin WHERE  Password =?",[str(password)])
        # conn.commit()
        # Email = "+email+" and
        data = cur.fetchall()
        print(data)
        datalen = len(data)
        print(datalen)
        conn.close()
        message = str(email)
        resourceUrl = getResources()
        img = getImage()

        if datalen == 0:
            return render_template("index.html")
        else:
            return render_template("home.html", message = message, url = resourceUrl, imageName=img, msg = '')




@app.route("/signUp", methods=["POST", "GET"])
def signUp():
    logging.info("Entry")
    if request.method == "GET":
        return render_template("signUP.html")
    elif request.method == "POST":
        # return render_template("index.html")
        email = request.form.get("email")
        password = request.form.get("password")
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO Admin ('Email', 'Password')\
                    VALUES (?,?)",(email, password) )
        conn.commit()
        conn.close()
        message = str(email)
        resourceUrl = getResources()
        img = getImage()
        return render_template("home.html", message = message, url = resourceUrl, imageName=img, msg = '')

# @app.route ("/hello/emailLog", methods="[GET]")
# def emailLog():
#     email = request.form.get("Email")
#

def getResources():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT url FROM tbl_Resources")
    # cur.execute("SELECT * FROM Customers WHERE surname=? AND public = 'True';", [surname])
    data = cur.fetchall()
    conn.close()
    return data

def getImage():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT image FROM tbl_Resources')
    # max_id = cur.fetchone()[0]
    data = cur.fetchall()
    conn.close()
    return data


if __name__ == "__main__":
    # createDB()
    # populateCustomers()
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=8080)
