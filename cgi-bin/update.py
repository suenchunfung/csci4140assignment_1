#!D:/CSCI4140/python/python-3.5.4.amd64/python
import cgi, cgitb, os, random
import mysql.connector
from os import environ
import os

#connect tio the data basestring
userdb = mysql.connector.connect(user='alan', password='alansuen',host='localhost',database='accountdata')
cursor = userdb.cursor()

#get user 's entry
form = cgi.FieldStorage()
password = form.getvalue('password')
newPassword = form.getvalue('newPassword')
pswConfirm = form.getvalue('pswConfirm')

userName = 'public'
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

#Check for the correctness of the password
query = "SELECT password FROM account WHERE username='"+userName+"'"
cursor.execute(query)
passwordVal = cursor.fetchone()
validation = False
if passwordVal is not None:
  if password == passwordVal[0]:
    validation = True
#html
print ("Content-type:text/html\r\n\r\n")
print ("<html><head>")
print ("<title>Web Instagram</title>")
print ("</head>")
print ("<body>")
if validation == True:
##Check if the password enter correct or not
  if pswConfirm != newPassword:
    print ("<h2>Error</h2><h4>re-entered password is not the same</h4>")
    print ("<a href='/updateAccount.py'>back</a>")
  else:
    query = ("UPDATE account SET password = %(password)s WHERE username=%(username)s")
    data = { 'username': userName, 'password': newPassword}
    cursor.execute(query,data)
    userdb.commit()
    print ("<h2>Update user password success.</h2>")
    print ("<a href='/index.py'>back</a>")
else:
  print("<h2>Current password wrong!<h2>")
  print ("<a href='/updateAccount.py'>back</a>")
cursor.close()
userdb.close()
print ("</body></html>")








