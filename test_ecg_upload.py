#!/usr/bin/env python
#
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
    def upload_ecg(self, device_index, client_count=1):

        user_id, device_id = self.login_device(device_index)
        if not client_count:
            client_count = 1
        for n in range(client_count):
            file_name = n
            if n > 99:
                file_name = n % 99
            topic = "sys/%s/%s/ecg/upload/%s" % (user_id, device_id, n)
            data_file = os.path.join(self.ecg_file_path,
                                     str(file_name) + '.bin')
            pub_cmd = 'mosquitto_pub -h %s -p %s -i client_%s  -t "%s" -u %s -P %s -d --cafile %s --insecure -r -q 1 -f %s' % (
                self.server_ip, self.server_port, device_index, topic,
                self.username, self.password,
                self.cert_file, data_file)

            logging.info(pub_cmd)
            try:
                response = os.system(pub_cmd)
                if response != 0:
                    response = os.system(pub_cmd)

            except Exception as e:
                response = os.system(pub_cmd)
            finally:
                logging.info("%s file num %d response is : %s" % (user_id, n,
                                                                  response))

        time.sleep(15)
        fileSizeUtil.data_validation(user_id=user_id, device_id=device_id,
                                     file_num=client_count,
                                     file_size=self.expect_file_size)

    def multi_process_ecg_upload(self, process, client_count=10):

        logging.info(
            "Start testing at %s" % self.str2datetime(time.localtime()))

        processes = []
        lock = multiprocessing.Lock()
        for i in range(process):
            p = multiprocessing.Process(target=self.upload_ecg,
                                        args=(i, client_count))
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
        self.multi_process_ecg_upload(concurrency,2000)

    @unittest.skip("test_mutiple_device_concurrency_upload_50")
    def test_mutiple_device_concurrency_upload_50(self):
        print '----'
        concurrency = 50
        self.multi_process_ecg_upload(concurrency, 1000)
        # concurrency = 1
        # self.multi_process_ecg_upload(concurrency, 2)

    @unittest.skip("test_mutiple_device_concurrency_upload_70")
    def test_mutiple_device_concurrency_upload_70(self):
        concurrency = 70
        self.multi_process_ecg_upload(concurrency, 1000)

    @unittest.skip("test_mutiple_device_concurrency_upload_100")
    def test_mutiple_device_concurrency_upload_100(self):
        concurrency = 100
        self.multi_process_ecg_upload(concurrency, 1000)


if __name__ == '__main__':
    unittest.main()
