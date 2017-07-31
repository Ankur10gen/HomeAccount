from pymongo import MongoClient

client = MongoClient()
account_db = client['account_db']

class DatabaseConnection:

    """
    This class provides access to the MongoDB database using a single MongoClient defined above.
    """

    """Access to Database

    def insert_document(document, collection_name):
        try:
            account_db[collection_name].insert_one(document)
        except ConnectionError as ce:
            print("Couldn't establish a connection to the database.\n"
                  " The error is {0}. The type of error is {1}".format(ce, type(ce)))
        except pymongoerrors.DuplicateKeyError as dke:
            print("Please enter a unique ID.")
        except Exception as e:
            print(e, type(e))
    """

    @staticmethod
    def get_collection(collection_name):

        """
        This method will help in setting a collection for CRUD operations.
        
        :param collection_name: 
        :return: 
        """
        return account_db[collection_name]

if __name__=='__main__':
    db = DatabaseConnection()

