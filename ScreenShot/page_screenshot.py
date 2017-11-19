import os
import sys
from time import sleep
sys.path.append(os.path.join(os.getcwd().split('scholar')[0],'scholar'))

from multiprocessing.dummy import Pool

import requests
from ScreenShot.url_cache import redis_obj

def run(url, id):
    try:
        res = requests.post("http://localhost:5050", data={"url":url,"output":"{}.jpg".format(id)})
        sleep(1)
        print(url)
    except Exception as e:
        print(e)
        
        
pool = Pool(processes=10)

while True:
    tmp = redis_obj.lpop("scholar").decode('utf-8').split("  ")
    id, url = tmp[0], tmp[1]
    print(id, url)
    run(url=url, id=id)
    
pool.close()
pool.join()
