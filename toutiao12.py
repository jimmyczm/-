#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io  
import sys
import requests
from urllib.parse import urlencode
import os
from hashlib  import md5
from multiprocessing.pool import Pool
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 

def  get_page(offset):
    params = {
         'offset': offset,
        'format': 'json',
        'keyword': 'dota',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab',
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_images(neirong):
    if neirong.get('data'):
        for item in neirong.get('data'):
            title = item.get('title')
            image= item.get('image_url')
            if title and image != None and image :
                yield {
                    'image' : 'http:'+image,
                    'title' : title
                }
            
def save_image (item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            rstr = r"[\/\\\:\*\?\"\<\>\|]"
            filename = re.sub(rstr, "_", item.get('title'))
            file_path = '{0}/{1}.{2}'.format(filename,md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f :
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')
            
def main (offset):
    neirong = get_page(offset)
    for item in get_images(neirong):
        print(item)
        save_image(item)

GROUP_START = 1
GROUP_END = 20

if __name__ == '__main__' :
    pool = Pool()
    groups = ([x * 20 for x in range (GROUP_START, GROUP_END + 1)]) 
    pool.map(main,groups)
    pool.close()
    pool.join()


        
            
    
          
        
        




