#!/usr/bin/python
# coding:utf-8
#

import test_base
import unittest
import os
import time
import fileSizeUtil


class ECGNetworkFailureUploadTest(test_base.BaseTest):
    def network_fault_commondl(self, network_name="eth0", command_type="add",
                               fault_type="delay", value="50ms 20ms 20%"):
        cmd = "sudo tc qdisc %s dev %s root netem %s %s" % (
            command_type, network_name, fault_type, value)
        print "network command:%s" % cmd
        os.system(cmd)

    # @unittest.skip("test_network_latency_upload")
    def test_network_latency_upload(self):
        try:
            self.network_fault_commondl("eth0", "add")
            time.sleep(1)
            device_index = 1
            user_id, device_id = self.login_device(device_index)

            self.ecg_upload2(user_id, device_id, upload_file_num=100,
                             client_index=device_index)

            time.sleep(15)
            fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                         file_num=100)
        finally:
            self.network_fault_commondl("eth0", "del")

    # @unittest.skip("test_network_pack_repeat_upload")
    def test_network_pack_repeat_upload(self):
        try:
            self.network_fault_commondl("eth0", "add", "duplicate", "1%")
            time.sleep(1)
            device_index = 1
            user_id, device_id = self.login_device(device_index)

            self.ecg_upload2(user_id, device_id, upload_file_num=100,
                             client_index=device_index)
            time.sleep(15)
            fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                         file_num=100)
        finally:
            self.network_fault_commondl("eth0", "del", "duplicate", "1%")


if __name__ == '__main__':
    unittest.main()
