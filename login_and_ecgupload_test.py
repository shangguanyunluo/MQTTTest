#!/usr/bin/python
# coding:utf-8
import time
import os
import test_base
import requests
import json
import unittest


class LoginAndEcgUploadTest(test_base.BaseTest):
    def setUp(self):
        test_base.BaseTest.setUp(self)

    # def login_device(self, index=0, success_code=200000):
    #     try:
    #         resp = requests.post(self.base_url + self.login_url,
    #                              json=json.loads(self.device_info[index]),
    #                              verify=False)
    #         user_dev_info = json.loads(resp.text)
    #         if success_code == eval(user_dev_info['code']):
    #             user_id = user_dev_info['data']['userId']
    #             device_id = user_dev_info['data']['deviceId']
    #             print user_id + " " + device_id
    #             return user_id, device_id
    #         else:
    #             raise Exception(
    #                 "user login error:%s" % user_dev_info['msg'])
    #     except Exception as e:
    #         print e.message
    #
    # def ecg_upload(self, device_index=0, delay=0):
    #     user_id, device_id = self.login_device(device_index)
    #     try:
    #         time.sleep(delay)
    #         topic = "sys/%s/%s/ecg/upload/device_%s" % (user_id, device_id,
    #                                                     device_index)
    #         data_file = os.path.join(self.ecg_file_path,
    #                                  '%s.bin' % device_index)
    #         print data_file
    #         pub_cmd = 'mosquitto_pub -h %s -p %s -i client_%s  -t "%s" -u %s -P %s -d --cafile %s --insecure -r -q 1 -f %s' % (
    #             self.server_ip, self.server_port, device_index, topic,
    #             self.username, self.password,
    #             self.cert_file, data_file)
    #
    #         print "pub_cmd is : %s" % pub_cmd
    #         cmd_result = os.system(pub_cmd)
    #         print cmd_result
    #     except Exception as e:
    #         print e.message

    def test_login_upload(self, delay=0):
        self.ecg_login_upload(device_index=3, delay=delay)

    # @unittest.skip('---------------')
    def test_login_upload_with_delay(self, delay=200):
        self.ecg_login_upload(device_index=4, delay=delay,
                              topic_suffix="delay")


if __name__ == '__main__':
    unittest.main()
