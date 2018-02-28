#!D:/CSCI4140/python/python-3.5.4.amd64/python
import cgi, cgitb, mysql.connector, random

#connect to the data basestring
userdb = mysql.connector.connect(user='alan', password='alansuen',host='localhost',database='accountdata')
cursor = userdb.cursor()

#retrieve user input
form = cgi.FieldStorage()
userName = form.getvalue('userName')
password = form.getvalue('password')
#Check for the correctness of the password
query = "SELECT password FROM account WHERE username='"+userName+"'"
cursor.execute(query)
passwordVal = cursor.fetchone()
validation = False
if passwordVal is not None:
  if password == passwordVal[0]:
    validation = True
#generate session and check if the session is already in use
    session = random.randint(1,100000)
    query = "SELECT sessionId FROM session"
    cursor.execute(query)
    sessionCheck = cursor.fetchone()
    while sessionCheck is not None:  
      while session == sessionCheck[0]:
        session = random.randint(0,100000)
      sessionCheck = cursor.fetchone()
    query = "INSERT INTO SESSION (sessionId, username) VALUES ("+str(session)+",'"+userName+"')"
    cursor.execute(query)
    userdb.commit()
    print ("Set-Cookie:session = "+str(session)+";")
print ("Content-type:text/html\r\n\r\n")
print ("<html><head>")
print ("<title>Web Instagram</title>")
print ("</head>")
print ("<body>")
if validation == True:
  print("<h2>Login Success!<h2>");
  print ("<a href='/index.py'>Back to Album</a>")
else:
  print("<h2>Lohin in fail! User name or password wrong</h2>")
  print ("<a href='/login.py'>Back to login page</a>")
print ("</body></html>")

#db name:accountdata
#table name account