-- TO START WITH USING THIS PROJECT --


    1- Create a virtual environment using
    python -m venv env

    2- Install required Packages using
    pip install -r requirements.txt

    3- Create a .env file in the main folder and add your DB credentials
    You need to add your own values for Host, user, password and Database.
                            For Example 
                            HOST='localhost'
                            USER='root'
                            PASSWORD='1234'
                            DATABASE='DataEng'
    
    4- In the App.py file, there is a function called wrapper
    Import this function in your frontend/testing file and pass two arguments
        1- County, 2- Key
    
    5- Open Console (Ctrl + J) in Vs Code
    Type python {file_name}.py
    Boom

    6- You will barely find any Print Statements in the Code
    For any issue, please read the logs in the logs folder
    Every file has its own log file and logs are written in the following pattern
    [TIME][FILE NAME][LOGGING LEVEL]-[MESSAGE]
    [2025-05-14 10:46:50,177][FILE:__main__][INFO]-[Calling Search Endpoint ]


    # Note : This setup uses mysql Database and expects the required tables to be present in the used DB.
