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

    # upload ECG data
    def upload_ecg_data(self, device_index, file_number=100):
        user_id, device_id = self.login_device(device_index)

        self.ecg_upload2(user_id, device_id, upload_file_num=file_number,
                         client_index=device_index, test_mode=False)

        time.sleep(15)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=file_number)

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

    def remove_loss_pack(self):
        cmd = "tc qdisc del dev %s root" % self.network
        os.system(cmd)

        cmd_check = "tc qdisc"
        child = subprocess.Popen(cmd_check, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
        line = child.stdout.readline()
        print line

    # @unittest.skip("test_network_loss_pac")
    def test_network_loss_pac(self):
        self.upload_ecg_data(device_index=9, file_number=10)

    def tearDown(self):
        self.remove_loss_pack()


if __name__ == '__main__':
    unittest.main()
