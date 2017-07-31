from util.databaseconnection import DatabaseConnection as dbconn


class Expenditure:

    """
    This class will provide a template for an expense.
    An expense is reported by a member for a particular group.
    One expense will be reported by one person and the amount may be split in group members.
    Person reporting the expense will be the LENDER while other the members who will share 
    that expense will be the BORROWERS.
    """

    def __init__(self, group_id, member_id, amount, time, shared_between):
        self._group_id = group_id
        self._member_id = member_id
        self._amount = amount
        self._time = time
        self._shared_between = shared_between

    @staticmethod
    def save_expenditure(group_id, member_id, amount, time, shared_between):
        """
        This method saves the expenditure to the database.
        
        :param group_id: 
        :param member_id: 
        :param amount: 
        :param time: 
        :param shared_between: 
        :return: 
        """
        try:
            doc = {"group_id": group_id, "member_id": member_id, "amount": amount, "time": time,
                   "shared_between": shared_between}
            dbconn.get_collection('expenditures').insert_one(doc)
        except Exception as e:
            print(e, type(e))