from datetime import datetime

from pymongo import errors as pymongoerrors

from util.databaseconnection import DatabaseConnection as dbconn


class Member:
    """
    This class will help add members to the application
    
    The user will register as a member of the application.
    """

    def __init__(self, member_id, name, password):
        self._member_id = member_id
        self._name = name
        self._password = password
        self._lending = {}
        self._borrowing = {}
        self._member_of_groups = []

    def save_member(self):
        """
        This method will save the member in the database

        Exception: ConnectionError or Generic Exception with exception error and type 
        """
        try:
            doc = {"_id": self._member_id, "name": self._name, "password": self._password, "added_on": datetime.utcnow(), "member_of_groups": self._member_of_groups}
            dbconn.get_collection('members').insert_one(doc, 'members')
        except pymongoerrors.DuplicateKeyError:
            print("Oops! User ID is already taken.")
        except Exception as e:
            print(e, type(e))

    def get_member_info(self):
        """
        This method will return the details for the member
        :return: Member Details
        """
        return dbconn.get_collection('members').find_one({"_id": self._member_id})


