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
    def test_login_upload(self, device_index=0, file_number=100, delay=0):
        file_number = 1
        user_id, device_id = self.login_device(device_index)

        self.ecg_upload2(user_id, device_id, upload_file_num=file_number,
                         client_index=device_index, delay=delay)

        time.sleep(15)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=file_number)

    # @unittest.skip('test_login_upload_with_delay')
    def test_login_upload_with_delay(self, device_index=1, file_number=100,
                                     delay=200):
        user_id, device_id = self.login_device(device_index)

        self.ecg_upload2(user_id, device_id, upload_file_num=file_number,
                         client_index=device_index, delay=delay)

        time.sleep(15)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=file_number)


if __name__ == '__main__':
    unittest.main()
