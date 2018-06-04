#!/usr/bin/env python
#
import json
import os
# from multiprocessing import Pool
import subprocess
import unittest
import requests
import fileSizeUtil
import test_base
import time

class UploadTestWithNetFault(test_base.BaseTest):
    def setUp(self):
        test_base.BaseTest.setUp(self)

        self.network = "eth0"
        self.loss_start = 10
        self.loss_end = 20

        self.random_package_loss(self.network, self.loss_start, self.loss_end)

    # device login to get userID and deviceID according to deviceNum and secretKey
    def login_device(self, index):
        resp = requests.post(self.base_url + self.login_url,
                             json=json.loads(self.device_info[index]),
                             verify=False)
        user_dev_info = json.loads(resp.text)
        user_id = user_dev_info['data']['userId']
        device_id = user_dev_info['data']['deviceId']
        print user_id + " " + device_id
        return user_id, device_id

    # upload ECG data
    def upload_ecg(self, device_index):
        user_id, device_id = self.login_device(device_index)
        client_count = 100
        for n in range(client_count):
            topic = "sys/%s/%s/ecg/upload/%s" % (user_id, device_id, n)
            data_file = os.path.join(self.ecg_file_path, str(n) + '.bin')
            pub_cmd = 'mosquitto_pub -h %s -p %s -i client_%s  -t "%s" -u %s -P %s -d --cafile %s --insecure -r -q 1 -f %s' % (
                self.server_ip, self.server_port, device_index, topic,
                self.username, self.password,
                self.cert_file, data_file)

            print pub_cmd
            os.system(pub_cmd)
        time.sleep(15)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=client_count)

    def random_package_loss(self, network, start, end):
        cmd_check = "tc qdisc"
        os.system(cmd_check)

        cmd = "tc qdisc add dev %s root netem loss %s %s" % (
            network, start, end)
        os.system(cmd)

        child = subprocess.Popen(cmd_check, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
        line = child.stdout.readline()
        print line

    def remove_loss_pack(self, network):
        cmd = "tc qdisc del dev %s root" % self.network
        os.system(cmd)

        cmd_check = "tc qdisc"
        child = subprocess.Popen(cmd_check, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
        line = child.stdout.readline()
        print line

    def test_network_loss_pac(self):
        concurrency = 1
        # self.upload_ecg(0)
        # self.multi_process_ecg_upload(concurrency)
        self.upload_ecg(16)

    def tearDown(self):
        self.remove_loss_pack(self.network)


if __name__ == '__main__':
    unittest.main()
