#!/usr/bin/env python


import unittest
import json, requests, time, os
import logging

fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.DEBUG,
    # format='LINE %(lineno)-4d %(levelname)-8s %(message)s',
    format=fmt,
    datefmt='%Y/%m/%d %H:%M:%S',
    filename='smartvest.log',
    filemode='w',

)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(fmt)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://43.255.224.58/api/test"
        self.login_url = "/device-service/device/login"
        self.logout_url = "/device-service/device/logout"
        self.server_ip = "43.255.224.120"
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

    def str2datetime(self, now):
        return time.strftime("%Y-%m-%d %H:%M:%S", now)

    def login_device(self, index=0, success_code=200000, try_time=2):
        try:
            login_status = False
            for i in range(try_time):
                # logging.info("Device %s, The %s time to Login " % (index, i,))
                resp = requests.post(self.base_url + self.login_url,
                                     json=json.loads(self.device_info[index]),
                                     verify=False)
                user_dev_info = json.loads(resp.text)
                if success_code == eval(user_dev_info['code']):
                    # if i == 0: continue
                    login_status = True
                    break
            # logging.info("login_status is %s" % login_status)
            if not login_status:
                logging.error("%s Login fail:%s" % (index,))
                raise Exception("%s re_login fail" % index)

            user_id = user_dev_info['data']['userId']
            device_id = user_dev_info['data']['deviceId']
            logging.info("%s login success" % user_id)
            return user_id, device_id
        except Exception as e:
            logging.error("%s Login fail:%s" % (index, e))
            raise Exception("%s login fail" % index)

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

        pub_cmd = 'mosquitto_pub -h %s -p %s -i client_%s  -t %s -u %s -P %s -d --cafile %s --insecure -r -q 1 -f %s' % (
            self.server_ip, self.server_port, client_index, topic,
            self.username, self.password,
            self.cert_file, data_file)

        logging.info("pub_cmd is : %s" % pub_cmd)
        try:
            response = os.system(pub_cmd)
            if response != 0:
                response = os.system(pub_cmd)
        except:
            response = os.system(pub_cmd)
        finally:
            logging.info("%s file num %d response is : %s" % (
                user_id, topic_suffix, response))

    def ecg_upload2(self, user_id, device_id, upload_file_num=1,
                    source_filname_range=100, client_index=0, delay=0,
                    test_mode=False):
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

        for filname_prefix in range(upload_file_num):
            topic_suffix = filname_prefix
            filname_prefix %= source_filname_range
            data_file = os.path.join(self.ecg_file_path,
                                     '%s.bin' % filname_prefix)

            topic = "sys/%s/%s/ecg/upload/%s" % (
                user_id, device_id, topic_suffix)

            pub_cmd = 'mosquitto_pub -h %s -p %s -i client_%s  -t %s -u %s -P %s -d --cafile %s --insecure -r -q 1 -f %s' % (
                self.server_ip, self.server_port, client_index, topic,
                self.username, self.password,
                self.cert_file, data_file)

            logging.info("pub_cmd is : %s" % pub_cmd)
            if not test_mode:
                try:
                    response = os.system(pub_cmd)
                    if response != 0:
                        response = os.system(pub_cmd)
                except:
                    response = os.system(pub_cmd)
                finally:
                    logging.info("%s file num %d response is : %s" % (
                        user_id, topic_suffix, response))

    # def ecg_upload_files(self, user_id, device_id, filname_range=(0, 100),
    #                      delay=0, client_index=0):
    #     """
    #
    #     :param user_id:
    #     :param device_id:
    #     :param filname_prefix: the file you upload
    #     :param topic_suffix: the path and filename in the server
    #     :param delay: delay to upload
    #     :param client_index: the client who can receive the message or data
    #     :return:
    #     """
    #     for filname_prefix in range(filname_range[0], filname_range[-1]):
    #         self.ecg_upload(user_id, device_id, filname_prefix=filname_prefix,
    #                         topic_suffix=filname_prefix, delay=delay,
    #                         client_index=client_index)

    def ecg_login_upload(self, device_index=0, delay=0, filname_prefix=0,
                         topic_suffix=0, client_index=0):
        user_id, device_id = self.login_device(device_index)

        self.ecg_upload(user_id, device_id, filname_prefix=filname_prefix,
                        topic_suffix=topic_suffix, delay=delay,
                        client_index=client_index)
        return user_id, device_id

    def upload_file_intervial(self, user_id, device_id, time_period=300,
                              time_interval=45, source_filname_range=100):
        """
        topic_suffix : use this to distinguish which method call this method
        time_period : the whole time to upload files
        time_interval : the time between you upload two files
        file_num :the number of file you will uploads in the time_period
        :return:
        """
        file_num = 0
        start_time = time.time()
        continue_flag = True
        while continue_flag:
            now_time = time.time()
            if int(now_time - start_time) >= time_period:
                continue_flag = False

            filname_prefix = file_num % source_filname_range

            self.ecg_upload(user_id, device_id, filname_prefix=filname_prefix,
                            topic_suffix=file_num)
            file_num += 1
            if continue_flag:
                time.sleep(time_interval)
        return file_num
