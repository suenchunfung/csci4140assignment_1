#!D:/CSCI4140/python/python-3.5.4.amd64/python
import cgi, cgitb
import mysql.connector

#connect tio the data basestring
userdb = mysql.connector.connect(user='alan', password='alansuen',host='localhost',database='accountdata')

#html
print ("Content-type:text/html\r\n\r\n")
print ("<html><head>")
print ("<title>Web Instagram</title>")
print ("</head>")
print ("<body>")
print ("<h2>Create your account<h2><br>")
#Form for user enter his information
print ("<form action='/register.py' method='POST'> \
        User name: <input type='text' name='userName'><br> \
		Password: <input type='password' name='password'><br> \
		Re-enter password: <input type='password' name='pswConfirm'><br> \
		<input type='submit' value='Register'>")


print ("</body></html>")