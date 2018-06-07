#!/usr/bin/python
# coding:utf-8

import unittest

import time
import logging
import test_base
import fileSizeUtil


class ECGUploadSpecifizedFileTest(test_base.BaseTest):
    # @unittest.skip("testUploadFile1B")
    def testUploadFile1B(self):
        logging.info("%s ---- : %s" % ("testUploadFile1B", "start"))
        user_id, device_id = self.ecg_login_upload(device_index=6,
                                                   filname_prefix="1B",
                                                   topic_suffix="1B")
        time.sleep(2)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=1, file_size=1)
        logging.info("%s ---- : %s" % ("testUploadFile1B", "end"))

    # @unittest.skip("testUploadFile256KB")
    def testUploadFile256KB(self):
        logging.info("%s ---- : %s" % ("testUploadFile256KB", "start"))
        user_id, device_id = self.ecg_login_upload(device_index=7,
                                                   filname_prefix="256KB",
                                                   topic_suffix="256KB")
        time.sleep(5)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=1, file_size=256 * 1024)
        logging.info("%s ---- : %s" % ("testUploadFile256KB", "end"))

    # @unittest.skip("testUploadFile300KB")
    def testUploadFile300KB(self):
        logging.info("%s ---- : %s" % ("testUploadFile300KB", "start"))
        user_id, device_id = self.ecg_login_upload(device_index=8,
                                                   filname_prefix="300KB",
                                                   topic_suffix="300KB")
        time.sleep(2)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=1, file_size=300 * 1024)
        logging.info("%s ---- : %s" % ("testUploadFile300KB", "end"))


if __name__ == '__main__':
    unittest.main()
