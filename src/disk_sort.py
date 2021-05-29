from sub_machine.disk_redis import MonitorInfo
from redis.client import Redis
from redis.connection import ConnectionPool
from os import path
import time

REDIS_PORT=31079
REDIS_HOST="81.69.32.223"
pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
r = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def getRank(ids):
    monitors=[]
    for id in ids:
        enum=MonitorInfo(id)
        enum.getMonitorInfo()
        monitors.append(enum)
    
    savefile(__file__,f'rank_{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.txt',monitors.sort())

def savefile(run_parent,filename, data):
    config_path = path.join(path.dirname(run_parent),filename)
    # jsonStr = json.dumps(data, indent=4,ensure_ascii=False)
    with open(config_path,"r+",encoding="utf8")as fp:
        fp.truncate(0)
        fp.seek(0)
        # fp.write(jsonStr)
        for enum in data:
            fp.write(enum.__tostring__())

# getRank()