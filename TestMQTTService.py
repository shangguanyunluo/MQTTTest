#!/usr/bin/env python
#
# Copyright (c) 2018 Lenovo, Inc.
# All Rights Reserved.
#
# Authors:
#     Ying Liu <liuying23@lenovo.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import json
import requests
import os
import time
from datetime import datetime
from multiprocessing import Pool

concurrency = 50
base_url = "https://43.255.224.58/api/test"
server_ip = "43.255.224.120"
server_port = "1883"
username = "admin1"
password = "passw0rd@"
cert_file = "./ca.crt"
login_url = "/device-service/device/login"
ecg_file_path = "./sim_data_test_3_hours/"

with open('device_info.txt', 'r') as f:
    device_info = f.read().split('\n')
    f.close()

# datefmt = "%a, %d %b %Y %H:%M:%S"
datefmt = "%Y-%m-%d %H:%M:%S.%f"


def str2datetime(s, format=datefmt):
    dt = None
    try:
        dt = s.strftime(format)
    except (ValueError):
        dt = None
    finally:
        return dt


# 1) device login to get deviceNum and secretKey
# 2) upload ECG data
def device_login_and_upload_ecg(d_n):
    resp = requests.post(base_url + login_url,
                         json=json.loads(device_info[d_n]),
                         verify=False)
    user_dev_info = json.loads(resp.text)
    user_id = user_dev_info['data']['userId']
    device_id = user_dev_info['data']['deviceId']
    print user_id + " " + device_id

    for n in range(100):
        topic = "sys/%s/%s/ecg/upload/%s" % (user_id, device_id, n)
        data_file = os.path.join(ecg_file_path, str(n) + '.bin')
        pub_cmd = 'mosquitto_pub -h %s -p %s -i client_%s  -t "%s" -u %s -P %s -d --cafile %s --insecure -r -q 1 -f %s' % (
            server_ip, server_port, d_n, topic, username, password, cert_file, data_file)
        print pub_cmd
        os.system(pub_cmd)


if __name__ == '__main__':
    # device_login_and_upload_ecg(0)
    pool = Pool(processes=4)

    s_time = str2datetime(datetime.now())
    print "Start testing at %s" % s_time

    results = []
    msgs = [x for x in range(10)]
    results = pool.map(device_login_and_upload_ecg, msgs)

    pool.close()
    pool.join()

    e_time = str2datetime(datetime.now())
    print "Finish testing at %s" % e_time

    print 'Uploading ECG data concurrently'
    for r in results:
        print r

