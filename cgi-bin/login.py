#!D:/CSCI4140/python/python-3.5.4.amd64/python
import cgi, cgitb

print ("Content-type:text/html\r\n\r\n")
print ("<html><head>")
print ("<title>Web Instagram</title>")
print ("</head>")
print ("<body>")
print ("<h1>User Login<h1><br>");
print ("<form action='/validation.py' method='post'>")
print ("User name: <input type='text' name='userName'><br>")
print ("Password: <input type='password' name='password'>")
print ("<input type='submit' value='login'></form>")
print ("</body></html>")