from pymongo import errors as pymongoerrors

from util.databaseconnection import DatabaseConnection as dbconn


class Group:
    """
    This class will help setting up a group
    
    A member can create a group and add more members to it.
    """

    def __init__(self, group_id, group_name):
        self._group_id = group_id
        self._group_name = group_name
        self._member_list = []
        self._admin_list = []
        self._last_split = ''

    @staticmethod
    def save_group(group_id, group_name, admin_list, member_list=[]):

        """
        This method is called when creating a new group. This will store information in the database.
        
        :param group_id: 
        :param group_name: 
        :param admin_list: 
        :param member_list: 
        :return: 
        """
        try:
            doc = { "_id":group_id, "group_name": group_name, "members_list":member_list, "admin_list":admin_list}
            dbconn.get_collection('groups').insert_one(doc)
            print("Group Created Successfully")
        except pymongoerrors.DuplicateKeyError:
            print("Oops! User ID is already taken.")
        except Exception as e:
            print(e, type(e))

    @staticmethod
    def add_members_to_group(group_id, member_list):
        """
        This method is called when adding new members to a group.
        
        :param group_id: 
        :param member_list: 
        :return: 
        """
        dbconn.get_collection('groups').update_one({"_id":group_id}, {"$addToSet": {"member_list":member_list}})

    @staticmethod
    def remove_members_from_group(group_id, member_list):
        """
        This method will be called while removing list of members from a group.
        
        :param group_id: 
        :param member_list: 
        :return: 
        """
        dbconn.get_collection('groups').update_one({"_id":group_id}, {"$pull": {"member_list": {"$in":member_list}}})

    @staticmethod
    def get_group_details(group_id):
        """
        Returns the group details from database.
        
        :param group_id: 
        :return: 
        """
        return dbconn.get_collection('groups').find_one({"_id":group_id})