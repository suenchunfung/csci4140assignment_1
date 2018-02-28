1. Directory "temp" store the temporary files of the photo editor when doing uploading and editing    of the images.
2. Directory "thumbnails" store the thumbnails of all the uploaded image in order to let the album    page load faster
3.  I use MYSQL as database and wand as image procsesing.  
4.1 First install XAMPP 
4.2 Then install imagemagick
4.3 Then intall "wand" by "pip install Wand"
4.4 Then intall "mysql-connector" by "pip install mysql-connector"
5. I cannot finish the image type checking because I cannot find a function.
6. Two empty folders "temp" and "thumbnails" should be created first under the "cgi-bin"
7. A database called "accountdata" should be created first before running the server.
8. Three tables("photo", "account","session in "accountdata" should be created first.
   By following commands:
   CREATE TABLE account (username varchar(255), password varchar(255));
   CREATE TABLE session (sessionId int, username varchar(255));
   CREATE TABLE photo (id int NOT NULL AUTO_INCREMENT, imageName varchar(255), userName varchar(255), privacy varchar(255));
9. Sorry for not finishing the Initialise part since I cannot finish it before the deadline.
