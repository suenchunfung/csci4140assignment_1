#!D:/CSCI4140/python/python-3.5.4.amd64/python
import cgi, cgitb
import mysql.connector
import os

#connect tio the data basestring
userdb = mysql.connector.connect(user='alan', password='alansuen',host='localhost',database='accountdata')
cursor = userdb.cursor()

#get user 's entry
form = cgi.FieldStorage()
uName = form.getvalue('userName')
password = form.getvalue('password')
pswConfirm = form.getvalue('pswConfirm')

#html
print ("Content-type:text/html\r\n\r\n")
print ("<html><head>")
print ("<title>Web Instagram</title>")
print ("</head>")
print ("<body>")

#Register user
##Check if the password enter correct or not
if pswConfirm != password:
  print ("<h2>Error</h2><h4>re-entered password is not the same</h4>")
  print ("<a href='/createAccount.py'>back</a>")
else:
##Search if the user name is already in user
  query = ("SELECT username FROM account WHERE username='"+uName+"'")
  cursor.execute(query)
  row = cursor.fetchone()
  if row is not None:
    print ("<h2>Error</h2><h4>The user name is already in used</h4>")
    print ("<a href='/createAccount.py'>back</a>")
  else:
    newUser = ("INSERT INTO account (username, password) VALUES (%(username)s, %(password)s)")
    data = { 'username': uName, 'password': password} 
    cursor.execute(newUser,data)
    userdb.commit()
#create directory for the user
#    if not os.path.exists('/CSCI4140/xampp/htdocs/'+uName):
#      os.makedirs('/CSCI4140/xampp/htdocs/'+uName)
#    if not os.path.exists('/CSCI4140/xampp/htdocs/'+uName+'/thumbnails'):
#      os.makedirs('/CSCI4140/xampp/htdocs/'+uName+'/thumbnails')
    print ("<h2>Create user account success.</h2>")
    print ("<a href='/index.py'>back</a>")
cursor.close()
userdb.close()
print ("</body></html>")