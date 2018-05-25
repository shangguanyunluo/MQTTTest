#!/usr/bin/env python
#
# Copyright (c) 2018 Lenovo, Inc.
# All Rights Reserved.
#
# Authors:
#     Jing Chen <chenjing22@lenovo.com>
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

import test_base
import requests
import json
import os
from datetime import datetime
#from multiprocessing import Pool
import multiprocessing


class ECGUploadTest(test_base.BaseTest):

    def setUp(self):
        test_base.BaseTest.setUp(self)

    #device login to get userID and deviceID according to deviceNum and secretKey
    def login_device(self, index):
        resp = requests.post(self.base_url + self.login_url,
                             json=json.loads(self.device_info[index]),
                             verify=False)
        user_dev_info = json.loads(resp.text)
        user_id = user_dev_info['data']['userId']
        device_id = user_dev_info['data']['deviceId']
        print user_id + " " + device_id
        return user_id, device_id

    #upload ECG data
    def upload_ecg(self, device_index):

        user_id, device_id = self.login_device(device_index)
        client_count = 1
        for n in range(client_count):
            topic = "sys/%s/%s/ecg/upload/%s" % (user_id, device_id, n)
            data_file = os.path.join(self.ecg_file_path, str(n) + '.bin')
            pub_cmd = 'mosquitto_pub -h %s -p %s -i client_%s  -t "%s" -u %s -P %s -d --cafile %s --insecure -r -q 1 -f %s' % (
                self.server_ip, self.server_port, device_index, topic, self.username, self.password,
                self.cert_file, data_file)

            print pub_cmd
            os.system(pub_cmd)

    def multi_process_ecg_upload(self, process):

        s_time = self.str2datetime(datetime.now())
        print "Start testing at %s" % s_time

        processes = []
        for i in range(process):
            p = multiprocessing.Process(target=self.upload_ecg, args=(i, ))
            processes.append(p)

        for process in processes:
            process.start()

        e_time = self.str2datetime(datetime.now())
        print "Finish testing at %s" % e_time


    def test_mutiple_device_concurrency_upload(self):
        concurrency = 4
        #self.upload_ecg(0)
        self.multi_process_ecg_upload(concurrency)