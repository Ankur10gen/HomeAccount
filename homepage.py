from loginpage import login_member
from pageafterlogin import after_login
from createmember import create_member

def home_page():
    """
    This function serves the main page of the application and further calls upon other functions based on 
    user responses.
    :return: 
    """
    while True:
        try:
            home_page_choice = int(input("Enter 1 for Log In \n"
                               " 2 for Sign Up. \n"))
            if home_page_choice==1:
                print("======LOG IN FORM======")
                login_member()
                after_login()
            elif home_page_choice==2:
                print("======WELCOME TO THE REGISTRATION PAGE======")
                create_member()
                break
            else:
                print("Oh! Wrong input. Try again.")
        except ValueError:
            print("Wrong Input Type")
        except Exception as e:
            print(e, type(e))
