#!/usr/bin/python
# coding:utf-8

import logging
import unittest
import time
import math
import test_base
import fileSizeUtil


class ECGUploadContinuouslyTest(test_base.BaseTest):
    def str2datetime(self, now):
        return time.strftime("%Y-%m-%d %H:%M:%S", now)

    # @unittest.skip("test_continue_upload_in300s")
    def test_continue_upload_in300s(self):
        logging.info(
            "%s ---- : %s : %s" % ("test_continue_upload_in300s", "start",
                                   self.str2datetime(time.localtime())))

        user_id, device_id = self.login_device(index=2)
        file_num = self.upload_file_intervial(user_id, device_id,
                                              time_period=300,
                                              time_interval=2)
        time.sleep(10)

        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=file_num)
        logging.info(
            "%s ---- : %s : %s" % ("test_continue_upload_in300s", "end",
                                   self.str2datetime(time.localtime())))

    # @unittest.skip("test_noncontinue_upload_in300s")
    def test_noncontinue_upload_in300s(self):
        logging.info(
            "%s ---- : %s" % ("test_noncontinue_upload_in300s", "start"))

        user_id, device_id = self.login_device(index=3)
        file_num = self.upload_file_intervial(user_id, device_id)
        time.sleep(10)

        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=file_num)
        logging.info(
            "%s ---- : %s" % ("test_noncontinue_upload_in300s", "end"))

    # @unittest.skip("test_continue_upload_greater_than_300s")
    def test_continue_upload_greater_than_300s(self):
        logging.info("%s ---- : %s" % (
            "test_continue_upload file greater_than_300s", "start"))

        user_id, device_id = self.login_device(index=4)
        file_num = self.upload_file_intervial(user_id, device_id,
                                              time_period=320,
                                              time_interval=3)
        time.sleep(10)

        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=file_num)
        logging.info("%s ---- : %s" % (
            "test_continue_upload file greater_than_300s", "end"))

    # @unittest.skip("test_continue_upload_file_1_5GB")
    def test_continue_upload_file_1_5GB(self):
        logging.info(
            "%s ---- : %s : %s" % ("test_continue_upload_file_1.5GB", "start",
                                   self.str2datetime(time.localtime())))
        # "1.5GB is : %s" % (1.5 * 1024 * 1024 * 1024,)
        data_size = 1610612736.0
        # "each bin file size is %s" % 262152
        bin_size = 262152
        bin_file_number = int(math.ceil(data_size / bin_size))

        user_id, device_id = self.login_device(5)
        for i in range(bin_file_number):
            self.ecg_upload(user_id, device_id, topic_suffix=i)
        logging.info(
            "%s ---- : %s : %s" % ("test_continue_upload_file_1.5GB", "end",
                                   self.str2datetime(time.localtime())))
        time.sleep(20)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=bin_file_number)


if __name__ == '__main__':
    unittest.main()
