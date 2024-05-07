@echo off
rem Frontend React
call .venv\Scripts\activate
cd .\react-spa-template-master\
start npm start

rem Backend Flask
call .venv\Scripts\activate
cd ..\flask_server\
start cmd /k flask run --debug