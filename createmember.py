from util.databaseconnection import DatabaseConnection as dbconn
from util.password_manipulation import *
from util.member import Member

def create_member():
    """
    This methods helps register a new member to the application.
    
    :return: 
    """
    from homepage import home_page # The import statement was put here to resolve circular dependency

    try:
        while True:
            username = input("Enter a unique username: ")
            check_db_for_user = dbconn.get_collection('members').find_one({"_id": username})
            if check_db_for_user:
                print("Username {0} already exists. Choose a different username.".format(username))
            else:
                break
        name = input("Enter your name: ")
        password = input("Enter Password: ")
        hashed_password = hash_the_password(password)
        member_obj = Member(username, name, hashed_password)
        member_obj.save_member()
        print("Your account has been created.")
        home_page()
    except Exception as e:
        print(e, type(e))