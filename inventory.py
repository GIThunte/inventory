#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------
Author:         Alex Zubov 2020 
Email:          zubovalexandr691@gmail.com
Telegram:       @LordOfFear
Instagram:      @_snake_case
Information:    This application for inventory.
---------------------------------------------------------------
"""
# hard import
import os
import random
import barcodes
import mongo_bridge

# Import from 
from flask import render_template, request, json, redirect, url_for, Flask
from gevent.pywsgi import WSGIServer
from pymongo import MongoClient
from os import environ

# The application object
app = Flask(__name__)

# Vars for application
random_value      = ''.join(str(random.randint(0,9)) for _ in range(12))
app_host          = environ.get('APP_HOST', '0.0.0.0')
app_port          = environ.get('APP_PORT', '5000')
app_mongo_ip      = environ.get('MONGO_IP', '10.1.0.82')
app_mongo_port    = int(environ.get('MONGO_PORT', '27017'))
app_mongo_db      = environ.get('MONGO_DB', 'profiles')
app_mongo_coll    = environ.get('MONGO_COLLECTION', 'inventory_data')
tmp_path          = environ.get('TMP_PATH_DIR', '/tmp')
debug             = environ.get('DEBUG', 'false')
mongo_client      = MongoClient(app_mongo_ip, app_mongo_port)
collection        = mongo_client[app_mongo_db][app_mongo_coll]

"""
When you go to this route, you will see the data 
entry form for inventory. The transition to this
route can be done by going to the application 
address or by redirecting from the functions:
 - delete_data()
 - set_data()
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
When you go to this route, you will see inventory
data for users working remotely. 
"""
@app.route('/remote_users')
def remote_users():
    return render_template('remote_users.html',
                            inventory_data=mongo_bridge.get_mongo_data(collection))

"""
When you go to this route, you will see all inventory
data.
"""
@app.route('/inventory')
def inventory():
    return render_template('inventory.html',
                            inventory_data=mongo_bridge.get_mongo_data(collection))

"""
Internal route for editing inventory data. Using
in functions update_data()
"""
@app.route('/edit_data')
def edit_data():
    return render_template('edit_data.html',
                            edit_user_id=request.args.get('inv_id'),
                            inventory_data=mongo_bridge.get_mongo_data(collection),
                            updated=request.args.get('updated_c'))

"""
Internal route for deleting inventory data
"""
@app.route('/delete_data', methods=['POST', 'GET'])
def delete_data():
    mongo_bridge.delete_mongo_data(collection, request.args.get('inv_id'))
    return redirect(url_for('index'))


"""
The route for get additional information.
Using only for mobile displays
"""
@app.route('/add_info')
def add_info():
    for user in mongo_bridge.get_mongo_data(collection):
        if request.args.get('inv_id') in user['InvID']:   
            return render_template('add_info.html', inventory_data=user)

"""
This route receives the image of the serial number 
of the hard drive, and returns the serial number in 
text form
"""
@app.route('/hdd_sn', methods=['POST', 'GET'])
def hdd_sn():
    return json.dumps({'hdd_serial': barcodes.barcodes_worker(request.files['hdd_sn'],
                                    tmp_path,
                                    random_value)})

"""
This route receives the image of the serial number 
of the monitor, and returns the serial number in 
text form
"""
@app.route('/monitor_sn', methods=['POST', 'GET'])
def monitor_sn():
    return json.dumps({'monitor_serial': barcodes.barcodes_worker(request.files['monitor_sn'],
                                    tmp_path,
                                    random_value)})

"""
Internal route for update inventory data
"""
@app.route('/update_data', methods=['POST', 'GET'])
def update_data():
    inventory_id = request.args.get('InvID')
    
    new_data = {
        'InvID':                inventory_id,
        'UserName':             request.args.get('UserName'),            
        'Room':                 request.args.get('Room'),                
        'Processor':            request.args.get('Processor'),           
        'RAM':                  request.args.get('RAM'),                 
        'Display':              request.args.get('Display'),             
        'DisplaySerialNumber':  request.args.get('DisplaySerialNumber'), 
        'HardDisk':             request.args.get('HardDisk'),            
        'HardDiskSerialNumber': request.args.get('HardDiskSerialNumber'),
        'AdditionalInfo':       request.args.get('AdditionalInfo')      
                        
    }

    update_count = mongo_bridge.update_db_data(inventory_id,
                                               collection,
                                               new_data)
    return(redirect(url_for('edit_data',
                             inv_id=inventory_id,
                             updated_c=update_count)))
    
"""
The route for add inventory data to database.
"""
@app.route('/add_data', methods=['POST', 'GET'])
def set_data():
    if request.method == 'GET':
        count_data      = collection.count() + 1
        inv_type        = request.args.getlist('list')
        username        = request.args.get('username')
        cpu             = request.args.get('cpu')
        memory          = request.args.get('memory')
        monitor         = request.args.get('monitor')
        monitor_sn      = request.args.get('monitor_sn')
        hdd             = request.args.get('hdd')
        hdd_sn          = request.args.get('hdd_sn')
        room_num        = request.args.get('room')
        additional_info = request.args.get('ainfo')

        dict_data =  {
                       'InvID':                   random_value,
                       'UserName':                username,
                       'Room':                    room_num,
                       'Processor':               cpu,
                       'RAM':                     memory,
                       'Display':                 monitor,
                       'DisplaySerialNumber':     monitor_sn,
                       'HardDisk':                hdd,
                       'HardDiskSerialNumber':    hdd_sn,
                       'AdditionalInfo':          additional_info,
                       'type':                    inv_type[0]
                     } 
                        
        mongo_bridge.add_mongo_data(collection, dict_data)
        
        return(redirect(url_for('index')))


# Main check if script module
if __name__ == '__main__':
    if debug == 'true':
        app.run(host=app_host, port=app_port)
    else:
        http_server = WSGIServer((app_host, int(app_port)), app)
        http_server.serve_forever()

