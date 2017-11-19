import os
import sys
from time import sleep
sys.path.append(os.path.join(os.getcwd().split('scholar')[0],'scholar'))

from multiprocessing.dummy import Pool

import requests
from ScreenShot.url_cache import redis_obj

def run(url, id):
    try:
        _url = str(url.decode('utf-8'))
        _id = int(id.decode('utf-8'))
        res = requests.post("http://localhost:5050", data={"url":_url,"output":"{}.jpg".format(_id)})
        redis_obj.delete(id)
        print(_url)
    except Exception as e:
        print(e)
        
        
pool = Pool(processes=10)

for i in redis_obj.scan_iter():
    id = i
    url = redis_obj.get(i)
# while redis_obj.llen("scholar"):
#     tmp = redis_obj.lpop("scholar").decode('utf-8').split("  ")
#     id, url = tmp[0], tmp[1]
    pool.apply_async(run, args=(url, id))
    
pool.close()
pool.join()
