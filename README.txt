CPSC 449 Project 2 Group 8

Group Members:
Yi Wei
Gregory Pierot

Work included in TAR file:

Folder "bin"
- Contains the init.sh and post.sh 
- First contains code for sqlite3 and the second
contains code for http posting

Folder "etc"
- Contains api.ini, logging.ini, and timelines.ini
- Api.ini and timelines.ini contain code for sqlite3 db
- Logging.ini contains a simple logging configuration for python

Folder "share"
- Contains timelines.sql and users.sql which have sql code to generate
the schema for each respective db.
- Contains json files for reading or posting.

Folder "var"
- Contains the log folder which hold the logs from the api.

File ".env"
- Simple file for python buffering

File "Procfile"
- Declares the commands to be run on the container.
- It binds the connection and port as well as debugging

File "api.py"
- Contains all the user defined services for the application such as;
"createuser", "checkpassword", "getfollower", ect.
- Has error handling for post and get
- The "meat" part of the project

File "timelines.py"
- Contains functions for retireving and appening data from the db.
- Functions such as; "query", "usertime", and "userpost".
- The "potatoes" part of the project.

How to Run:
- Navigate to the directory CPSC449_Project2_Group8
- Open two terminals
- In the first terminal run: "./bin/init.sh"
- Once the db is initialized run: "foreman start"
- The first terminal is on port 5000 and the second port 
is on 5100.
- With the second terminal you can make requests to the first terminal
and receive responses.