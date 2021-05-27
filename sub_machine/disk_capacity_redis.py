#!/usr/bin/python3
# schtasks /create /sc minute /mo 20 /tn "Available Check" /tr "disk_capacity.exe"
import os
import platform
import ctypes
import json
import queue,requests,time
import sys

arg1 = sys.argv[1]


def get_free_space_mb(folder):
    
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 // 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024 // 1024

def post_data(url,args):
    headers = {'Content-Type': 'application/json'}
    # datas = json.dumps({"param1": "Detector", "param2": "cnblogs"})
    datas = json.dumps(args)
    # r = requests.post("http://httpbin.org/post", data=datas, headers=headers)
    r = requests.post(url, data=datas, headers=headers)
    print(r.text)

# def setDiskValue():


try:
    # get_free_space_mb('G:\')
    if platform.system() == 'Windows':
        dir='G:\\'
    else:
        dir='/dev/disk1s5'
    val=get_free_space_mb(dir)
    print(arg1)
    print(val)

    # post_data(arg1,{"available": val,"time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) })

except:
    print('get_free_space_mb ERROR')