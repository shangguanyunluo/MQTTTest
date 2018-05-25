
import test_base
import requests
import json
import os
from datetime import datetime
#from multiprocessing import Pool
import multiprocessing
import subprocess


class UploadTestWithNetFault(test_base.BaseTest):

    def setUp(self):
        test_base.BaseTest.setUp(self)

        self.network = "eno1"
        self.loss_start = 10
        self.loss_end = 20

        self.random_package_loss(self.network, self.loss_start, self.loss_end)

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

    def random_package_loss(self, network, start, end):
        cmd_check = "tc qdisc"
        os.system(cmd_check)

        cmd = "tc qdisc add dev %s root netem loss %s %s" % (network, start, end)
        os.system(cmd)

        child = subprocess.Popen(cmd_check, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
        line = child.stdout.readline()
        print line

    def remove_loss_pack(self, network):
        cmd = "tc qdisc del dev eno1 root"
        os.system(cmd)

        cmd_check = "tc qdisc"
        child = subprocess.Popen(cmd_check, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
        line = child.stdout.readline()
        print line

    def test_network_loss_pac(self):
        concurrency = 2
        #self.upload_ecg(0)
        self.multi_process_ecg_upload(concurrency)

    def tearDown(self):
        self.remove_loss_pack(self.network)