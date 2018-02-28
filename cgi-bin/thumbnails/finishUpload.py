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
if 'HTTP_COOKIE' in os.environ:
  cookies = os.environ['HTTP_COOKIE'].split('; ')
  for cookie in cookies:
    cookie = cookie.split('=')
    if cookie[0] == 'session':
      session = int(cookie[1],10)
    if cookie[0] == 'uploadImage':
      savedFileName = str(cookie[1])
#check the user name by the session id
query = "SELECT username FROM session WHERE sessionId="+str(session)
cursor.execute(query)
result = cursor.fetchone()
userName="public"
if result is not None:
  userName = result[0]

#read privacy setting
form = cgi.FieldStorage()
privacy = form.getvalue('privacy')

#html
print ("Content-type:text/html\r\n\r\n")
print ("<html><head>")
print ("<title>Web Instagram</title>")
print ("</head>")
print ("<body>")

#Save the image file and display it
with Image(filename="/CSCI4140/xampp/htdocs/temp/temp.jpg") as img:
#Update database for the photolist depends on the privacy
#set as public if it is
  if privacy == 'public':
    data = {'imageName': savedFileName, 'userName': userName, 'privacy': 'public'}
  else:
    data = {'imageName': savedFileName, 'userName': userName, 'privacy': userName}
  query = ("INSERT INTO photo (imageName, userName,privacy) VALUES (%(imageName)s, %(userName)s, %(privacy)s)")
  cursor.execute(query,data)
  userdb.commit()
#Check the id of the image
  query=("SELECT id from photo WHERE userName='"+userName+"' AND imageName='"+savedFileName+"'")
  cursor.execute(query)
  result = cursor.fetchone()
  imageId = result[0]
#save image
  img.format = 'jpeg'
  img.save(filename="/CSCI4140/xampp/htdocs/"+str(imageId)+".jpg")
  img.resize(200,200)
  img.save(filename="/CSCI4140/xampp/htdocs/thumbnails/"+str(imageId)+".jpg")
#update database
  query=("UPDATE photo SET imageName = %(imageName)s WHERE id=%(id)s")
  data = { 'id': str(imageId), 'imageName': str(imageId)+".jpg"}
  cursor.execute(query,data)
  userdb.commit()
#remove temp
  os.remove('/CSCI4140/xampp/htdocs/temp/temp.jpg')
  os.remove('/CSCI4140/xampp/htdocs/temp/'+savedFileName)
#PRINT LINK
  print ("<a href='/"+str(imageId)+".jpg"+"'>permalink: /"+str(imageId)+".jpg"+"</a>")
  print ("<br><a href='/index.py'>Back to album</a>")
  print ("<img src='/thumbnails/"+str(imageId)+".jpg"+"'width=200px height=200px><br>")
cursor.close()
userdb.close()
print ("</body></html>")