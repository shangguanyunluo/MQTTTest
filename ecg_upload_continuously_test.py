#!/usr/bin/python
# coding:utf-8
import json
import unittest
import time
import math

import test_base


class ECGUploadContinuouslyTest(test_base.BaseTest):
    def upload_file_intervial(self, user_id, device_id, topic_suffix="",
                              time_period=300, time_interval=45,
                              filname_prefix=0):
        """
        topic_suffix : use this to distinguish which method call this method
        time_period : the whole time to upload files
        time_interval : the time between you upload two files
        file_num :the number of file you will uploads in the time_period
        :return: 
        """
        file_num = time_period / time_interval + 1
        start_time = time.time()
        continue_flag = True
        while continue_flag:
            now_time = time.time()
            # print "(now_time - start_time) is : %s" % (now_time - start_time)
            if int(now_time - start_time) >= time_period:
                continue_flag = False
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), \
                "topic_suffix is : %s%s" % (topic_suffix, file_num)

            self.ecg_upload(user_id, device_id, filname_prefix=filname_prefix,
                            topic_suffix="%s%s" % (topic_suffix, file_num))
            file_num -= 1
            if continue_flag:
                time.sleep(time_interval)

    # @unittest.skip("test_continue_upload_in300s")
    def test_continue_upload_in300s(self):
        print("%s ---- : %s" % ("test_continue_upload_in300s", "start"))

        user_id, device_id = self.login_device(index=33)
        self.upload_file_intervial(user_id, device_id, time_period=300,
                                   time_interval=3, topic_suffix="_")

        print("%s ---- : %s" % ("test_continue_upload_in300s", "end"))

    # @unittest.skip("test_noncontinue_upload_in300s")
    def test_noncontinue_upload_in300s(self):
        print("%s ---- : %s" % ("test_noncontinue_upload_in300s", "start"))

        user_id, device_id = self.login_device(index=34)
        self.upload_file_intervial(user_id, device_id, topic_suffix="__")

        print("%s ---- : %s" % ("test_noncontinue_upload_in300s", "end"))

    # @unittest.skip("test_continue_upload_greater_than_300s")
    def test_continue_upload_greater_than_300s(self):
        print("%s ---- : %s" % (
            "test_continue_upload file greater_than_300s", "start"))

        user_id, device_id = self.login_device(index=36)
        self.upload_file_intervial(user_id, device_id, time_period=320,
                                   time_interval=3, topic_suffix="___")

        print("%s ---- : %s" % (
            "test_continue_upload file greater_than_300s", "end"))

    # @unittest.skip("test_continue_upload_file_1_5GB")
    def test_continue_upload_file_1_5GB(self):
        print(
            "%s ---- : %s" % ("test_continue_upload_file_1.5GB", "start"))
        # "1.5GB is : %s" % (1.5 * 1024 * 1024 * 1024,)
        data_size = 1610612736.0
        # "each bin file size is %s" % 262152
        bin_size = 262152
        bin_file_number = int(math.ceil(data_size / bin_size))
        # print bin_file_number
        user_id, device_id = self.login_device()
        for i in range(bin_file_number):
            self.ecg_upload(user_id, device_id, topic_suffix=i)
        print("%s ---- : %s" % ("test_continue_upload_file_1.5GB", "end"))


# if __name__ == '__main__':
#     unittest.main()
