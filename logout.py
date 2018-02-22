#!D:/CSCI4140/python/python-3.5.4.amd64/python
import cgi, cgitb, os, random
import mysql.connector

#connect to the data basestring
userdb = mysql.connector.connect(user='alan', password='alansuen',host='localhost',database='accountdata')
cursor = userdb.cursor()

#check if the user login or not
session = 0
if 'HTTP_COOKIE' in os.environ:
  cookies = os.environ['HTTP_COOKIE'].split('; ')
  for cookie in cookies:
    cookie = cookie.split('=')
    if cookie[0] == 'session':
      session = int(cookie[1],10)
query = "SELECT username FROM session WHERE sessionId="+str(session)
cursor.execute(query)
result = cursor.fetchone()
if result is not None:
#delete session from database
  query = ("DELETE FROM session WHERE sessionId="+str(session))
  cursor.execute(query)
  userdb.commit()
#Update cookie
print ("Set-Cookie:session = 0;")

print ("Content-type:text/html\r\n\r\n")
print ("<html><head>")
print ("<title>Web Instagram</title>")
print ("</head>")
print ("<body>")
print ("<p>You has successfully log out.</p>")
print ("<a href='/index.py'>Back to homepage</a>")
print ("</body></html>")