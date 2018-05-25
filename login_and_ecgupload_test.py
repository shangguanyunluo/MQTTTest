#!/usr/bin/python
# coding:utf-8
import time
import os
import test_base
import requests
import json
import unittest


class LoginAndEcgUploadTest(test_base.BaseTest):
    def setUp(self):
        test_base.BaseTest.setUp(self)

    # @unittest.skip('test_login_upload')
    def test_login_upload(self, delay=0):
        self.ecg_login_upload(device_index=3, delay=delay)

    # @unittest.skip('test_login_upload_with_delay')
    def test_login_upload_with_delay(self, delay=200):
        self.ecg_login_upload(device_index=4, delay=delay,
                              topic_suffix="delay")


# if __name__ == '__main__':
#     unittest.main()
