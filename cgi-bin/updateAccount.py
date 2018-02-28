#!D:/CSCI4140/python/python-3.5.4.amd64/python
import cgi, cgitb, os, random
import mysql.connector
from os import environ
import os

#connect tio the data basestring
userdb = mysql.connector.connect(user='alan', password='alansuen',host='localhost',database='accountdata')
cursor = userdb.cursor()

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

print ("Content-type:text/html\r\n\r\n")
print ("<html><head>")
print ("<title>Web Instagram</title>")
print ("</head>")
print ("<body>")
#Form for user update his pasword
print ("<form action='/update.py' method='POST'> \
        Current password: <input type='password' name='password'><br> \
        New password: <input type='password' name='newPassword'><br> \
        Re-enter password: <input type='password' name='pswConfirm'><br> \
        <input type='submit' value='Update'>")

print ("</body></html>")