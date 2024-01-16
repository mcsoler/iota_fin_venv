#!/usr/bin/python
from ggoCableBase import Config
from ggoCableBase import Store
from ggoCableBase.Events2 import Events2
from ggoCableBase.Api import Api
import time
import os
import sys
import json
import re
import subprocess

#Declare var
cnf = Config()
api = Api()

#Cycle start
while True:

    #Start of reference point
    start = time.time()
    #Query of workstations
    sql =  "select CAST(CASE WHEN END_DATE is NULL THEN 999990 ELSE UNIX_TIMESTAMP(NOW())-UNIX_TIMESTAMP(END_DATE) END AS char(5)) as CNT from CM_CURRENT_TEST where WORKSTATION=1 order by ID desc limit 1"
    sql1 =  "select CAST(CASE WHEN END_DATE is NULL THEN 999990 ELSE UNIX_TIMESTAMP(NOW())-UNIX_TIMESTAMP(END_DATE) END AS char(5)) as CNT from CM_CURRENT_TEST where WORKSTATION=2 order by ID desc limit 1"
    sql2 =  "select CAST(CASE WHEN END_DATE is NULL THEN 999990 ELSE UNIX_TIMESTAMP(NOW())-UNIX_TIMESTAMP(END_DATE) END AS char(5)) as CNT from CM_CURRENT_TEST where WORKSTATION=3 order by ID desc limit 1"
    
    #Execute query
    res = api.execute_sql(sql)
    print(res)
    res1 = api.execute_sql(sql1)
    print(res1)
    res2 = api.execute_sql(sql2)
    
    #Cycle to execute cm_info in workstation
    try:
        if 'results' in res and len(res['results']) > 0:
            if float(res['results'][0]['CNT']) == 99999:
                act = './fire_event2.py'
                arg = 'cm_info'
                for _ in range(2):
                    subprocess.run(['python3', act, arg])
        if 'results' in res1 and len(res1['results']) > 0:
            if float(res1['results'][0]['CNT']) == 99999:
                act = './fire_event2.py'
                arg = 'cm_info'
                for _ in range(2):
                    subprocess.run(['python3', act, arg])
        if 'results' in res2 and len(res2['results']) > 0:
            if float(res2['results'][0]['CNT']) == 99999:
                act = './fire_event2.py'
                arg = 'cm_info'
                for _ in range(2):
                    subprocess.run(['python3', act, arg])
    except Exception as e:
        print("Error ",str(e))
        
        #Break arguments
        if len(sys.argv) >= 2:
            break
    time.sleep(10)