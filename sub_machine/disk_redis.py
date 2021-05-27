import math,time
from redis.client import Redis
from redis.connection import ConnectionPool


REDIS_PORT=31079
REDIS_HOST="81.69.32.223"
pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
r = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

class DiskInfo:
    Capacity: int
    level: int
    def __init__(self,Capacity,level=10):
        self.Capacity=Capacity
        self.level=level
    # def setLevel(self,level):
    #     self.level=level
def setLevel2(diskInfo:DiskInfo,lastDiskInfo:DiskInfo):
    multiplier=math.ceil(diskInfo.capacity/230)

def setLevel(diskInfo:DiskInfo,lastDiskInfo:DiskInfo):
    if lastDiskInfo.level//10==1:
        if diskInfo.Capacity<150:
            diskInfo.level=11
        elif diskInfo.Capacity<200:  #150~200
            diskInfo.level=12
        elif diskInfo.Capacity>200:
            diskInfo.level=20
    elif lastDiskInfo.level//10==2:
        if lastDiskInfo.level<24:
            if diskInfo.Capacity>240:
                diskInfo.level=24
            elif diskInfo.Capacity>lastDiskInfo.Capacity:  # diskInfo.level单调增
                diskInfo.level=diskInfo.Capacity//10
            else:  # <240&&下降
                diskInfo.level=lastDiskInfo.level
        if diskInfo.level>24 and diskInfo.Capacity<lastDiskInfo.Capacity:
            diskInfo.level=30
    elif lastDiskInfo.level//10==3:
        if diskInfo.Capacity<lastDiskInfo.Capacity:
            diskInfo.level=31
        else:
            diskInfo.level=32
            if diskInfo.Capacity>170:
                diskInfo.level=40

class MonitorInfo:
    CapacityD: int
    CapacityE: int
    CapacityF: int
    CapacityG: int
    createTime: str
    id: str
    def __init__(self,id,createTime=None):
        if id == None:
            id = "default"
        self.id=id
        if createTime!=None:
            self.createTime=createTime
        # self.__initMonitorInfo()
    def __lt__(self,other):
        # return self.CapacityG<other.CapacityG 
        if self.CapacityG<other.CapacityG:
            return True
        elif self.CapacityG==other.CapacityG and math.max(
            self.CapacityF,self.CapacityE,self.CapacityD)<max(
            other.CapacityF,other.CapacityE,other.CapacityD):
            return True
        return False
    def __tostring__(self):
        return f'{self.id} {self.CapacityG} {self.CapacityD} {self.CapacityE} {self.CapacityF}'
    def getMonitorInfo(self):
        valG,valF,valE,valD,valTime=r.mget(f"{id}::CapacityG",f"{id}::CapacityF",f"{id}::CapacityE",f"{id}::CapacityD",f"{id}::createTime")
        self.CapacityG=valG if valG!=None else None
        self.CapacityF=valF if valF!=None else None
        self.CapacityE=valE if valE!=None else None
        self.CapacityD=valD if valD!=None else None
        self.createTime=valTime if valTime!=None else None

    def setMonitorInfo(self):
        r.mset(f"{id}::CapacityG",f"{id}::CapacityF",f"{id}::CapacityE",f"{id}::CapacityD",f"{id}::createTime")
        MonitorInfoDict = dict(zip(
            [ f"{id}::CapacityG",f"{id}::CapacityF",f"{id}::CapacityE",f"{id}::CapacityD",f"{id}::createTime"],
            [ self.CapacityG,self.CapacityF,self.CapacityE,self.CapacityD,self.createTime ]
        ))
        r.mset(MonitorInfoDict)
    
    def setLastMonitorInfo(self):
        r.mset(f"{id}::LastCapacityG",f"{id}::LastCapacityF",f"{id}::LastCapacityE",f"{id}::LastCapacityD",f"{id}::LastcreateTime")
        DiskInfoDict = dict(zip(
            [ f"{id}::LastCapacityG",f"{id}::LastCapacityF",f"{id}::LastCapacityE",f"{id}::LastCapacityD",f"{id}::LastcreateTime"],
            [ self.CapacityG,self.CapacityF,self.CapacityE,self.CapacityD,self.createTime ]
        ))
        r.mset(DiskInfoDict)
