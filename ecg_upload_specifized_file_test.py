#!/usr/bin/python
# coding:utf-8
import unittest
import test_base
import os


class ECGUploadSpecifizedFileTest(test_base.BaseTest):
    # @unittest.skip("testUploadFile1B")
    def testUploadFile1B(self):
        print("%s ---- : %s" % ("testUploadFile1B", "start"))
        # data_file = os.path.join(self.ecg_file_path, '%s.bin' % "1B")
        self.ecg_login_upload(filname_prefix="1B", topic_suffix="1B")
        print("%s ---- : %s" % ("testUploadFile1B", "end"))

    # @unittest.skip("testUploadFile256KB")
    def testUploadFile256KB(self):
        print("%s ---- : %s" % ("testUploadFile256KB", "start"))
        # data_file = os.path.join(self.ecg_file_path, '%s.bin' % "256KB")
        self.ecg_login_upload(filname_prefix="256KB", topic_suffix="256KB")
        print("%s ---- : %s" % ("testUploadFile256KB", "end"))

    # @unittest.skip("testUploadFile300KB")
    def testUploadFile300KB(self):
        print("%s ---- : %s" % ("testUploadFile300KB", "start"))
        # data_file = os.path.join(self.ecg_file_path, '%s.bin' % "300KB")
        self.ecg_login_upload(filname_prefix="300KB", topic_suffix="300KB")
        print("%s ---- : %s" % ("testUploadFile300KB", "end"))


# if __name__ == '__main__':
#     unittest.main()
