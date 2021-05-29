#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import math,time
from redis.client import Redis
from redis.connection import ConnectionPool


REDIS_PORT=31079
REDIS_HOST="81.69.32.223"
pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
r = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

class DiskInfo:
    level: int
    capacity: int


    def __init__(self,capacity,level=10):
        self.capacity=capacity
        self.level=level
    # def setLevel(self,level):
    #     self.level=level
def setLevel2(diskInfo:DiskInfo,lastDiskInfo:DiskInfo):
    multiplier=math.ceil(diskInfo.capacity/230)

def setLevel(diskInfo:DiskInfo,lastDiskInfo:DiskInfo):
    if lastDiskInfo.level//10==1:
        if diskInfo.capacity<150:
            diskInfo.level=11
        elif diskInfo.capacity<200:  #150~200
            diskInfo.level=12
        elif diskInfo.capacity>200:
            diskInfo.level=20
    elif lastDiskInfo.level//10==2:
        if lastDiskInfo.level<24:
            if diskInfo.capacity>240:
                diskInfo.level=24
            elif diskInfo.capacity>lastDiskInfo.capacity:  # diskInfo.level单调增
                diskInfo.level=diskInfo.capacity//10
            else:  # <240&&下降
                diskInfo.level=lastDiskInfo.level
        if diskInfo.level>24 and diskInfo.capacity<lastDiskInfo.capacity:
            diskInfo.level=30
    elif lastDiskInfo.level//10==3:
        if diskInfo.capacity<lastDiskInfo.capacity:
            diskInfo.level=31
        else:
            diskInfo.level=32
            if diskInfo.capacity>170:
                diskInfo.level=40

class MonitorInfo:
    capacityD: int
    capacityE: int
    capacityF: int
    capacityG: int
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
        # return self.capacityG<other.capacityG 
        if self.capacityG<other.capacityG:
            return True
        elif self.capacityG==other.capacityG and math.max(
            self.capacityF,self.capacityE,self.capacityD)<max(
            other.capacityF,other.capacityE,other.capacityD):
            return True
        return False
    def __tostring__(self):
        return f'{self.id} {self.capacityG} {self.capacityD} {self.capacityE} {self.capacityF}'
    def getMonitorInfo(self):
        valG,valF,valE,valD,valTime=r.mget(f"{id}::capacityG",f"{id}::capacityF",f"{id}::capacityE",f"{id}::capacityD",f"{id}::createTime")
        self.capacityG=valG if valG!=None else None
        self.capacityF=valF if valF!=None else None
        self.capacityE=valE if valE!=None else None
        self.capacityD=valD if valD!=None else None
        self.createTime=valTime if valTime!=None else None

    def setMonitorInfo(self):
        r.mset(f"{id}::capacityG",f"{id}::capacityF",f"{id}::capacityE",f"{id}::capacityD",f"{id}::createTime")
        MonitorInfoDict = dict(zip(
            [ f"{id}::capacityG",f"{id}::capacityF",f"{id}::capacityE",f"{id}::capacityD",f"{id}::createTime"],
            [ self.capacityG,self.capacityF,self.capacityE,self.capacityD,self.createTime ]
        ))
        r.mset(MonitorInfoDict)
    
    def setLastMonitorInfo(self):
        if self.capacityG!=None:
            r.mset(f"{id}::LastcapacityG",f"{id}::LastcapacityF",f"{id}::LastcapacityE",f"{id}::LastcapacityD",f"{id}::LastcreateTime")
            DiskInfoDict = dict(zip(
                [ f"{id}::LastcapacityG",f"{id}::LastcapacityF",f"{id}::LastcapacityE",f"{id}::LastcapacityD",f"{id}::LastcreateTime"],
                [ self.capacityG,self.capacityF,self.capacityE,self.capacityD,self.createTime ]
            ))
            r.mset(DiskInfoDict)

