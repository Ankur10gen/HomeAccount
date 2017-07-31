from util.databaseconnection import DatabaseConnection as dbconn
from util.group import Group
from pymongo import errors as pymongoerrors
import session
from util.expenditure import Expenditure
from datetime import datetime

group_details = '' # Global Variable recording the details for the group
group_selection = '' # Global Variable to keep record of the currently selected group_id

def add_expense():

    """
    This method helps a member of the group to submit an expense.
    
    :return: 
    """
    group_operation = int(input('Enter 1 to add expense, 2 to add members. '))
    if group_operation == 1:
        amount_spent = int(input('Enter the amount (rounded off): '))
        shared_between = group_details['members_list']
        print('This expense will be shared by: {0}'.format(shared_between))
        shared_between_approval = int(input('Hit 1 to Approve or 2 to change list'))

        def share_expense():
            nonlocal shared_between_approval
            nonlocal shared_between
            if shared_between_approval == 1:
                Expenditure.save_expenditure(group_selection, session.user_details['_id'], amount_spent, datetime.utcnow(),
                                         shared_between)
                print('Expense saved successfully')
            elif shared_between_approval == 2:
                shared_between = input('Provide list of members to share the expense: ')
                print('This expense will be shared by: {0}'.format(shared_between))
                shared_between_approval = int(input('Hit 1 to Approve or 2 to change list'))
                share_expense()
        share_expense()

    elif group_operation == 2:
        member_list = input('Enter the members to add')
        Group.add_members_to_group(group_selection,member_list)
        print('Members added successfully')

def after_login():

    """
    This method helps render the page after login is successful
    and ask for further inputs.
    
    :return: 
    """

    after_login_page_choice = int(input("Enter 1 to check an existing group \n"
                                  "Enter 2 to create a new group \n"
                                  "Enter 3 to LogOut \n"))

    if after_login_page_choice == 1:
        if len(session.user_details['member_of_groups']) == 0:
            print("You are currently not a member of any group.")
            after_login()
        else:
            print("You are member of groups {0}".format(session.user_details['member_of_groups']))

        while True:
            global group_selection
            group_selection = input("Which group would you like to check? Enter 1 to go back ")
            if group_selection == 1:
                after_login()
            elif group_selection not in session.user_details['member_of_groups']:
                print("You are not a member of this group.")
                after_login()
            else:
                print("Here are the details from this group: \n")
                global group_details
                group_details = Group.get_group_details(group_selection)
                print(group_details)
                add_expense()

    elif after_login_page_choice == 2:
        print("Ok {0}. Let's create a new group for you.".format(session.user_details['name'].split()[0]))
        while True:
            try:
                group_id = input('Enter a unique group ID: ')
                group_name = input('Enter a group name: ')
                Group.save_group(group_id, group_name, [session.user_details["_id"],], [session.user_details["_id"],])
                session.user_details = dbconn.get_collection('members')\
                    .find_and_modify(
                    query={"_id": session.user_details['name']},
                    update={"$addToSet": { "member_of_groups": group_id}},
                    new=True)
                after_login()
            except pymongoerrors.DuplicateKeyError:
                break
            except Exception as e:
                print(e, type(e))

    elif after_login_page_choice == 3:
        print("LOGGED OUT")
        from homepage import home_page
        home_page()
