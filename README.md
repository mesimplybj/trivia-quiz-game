# Trivia quiz game

[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![GitHub license](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=flat-square)](https://github.com/mesimplybj/trivia-quiz-game/blob/master/LICENSE.txt)

The main aim of this game is to create  a multiplayer trivia game app, with rules loosely based on the popular  [HQ Trivia](https://en.wikipedia.org/wiki/HQ_(game))

## Overview
This project is developed in python using Django Framework. The websockets are  implemented using the django Channels. BackgroundScheduler is use to schedule the time of server to send the questions accross the connected clients.

[Client Flow chart](https://github.com/mesimplybj/trivia-quiz-game/blob/master/Documentation/user%20workflow.jpg)
[Admin Flow chart](https://github.com/mesimplybj/trivia-quiz-game/blob/master/Documentation/Listener%20engine.jpg)

# [Demo link ](https://trivia-quiz-game-bj.herokuapp.com/)
#### How to play the game
* After the page landing page is loaded
* Enter your name
* Choose a group  and wait untill other user join the game
* As soon as other user joins the game , questions are asked from the server with four options. 
* Question are  consume from https://opentdb.com/ .
* As everyone levels up the difficulty of the question also rises
* The last standing person will be the winner

Locally or in Demo you can join a room from different browser  at same time and  play the game. To test i hava set the maximum user connection to 3 which can be change later.

## Quickstart

##### Deploy in [Heroku](https://www.heroku.com/)
If you want to deploy this application in heroku,
* first fork this project
* create an app  in heroku ,
* go to  deploy tab   
* choose github  as deployment metho, 
* create a malual deploy or  automatic deploys 
* Change the connection string  of postgresql
* Alternatively, if you have redis module you can use that in channel(not all functionalities are implemented)
* After succesfull deployment your trivia-quiz-game is ready to go 

##### Deploy app locally
If you want to run the app locally clone or download the projec in the local folder. Then, open an instance of terminal and cd to the project’s file path, e.g
```bash
cd Users/User/Desktop/Trivia_Quiz_Game
```
##### System requirements
* python 3.6 or above 
* pip3
* virtualenv module

create a virtual environment  
```bash
C:\Users\Bijaya\Desktop\Trivia_Quiz_Game>virtualenv triviagame
```
activate the virtual environment just created
```bash
C:\Users\Bijaya\Desktop\Trivia_Quiz_Game>triviagame\scripts\activate

(triviagame) C:\Users\Bijay\Desktop\Trivia_Quiz_Game>
```

 Install all the requirement for the project by  this command. This will install the  required module  in  your triviagame environment
```bash
(triviagame) C:\Users\Bijay\Desktop\Trivia_Quiz_Game>pip3 install -r requirements.txt
```
After the succesfull installation of every modules, now its time to run the  project. To do so run following command
```bash
(triviagame) C:\Users\Bijay\Desktop\Trivia_Quiz_Game>python manage.py runserver 8090
```
Create a database in postgreqlserver and add create table from from database query file inside script folder and change the connection string

Then  your game is ready to go at  (http://127.0.0.1:8090/). If your 8090 is already in use then change the port and run the command

##### Features in scope 
requirements that are developed during this project are
* User can choose any quiz to play
* Each quiz starts when the user  number reach to 100 (or less for test purpose)
* Statistics should be show for each question of a quiz
* Level of hardness of the quiz must be increase
* Questions are taken from  open trivia database https://opentdb.com/
* Last player standing in the quiz is declare as winner
* Anyone can leave the quiz anytime
* Time to solve each question is 10 sec
* Simple design
* The application runs in completely  automatic mode
* Multiple game can be played simultaneously

##### Features out of scope
requirements that are not  developed during this project are
* user registration and mangement
* user logs

##### Keynotes from  the project
* Python
* Django
* Django channels
* Python scheduler
* Redis
* PostGreSQL