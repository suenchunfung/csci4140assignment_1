#!D:/CSCI4140/python/python-3.5.4.amd64/python
import cgi, cgitb, os, random
import mysql.connector
from os import environ
import os

#connect tio the data basestring
userdb = mysql.connector.connect(user='alan', password='alansuen',host='localhost',database='accountdata')
cursor = userdb.cursor()

userName = 'public'
photoList = []
photoUrlList = []
photoIdList = []
#check if the user login or not
session = 0
if 'HTTP_COOKIE' in os.environ:
  cookies = os.environ['HTTP_COOKIE'].split('; ')
  for cookie in cookies:
    cookie = cookie.split('=')
    if cookie[0] == 'session':
      session = int(cookie[1],10)
#if the user has logined, set the userName
if session !=0:
  query = "SELECT username FROM session WHERE sessionId="+str(session)
  cursor.execute(query)
  result = cursor.fetchone()
  if result is not None:
    userName = result[0]
#get the photo list
query = ("SELECT id,imageName FROM photo WHERE privacy='"+userName+"' OR privacy='public'")
cursor.execute(query)
#generate the photoList
record = cursor.fetchone()
while record is not None:
  photoList.append('/thumbnails/'+str(record[1]))
  photoUrlList.append('/'+str(record[1]))
  photoIdList.append(str(record[0]))
  record = cursor.fetchone()
#Calculate for the total page
totalPage = int(photoList.__len__()/8)
if photoList.__len__()%8 > 0:
  totalPage +=1
form = cgi.FieldStorage()
page=form.getvalue('page')
if not page:
  page = 1
  curPhotoIndex = 0
else:
  page = int(page,10)
  curPhotoIndex = (page-1)*8
print ("Content-type:text/html\r\n\r\n")
print ("<html><head>")
print ("<title>Web Instagram</title>")
print ("</head>")
print ("<body>")
print ("<a href='/login.py' position=absolute left:30px margin:10px>Login</a>")
print ("<a href='/createAccount.py' margin:10px>Create Account</a>")
print ("<a href='/updateAccount.py' margin:10px>Update Account</a>")
print ("<a href='/logout.py' margin:10px>Log out</a>")
print ("<p>Login as")
if userName=='public':
  print("Not login")
else:
  print(userName)
print("</p>")
print ("<h2>Welcome to the Web Instagram<h2> \
        <p>Here you can share your photos with the others</p>")
#Display the photos
if curPhotoIndex > 0:
  i = 0
  while i<8 and curPhotoIndex < photoList.__len__():
    print("<div><a href='displayOriginalImage.py?imageId="+photoIdList[curPhotoIndex]+"'><img src='"+photoList[curPhotoIndex]+"' width=200px height=200px margin=20px></a>")
    print("<br><a href='"+photoUrlList[curPhotoIndex]+"'>permalink: "+photoUrlList[curPhotoIndex]+"</a></div>")
    curPhotoIndex += 1
    i += 1
else:
  curPhotoIndex = 0
  i = 0
  while i<8 and curPhotoIndex < photoList.__len__():
    print("<div><a href='displayOriginalImage.py?imageId="+photoIdList[curPhotoIndex]+"'><img src='"+photoList[curPhotoIndex]+"' width=200px height=200px margin=20px></a>")
    print("<br><a href='"+photoUrlList[curPhotoIndex]+"'>permalink: "+photoUrlList[curPhotoIndex]+"</a></div>")
    curPhotoIndex += 1
    i += 1
curPhotoIndex -= 1
#Cal for other page display
prevPage = page - 1
if prevPage < 1:
  prevPage = 1
nextPage = page + 1
if nextPage > totalPage:
  nextPage = totalPage
#print the page info
print ("<br><br>")
print ("<p><h4><a href='/index.py?page="+str(prevPage)+"'>Previous Page</a> " + "Page " + str(page) + " of " + str(totalPage) + " <a href='/index.py?page="+str(nextPage)+"'>Next Page</a></p>")
#Let user to upload file
if session !=0:
  print ("<form enctype= 'multipart/form-data' action = 'photoEditor.py' method = 'post'> \
        <p>Upload Photo <input type = 'file' name = 'uploadedPhoto' /> \
		<input type='submit' value='Upload' /> \
		<input type='radio' name='privacy' value='private'>private</input> \
		<input type='radio' name='privacy' value='public'>public</input></p></form>")

#Allow user to upload photo if he has logined

print ("</body></html>")
