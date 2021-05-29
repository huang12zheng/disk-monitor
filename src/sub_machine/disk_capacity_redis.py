#!/usr/bin/python3
# schtasks /create /sc minute /mo 20 /tn "Available Check" /tr "disk_capacity.exe"
import os
import platform
import ctypes
import json
# import queue,time
from disk_redis import MonitorInfo
import sys

import socket

args=sys.argv
if len(args) > 1:
    HostName = sys.argv[1] 


def get_free_space_mb(folder):
    
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 // 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024 // 1024


try:
    if platform.system() == 'Windows':

        HostName="Default"
        monitor=MonitorInfo(HostName)
        monitor.getMonitorInfo().setLastMonitorInfo()
        
        monitor.CapacityG=get_free_space_mb("G:\\")
        monitor.CapacityF=get_free_space_mb("F:\\")
        monitor.CapacityE=get_free_space_mb("E:\\")
        monitor.CapacityD=get_free_space_mb("D:\\")
        monitor.createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        monitor.setMonitorInfo()
    else:
        dir='/dev/disk1s5'
        print("do none")

    # post_data(arg1,{"available": val,"time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) })

except:
    print('get_free_space_mb ERROR')