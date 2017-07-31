from util.databaseconnection import DatabaseConnection as dbconn
from util.password_manipulation import *
import session

def login_member():
    """
    This method helps the registered user to login to the application
    
    :return: 
    """

    try:
        while True:
            username = input("Enter your username: ")
            user_password = input("Enter your password: ")
            check_db_for_user = dbconn.get_collection('members').find_one({"_id":username})
            if check_db_for_user is None:
                print("User doesn't exist.")
            else:
                hashed_password = check_db_for_user['password']
                if check_password(hashed_password, user_password):
                    print("Great! Your details match our records.")
                break
        session.user_details = check_db_for_user
        print("Hello, {0}. Here are your account details: \n".format(session.user_details['name'].split()[0]))
        print(check_db_for_user) # Fix Password being showed to user
    except Exception as e:
        print(e, type(e))