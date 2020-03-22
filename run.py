"""
Routes and views for the flask application.
"""
import os
import random
from datetime import datetime
from flask import render_template, request, json, redirect, url_for, Flask
from os import environ
from pymongo import MongoClient
from pyzbar.pyzbar import decode
from PIL import Image

app = Flask(__name__)

random_value      = ''.join(str(random.randint(0,9)) for _ in range(12))
app_host          = environ.get('APP_HOST', '0.0.0.0')
app_port          = environ.get('APP_PORT', '5000')
app_mongo_ip      = environ.get('MONGO_IP', '134.209.241.140')
app_mongo_port    = int(environ.get('MONGO_PORT', '27017'))
app_mongo_db      = environ.get('MONGO_DB', 'profiles')
app_mongo_coll    = environ.get('MONGO_COLLECTION', 'inventory_data')
tmp_path          = environ.get('TMP_PATH_DIR', '/tmp')
mongo_client      = MongoClient(app_mongo_ip, app_mongo_port)
collection        = mongo_client[app_mongo_db][app_mongo_coll]

def logger(data):
    print(data)

def decode_barcode(img_path):
    try:
        return decode(Image.open(img_path))[0].data.decode('utf-8')
    except Exception as e:
        logger(e)
        return 'Could not recognition barcode'

def barcodes_worker(img, random_v):
    img.save(os.path.join(tmp_path, random_value))
    return json.dumps({'data_sn': decode_barcode(img)})
    
def get_mongo_data(collection_obj):
    try:
        return [x for x in collection_obj.find({}, {'_id': False})]
    except Exception as e:
        logger(e)

def add_mongo_data(m_collection, mongo_data):
    try:
        m_collection.insert_one(mongo_data)
    except Exception as e:
        logger(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remote_users')
def remote_users():
    return render_template('remote_users.html', inventory_data=get_mongo_data(collection))

@app.route('/inventory')
def inventory():
    return render_template('inventory.html', inventory_data=get_mongo_data(collection))

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
                        
        add_mongo_data(collection, dict_data)
        
        return(redirect(url_for('index')))

@app.route('/add_info')
def add_info():
    username   = request.args.get('user_name')
    mongo_data =  get_mongo_data(collection)

    for user in mongo_data:
        if username in user['UserName']:   
            return render_template('add_info.html', inventory_data=user)

@app.route('/hdd_sn', methods=['POST', 'GET'])
def hdd_sn():
    return barcodes_worker(request.files['hdd_sn'], random_value)

@app.route('/monitor_sn', methods=['POST', 'GET'])
def monitor_sn():
    return barcodes_worker(request.files['monitor_sn'], random_value)

app.run(host=app_host, port=app_port)

