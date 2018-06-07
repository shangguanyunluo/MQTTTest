#!/usr/bin/env python

import multiprocessing
import os
import time
import unittest

import logging

import fileSizeUtil
import test_base


class ECGUploadTest(test_base.BaseTest):
    def setUp(self):
        test_base.BaseTest.setUp(self)

        self.ecg_folder_list = []
        self.changed_size_file_list = {}
        self.expect_file_size = 262152
        self.tmp_path = '/root/s3data/staging.smartvest.lenovo.com/'

    # upload ECG data
    def upload_ecg_data(self, device_index, file_number=1):

        user_id, device_id = self.login_device(device_index)

        self.ecg_upload2(user_id, device_id, upload_file_num=file_number,
                         client_index=device_index)

        time.sleep(20)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=file_number)

    def multi_process_ecg_upload(self, process_num, file_number=10):

        logging.info(
            "Start testing at %s" % self.str2datetime(time.localtime()))

        processes = []
        for device_index in range(process_num):
            p = multiprocessing.Process(target=self.upload_ecg_data,
                                        args=(device_index, file_number))
            p.start()
            processes.append(p)

        for process in processes:
            process.join()
        logging.info("processes number is : %s" % len(processes))
        process_exitcode_list = [p.exitcode for p in processes]
        process_error_number = len([num for num in process_exitcode_list if
                                    num == 1])
        logging.info("process_exitcode_list ---- %s" % process_exitcode_list)
        logging.info("process_error_number ==== %s" % process_error_number)
        logging.info(
            "Finish testing at %s" % self.str2datetime(time.localtime()))

    @unittest.skip("test_mutiple_device_concurrency_upload_10")
    def test_mutiple_device_concurrency_upload_10(self):
        concurrency = 10
        self.multi_process_ecg_upload(concurrency, 2000)

    @unittest.skip("test_mutiple_device_concurrency_upload_50")
    def test_mutiple_device_concurrency_upload_50(self):
        concurrency = 50
        self.multi_process_ecg_upload(concurrency, 2000)

    @unittest.skip("test_mutiple_device_concurrency_upload_70")
    def test_mutiple_device_concurrency_upload_70(self):
        concurrency = 70
        self.multi_process_ecg_upload(concurrency, 1000)

    @unittest.skip("test_mutiple_device_concurrency_upload_100")
    def test_mutiple_device_concurrency_upload_100(self):
        concurrency = 100
        self.multi_process_ecg_upload(concurrency, file_number=0)


if __name__ == '__main__':
    unittest.main()
