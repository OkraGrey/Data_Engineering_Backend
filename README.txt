-- TO START WITH USING THIS PROJECT --

    1- Install required Packages using
    pip install -r requirements.txt

    2- Create a .env file in the main folder and add your DB credentials
    You need to add your own values for Host, user, password and Database.
                            For Example 
                            HOST='localhost'
                            USER='root'
                            PASSWORD='1234'
                            DATABASE='DataEng'
    
    3- Open the main.py file
    In the Search function, pass your arguments

    4- Open Console (Ctrl + J) in Vs Code
    Type python main.py
    Boom

    5- You will barely find any Print Statements in the Code
    For any issue, please read the logs in the logs folder
    Every file has its own log file and logs are written in the following pattern
    [TIME][FILE NAME][LOGGING LEVEL]-[MESSAGE]
    [2025-05-14 10:46:50,177][FILE:__main__][INFO]-[Calling Search Endpoint ]
