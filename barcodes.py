#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyzbar.pyzbar import decode
from PIL import Image
import json
import os

"""
The logger function
"""
def logger(data):
    print(data)
    
"""
This function will get img local path 
and return text barcode from image
"""
def decode_barcode(img_path):
    try:
        return decode(Image.open(img_path))[0].data.decode('utf-8')
    except Exception as e:
        print(e)
        return 'Could not recognition barcode'

"""
This function will get image and return barcode
"""
def barcodes_worker(img, tmp_path, random_value):
    try:
        img.save(os.path.join(tmp_path, random_value))
        return decode_barcode(img)
    except Exception as e:
        print(e)

"""
The defaul check
"""
if __name__ == '__main__':
    pass
