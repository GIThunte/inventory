#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The logger function
"""
def logger(data):
    print(data)
    
"""
This function for return some data from mongodb
get collection object and will return all data
from collection
"""
def get_mongo_data(collection_obj):
    try:
        return [x for x in collection_obj.find({}, {'_id': False})]
    except Exception as e:
        logger(e)

"""
Function for update db data, get username, object
mongo collection and new data for set in db, this
function will return count changes
"""
def update_db_data(username, collection_obj, new_data):
    try:
        update_obj = {'pattern': {'UserName': username},
                                      'new_count': { "$set": new_data }}
        update_result = collection_obj.update_one(update_obj['pattern'], update_obj['new_count'])
        return update_result.modified_count
    except Exception as e:
        logger(e)

"""
Function for add new mongo data in db, get colelction object
and data for insert
"""
def add_mongo_data(m_collection, mongo_data):
    try:
        m_collection.insert_one(mongo_data)
    except Exception as e:
        logger(e)

"""
Function for delete data, pattern for delete username
also for working whis function needed collection object
"""
def delete_mongo_data(m_collection, delete_user):
    try:
        m_collection.delete_one({'UserName': delete_user})
    except Exception as e:
        logger(e)

"""
The defaul check
"""
if __name__ == '__main__':
    pass
    