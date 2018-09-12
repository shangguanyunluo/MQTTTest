#!/usr/bin/env python

import logging
import multiprocessing
import time
import unittest

import fileSizeUtil
import test_base


class ECGUploadTest(test_base.BaseTest):

    def setUp(self):
        test_base.BaseTest.setUp(self)

        self.ecg_folder_list = []
        self.changed_size_file_list = {}
        self.expect_file_size = 262152
        # the file path you upload the file to
        self.tmp_path = '/root/s3data/staging.smartvest.lenovo.com/'

    # upload ECG data
    def upload_ecg_data(self, device_index, file_number=1):

        user_id, device_id = self.login_device(device_index)

        self.ecg_upload2(user_id, device_id, upload_file_num=file_number,
                         client_index=device_index)

        # time.sleep(30)
        # fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
        #                              file_num=file_number)

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
        login_process_exitcode_list = [p.exitcode for p in processes]
        login_process_error_number = len([num for num in
                                          login_process_exitcode_list if
                                          num == 1])
        logging.info(
            "login_process_exitcode_list ---- %s" % login_process_exitcode_list)
        logging.info(
            "login_process_error_number ==== %s" % login_process_error_number)

        # to check the files you upload,if there is some files fail to upload
        time.sleep(process_num / 2)
        upload_process_error_number, upload_fail_list = fileSizeUtil.validate_upload_files(
            process_num=process_num, file_num=file_number,
            file_size=self.expect_file_size)
        logging.info("upload_process_error_number :%s, upload_fail_list : %s" % \
                      (upload_process_error_number, upload_fail_list))
        logging.info(
            "Finish testing at %s" % self.str2datetime(time.localtime()))
        if upload_process_error_number > 0 or login_process_error_number > 0:
            msg = "%s process upload $s files test error,login error: %s, " \
                  "upload files error: %s" % (process_num, file_number,
                                              login_process_error_number,
                                              upload_process_error_number)
            logging.error(msg)
            raise Exception(msg)

    @unittest.skip("test_mutiple_device_concurrency_upload_10")
    def test_mutiple_device_concurrency_upload_10(self):
        concurrency = 10
        self.multi_process_ecg_upload(concurrency, 2000)

    @unittest.skip("test_mutiple_device_concurrency_upload_50")
    def test_mutiple_device_concurrency_upload_50(self):
        concurrency = 50
        file_number = 1000
        self.multi_process_ecg_upload(concurrency, file_number)

    @unittest.skip("test_mutiple_device_concurrency_upload_70")
    def test_mutiple_device_concurrency_upload_70(self):
        concurrency = 70
        self.multi_process_ecg_upload(concurrency, 1000)

    @unittest.skip("test_mutiple_device_concurrency_upload_100")
    def test_mutiple_device_concurrency_upload_100(self):
        concurrency = 100
        self.multi_process_ecg_upload(concurrency, file_number=1000)


if __name__ == '__main__':
    unittest.main()
