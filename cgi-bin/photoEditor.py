#!D:/CSCI4140/python/python-3.5.4.amd64/python
import cgi, cgitb, os
import mysql.connector
from os import environ
from wand.image import Image
from wand.image import COMPOSITE_OPERATORS
from wand.drawing import Drawing
from wand.display import display
import wand

cgitb.enable()

#connect to the data basestring
userdb = mysql.connector.connect(user='alan', password='alansuen',host='localhost',database='accountdata')
cursor = userdb.cursor()

#Read cookie
session = 0
savedFileName ='error'
storedPrivacy = 'error'
if 'HTTP_COOKIE' in os.environ:
  cookies = os.environ['HTTP_COOKIE'].split('; ')
  for cookie in cookies:
    cookie = cookie.split('=')
    if cookie[0] == 'session':
      session = int(cookie[1],10)
    if cookie[0] == 'uploadImage':
      savedFileName = str(cookie[1])
    if cookie[0] == 'privacy':
      storedPrivacy = str(cookie[1])
#check the user name by the session id
query = "SELECT username FROM session WHERE sessionId="+str(session)
cursor.execute(query)
result = cursor.fetchone()
userName="public"
if result is not None:
  userName = result[0]
#read the upload photo
form = cgi.FieldStorage()
filter = form.getvalue('filter')
privacy = form.getvalue('privacy')
uploadState = False
#Set cookies
if not privacy:
  print ("Set-Cookie:privacy = "+storedPrivacy+";")
else:
  print ("Set-Cookie:privacy = "+privacy+";")
  storedPrivacy = privacy

#upload when filter is none
if not filter:
  photo = form['uploadedPhoto']
  if photo.filename:
    savedFileName = os.path.basename(photo.filename)
    open("/CSCI4140/xampp/htdocs/temp/"+savedFileName,'wb').write(photo.file.read())
    print ("Set-Cookie:uploadImage = "+savedFileName+";")
    uploadState = True
#html
print ("Content-type:text/html\r\n\r\n")
print ("<html><head>")
print ("<title>Web Instagram</title>")
print ("</head>")
print ("<body>")
print ("<p>Filters <a href='/photoEditor.py?filter=Border'>Border</a>  \
           <a href='/photoEditor.py?filter=Lomo'>Lomo</a>   \
           <a href='/photoEditor.py?filter=flare'>Lens flare</a>  \
           <a href='/photoEditor.py?filter=BW'>Black White</a>  \
           <a href='/photoEditor.py?filter=blur'>blur</a></p>")
with Image(filename="/CSCI4140/xampp/htdocs/temp/"+savedFileName) as img:
  if not filter :
    print ("<img src='/temp/"+savedFileName+"' width=200px height=200px>")
  else:
    print("<h2>"+savedFileName+"</h2>")
    if filter == 'original':
      src = Image(filename="/CSCI4140/xampp/htdocs/temp/"+savedFileName)
      src.format = 'jpeg'
      src.save(filename="/CSCI4140/xampp/htdocs/temp/"+"temp.jpg")
      print ("<img src='/temp/temp.jpg' width=200px height=200px>")
    if filter == 'Border':
      img.border(wand.color.Color('black'),50,50)
      img.format = 'jpeg'
      img.save(filename="/CSCI4140/xampp/htdocs/temp/"+"temp.jpg")
      print ("<img src='/temp/temp.jpg' width=200px height=200px>")
    if filter =='Lomo':
      img.level(black=0.33,channel = 'red')
      img.level(black=0.33,channel = 'green')
      img.format = 'jpeg'
      img.save(filename="/CSCI4140/xampp/htdocs/temp/"+"temp.jpg")
      print ("<img src='/temp/temp.jpg' width=200px height=200px>")
    if filter == 'flare':
      flare = Image(filename="/CSCI4140/flare.png")
      img.composite(left=0, top=0, image=flare)
      img.format = 'jpeg'
      img.save(filename="/CSCI4140/xampp/htdocs/temp/"+"temp.jpg")
      print ("<img src='/temp/temp.jpg' width=200px height=200px>")
    if filter == 'BW':
      img.type = 'grayscale'
      img.format = 'jpeg'
      img.save(filename="/CSCI4140/xampp/htdocs/temp/"+"temp.jpg")
      print ("<img src='/temp/temp.jpg' width=200px height=200px>")
    if filter == 'blur':
      img.gaussian_blur(5,2)
      img.format = 'jpeg'
      img.save(filename="/CSCI4140/xampp/htdocs/temp/"+"temp.jpg")
      print ("<img src='/temp/temp.jpg' width=200px height=200px>")
#print the bottom panel
print("<p><a href='/photoEditor.py?filter=original'>Undo </a><a href='/index.py'>Discard </a><a href='/finishUpload.py?privacy="+storedPrivacy+"'>Finish</a>")
#wizard = Image(filename="/CSCI4140/xampp/htdocs/public/Taken_with_Xperia_3.jpg")
#rose = Image(filename="/CSCI4140/flare.png")
#w = wizard.clone()
#r = rose.clone()
#w.composite(left=0, top=0, image=r)
#w.border(wand.color.Color('red'),10,10)
#w.gaussian_blur(5,2)
#w.format = 'jpeg'
#w.save(filename="/CSCI4140/xampp/htdocs/"+userName+"/"+"temp.jpg")
print ("</body></html>")
