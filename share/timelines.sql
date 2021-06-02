PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  username VARCHAR NOT NULL PRIMARY KEY ,
  email VARCHAR NOT NULL,
  password VARCHAR NOT NULL,
  UNIQUE(username,email,password)

);

DROP TABLE IF EXISTS followers;
CREATE TABLE followers (
  username VARCHAR,
  follow VARCHAR,
  FOREIGN KEY(username) REFERENCES users(username),
  FOREIGN KEY(follow) REFERENCES uers(username)
);

DROP TABLE IF EXISTS timelines;
CREATE TABLE timelines{
  username VARCHAR NOT NULL PRIMARY KEY,
  post VARCHAR,
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(username) REFERENCES users(username)

};

INSERT INTO users(username, email, password) VALUES('AAA','AAA123@gmail.com','qqqa');
INSERT INTO users(username, email, password) VALUES('BBB','BBB123@gmail.com','azsdf');
INSERT INTO users(username, email, password) VALUES('CCC','CCC123@gmail.com','cccvddf');
INSERT INTO followers(username, follow) VALUES ('AAA','BBB');
INSERT INTO followers(username, follow) VALUES ('BBB','CCC');
INSERT INTO followers(username, follow) VALUES ('AAA','CCC');
INSERT INTO timelines(username,post) VALUES('AAA','I am student')
INSERT INTO timelines(username,post) VALUES('BBB','go and watch Attack on Titan')
INSERT INTO timelines(username,post) VALUES('CCC', 'go and sleep')
