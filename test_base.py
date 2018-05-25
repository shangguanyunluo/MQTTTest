#!/usr/bin/env python

import unittest
import json, requests, time, os


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://{{ipaddress}}/api/test"
        self.login_url = "/device-service/device/login"
        self.logout_url = "/device-service/device/logout"
        self.server_ip = "{{ipaddress}}"
        self.server_port = "1883"
        self.username = "admin1"
        self.password = "passw0rd@"
        self.cert_file = "./ca.crt"
        self.ecg_file_path = "./sim_data_test_3_hours/"
        self.device_info = []

        self.get_device_list()

    def get_device_list(self):
        with open('device_info.txt', 'r') as f:
            self.device_info = f.read().split('\n')
            f.close()

        print "The len of device info is %s" % len(self.device_info)

    datefmt = "%Y-%m-%d %H:%M:%S.%f"

    def str2datetime(self, s, format=datefmt):
        dt = None
        try:
            dt = s.strftime(format)
        except (ValueError):
            dt = None
        finally:
            return dt

    def login_device(self, index=0, success_code=200000):
        resp = requests.post(self.base_url + self.login_url,
                             json=json.loads(self.device_info[index]),
                             verify=False)
        user_dev_info = json.loads(resp.text)
        if success_code == eval(user_dev_info['code']):
            user_id = user_dev_info['data']['userId']
            device_id = user_dev_info['data']['deviceId']
            print user_id + " " + device_id
            return user_id, device_id
        else:
            raise Exception(
                "user login error:%s" % user_dev_info['code'])

    def ecg_upload(self, user_id, device_id, filname_prefix=0,
                   topic_suffix=0, delay=0, client_index=0):
        """
        
        :param user_id: 
        :param device_id: 
        :param filname_prefix: the file you upload
        :param topic_suffix: the path and filename in the server
        :param delay: delay to upload
        :param client_index: the client who can receive the message or data
        :return: 
        """
        if user_id is None or device_id is None:
            raise Exception("user_id or device_id is null.")
        time.sleep(delay)
        data_file = os.path.join(self.ecg_file_path, '%s.bin' %
                                 filname_prefix)

        topic = "sys/%s/%s/ecg/upload/%s" % (user_id, device_id, topic_suffix)

        pub_cmd = 'mosquitto_pub -h %s -p %s -i client_%s  -t "%s" -u %s -P %s -d --cafile %s --insecure -r -q 1 -f %s' % (
            self.server_ip, self.server_port, client_index, topic,
            self.username, self.password,
            self.cert_file, data_file)

        print "pub_cmd is : %s" % pub_cmd
        try:
            cmd_result = os.system(pub_cmd)
        except Exception as e:
            raise Exception("Upload data error:%s" % e.message)
        print cmd_result

    def ecg_login_upload(self, device_index=0, delay=0, filname_prefix=0,
                         topic_suffix=0, client_index=0):
        user_id, device_id = self.login_device(device_index)

        self.ecg_upload(user_id, device_id, filname_prefix=filname_prefix,
                        topic_suffix=topic_suffix, delay=delay,
                        client_index=client_index)
