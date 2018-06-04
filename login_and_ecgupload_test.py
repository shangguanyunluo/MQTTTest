#!/usr/bin/python
# coding:utf-8



import time
import os
import test_base
import requests
import json
import unittest
import fileSizeUtil


class LoginAndEcgUploadTest(test_base.BaseTest):
    def setUp(self):
        test_base.BaseTest.setUp(self)

    # @unittest.skip('test_login_upload')
    def test_login_upload(self, delay=0):
        # self.ecg_login_upload(device_index=3, delay=delay)
        user_id, device_id = self.ecg_login_upload_files(device_index=13,
                                                         delay=delay)

        time.sleep(15)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=100)

    # @unittest.skip('test_login_upload_with_delay')
    def test_login_upload_with_delay(self, delay=200):
        # self.ecg_login_upload(device_index=4, delay=delay,
        #                       topic_suffix="delay")
        user_id, device_id = self.ecg_login_upload_files(device_index=14,
                                                         delay=delay)
        time.sleep(15)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=100)


if __name__ == '__main__':
    unittest.main()
