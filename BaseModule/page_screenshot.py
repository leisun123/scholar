from multiprocessing.dummy import Pool

import requests
from BaseModule.url_cache import redis_obj
def run(url, id):
    try:
        res = requests.post("http://localhost:5050", data={"url":url,"output":"{}.jpg".format(id)})
        print(url)
    except Exception as e:
        print(e)
        
        
pool = Pool(processes=10)

for i in redis_obj.scan_iter():
    id = int(i.decode('utf-8'))
    url = str(redis_obj.get(i).decode('utf-8'))
    pool.apply_async(run, args=(url, id))
pool.close()
pool.join()
