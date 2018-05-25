
import test_base
import requests
import json
import os
from datetime import datetime
#from multiprocessing import Pool
import multiprocessing


class ECGUploadTest(test_base.BaseTest):

    def setUp(self):
        test_base.BaseTest.setUp(self)

        self.ecg_folder_list = []
        self.changed_size_file_list = {}
        self.expect_file_size = 262152
        self.tmp_path = '/mqtt/staging.smartvest.lenovo.com/'

    #device login to get userID and deviceID according to deviceNum and secretKey
    def login_device(self, index):
        resp = requests.post(self.base_url + self.login_url,
                             json=json.loads(self.device_info[index]),
                             verify=False)
        user_dev_info = json.loads(resp.text)
        user_id = user_dev_info['data']['userId']
        device_id = user_dev_info['data']['deviceId']
        print user_id + " " + device_id
        return user_id, device_id

    #upload ECG data
    def upload_ecg(self, device_index):

        user_id, device_id = self.login_device(device_index)
        client_count = 1
        for n in range(client_count):
            topic = "sys/%s/%s/ecg/upload/%s" % (user_id, device_id, n)
            data_file = os.path.join(self.ecg_file_path, str(n) + '.bin')
            pub_cmd = 'mosquitto_pub -h %s -p %s -i client_%s  -t "%s" -u %s -P %s -d --cafile %s --insecure -r -q 1 -f %s' % (
                self.server_ip, self.server_port, device_index, topic, self.username, self.password,
                self.cert_file, data_file)

            print pub_cmd
            os.system(pub_cmd)

    def multi_process_ecg_upload(self, process):

        s_time = self.str2datetime(datetime.now())
        print "Start testing at %s" % s_time

        processes = []
        lock = multiprocessing.Lock()
        for i in range(process):
            p = multiprocessing.Process(target=self.upload_ecg, args=(i, ))
            p.start()
            processes.append(p)

        for process in processes:
            process.join()

        e_time = self.str2datetime(datetime.now())
        print "Finish testing at %s" % e_time

    def verify_no_loss_pac(self, concurency):
        int_list = []
        for f in self.ecg_folder_list:
            n = f.find("ID") + 2
            int_list.append(int(f[n:len(f)]))

        i = 1
        while i < concurency + 1:
            if i not in int_list:
                print "TestDeviceID%s is not in disk" % i
            i += 1

    def verify_upload_file_size(self, f):
        fs = os.listdir(f)
        for f1 in fs:
            tmp_path = os.path.join(f, f1)
            if not os.path.isdir(tmp_path):
                fsize = os.path.getsize(tmp_path)
                #print("file: %s, size: %s" % (tmp_path, fsize))
                if fsize != self.expect_file_size:
                    self.changed_size_file_list[tmp_path] = fsize
            else:
                #print("folder: %s" % tmp_path)
                sub_path = tmp_path.split('/')
                if sub_path[-1].find("TestDeviceID") != -1:
                    self.ecg_folder_list.append(sub_path[-1])
                self.verify_upload_file_size(tmp_path)

    def print_changed_file_size_list(self):
        for key, value in self.changed_size_file_list.items():
            print key, ' => size:', value

    def test_mutiple_device_concurrency_upload_10(self):
        concurrency = 10
        #self.upload_ecg(0)
        self.multi_process_ecg_upload(concurrency)
        self.verify_upload_file_size(self.tmp_path)
        self.print_changed_file_size_list()
        self.verify_no_loss_pac(concurrency)

    def test_mutiple_device_concurrency_upload_50(self):
        concurrency = 50
        #self.upload_ecg(0)
        self.multi_process_ecg_upload(concurrency)
        self.verify_upload_file_size(self.tmp_path)
        self.print_changed_file_size_list()
        self.verify_no_loss_pac(concurrency)

    def test_mutiple_device_concurrency_upload_100(self):
        concurrency = 100
        #self.upload_ecg(0)
        self.multi_process_ecg_upload(concurrency)
        self.verify_upload_file_size(self.tmp_path)
        self.print_changed_file_size_list()
        self.verify_no_loss_pac(concurrency)
