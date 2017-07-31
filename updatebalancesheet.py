from util.databaseconnection import DatabaseConnection as dbconn
from pymongo import errors as pymongoerrors
from bson import ObjectId
from datetime import datetime

def update_balance_sheet(group_id):

    """
    This method helps in updating the balance sheet and settling all the expenses for a group
    since the last settlement was done.
    
    :param group_id: 
    :return: 
    """

    group_details = dbconn.get_collection('groups').find_one({"_id":group_id})
    print("Running Split Job on {0} after time {1}".format(group_details['group_name'],group_details['last_settlement_on']))

    for expense in dbconn.get_collection('expenditures').find(
            {'group_id': group_id, 'time':{'$gt':group_details['last_settlement_on']} }):

        split_expense = expense['amount']/len(expense['shared_between'])
        lender = expense['member_id']
        borrower_set = set(expense['shared_between']) - set(lender)
        for borrower in borrower_set:

            '''
            db.members.update(
                {'_id':'nir', 'borrowing.group_id':'grp_tst','borrowing.member_id':'tst1'}
                ,{$inc:{'borrowing.$.amount':100}}
				,{upsert:true}
				)
				
			db.members.update(
				{'_id':'nir'}
				,{'$addToSet': {'borrowing':{ 'group_id':'grp_tst','member_id':'tst1','amount':100}}}
				)

            '''

            try:
                dbconn.get_collection('members')\
                    .update_one(
                    {'_id':borrower, 'borrowing.group_id':group_id,'borrowing.member_id':lender}
                    ,{'$inc':{'borrowing.$.amount':split_expense}})
            except pymongoerrors.WriteError.code == 16836:
                print('You have never borrowed from this person. Running alternate update command.') # Added for testing
                dbconn.get_collection('members')\
                    .update_one(
                    {"_id":borrower}
                    ,{'$addToSet': {'borrowing':{'group_id':group_id,'member_id':lender,'amount':split_expense}}})

        dbconn.get_collection('expenditures').update_one({'_id':ObjectId(expense['_id'])},{'$set':{'settled':True}})
    dbconn.get_collection('groups').update_one({"_id":group_id}, {'$set': {'last_settlement_on':datetime.utcnow()}})

if __name__=='__main__':
    update_balance_sheet('grp_tst')





