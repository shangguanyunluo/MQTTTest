#!/usr/bin/python
# coding:utf-8

import os

import time

import logging

"""
# Use demo
#     sourceFile = "./sim_data_test_3_hours/0.bin"
#     targetFile = "./sim_data_test_3_hours/300MB.bin"
#     createFileWithSpecifizedSize(sourceFile, targetFile, "300mb")
"""


def createFileWithSpecifizedSize(sourceFile, targetFile, fileSize="1KB"):
    """self use,so only support GB,MB,KB,B"""
    fileSize = fileSize.upper()
    if fileSize.endswith("GB"):
        fileSize = eval(fileSize.replace("GB", "")) * 1024 * 1024 * 1024
    elif fileSize.endswith("MB"):
        fileSize = eval(fileSize.replace("MB", "")) * 1024 * 1024
    elif fileSize.endswith("KB"):
        fileSize = eval(fileSize.replace("KB", "")) * 1024
    elif fileSize.endswith("B"):
        fileSize = eval(fileSize.replace("B", ""))

    # print "fileSize is %s" % fileSize

    try:
        if os.path.getsize(targetFile) != 1:
            os.remove(targetFile)
    except Exception as e:
        print e.message

    write_number = 1
    # print "fileSize >= 1024: is %s" % fileSize >= 1024
    if fileSize >= 1024:
        write_number = fileSize / 1024
        fileSize = 1024

    # print "write_number is %s" % write_number

    with open(sourceFile, "r") as f:
        data = f.read(fileSize)
        target_file = open(targetFile, "a+")
        for i in range(write_number):
            target_file.write(data)
            target_file.flush()
        target_file.close()


def data_validation(path=None, user_id=None, device_id=None, file_num=0,
                    file_size=262152):
    if not file_num:
        return
    base_path = "/root/s3data/staging.smartvest.lenovo.com/%s/%s" % (
        user_id, device_id)

    if path is not None:
        real_path = os.path.join(base_path, path)
    else:
        upload_file = max(os.listdir(base_path))
        real_path = os.path.join(base_path, upload_file)
    logging.info("%s ,upload file path is : %s" % (user_id, real_path))
    file_list = os.listdir(real_path)
    num_list = range(file_num)
    for file_name in file_list:

        file_prefix = int(file_name.split("-")[0])
        if file_prefix in num_list:
            # print "-" * 20
            num_list.remove(file_prefix)
    if len(num_list) > 0:
        logging.error("%s ,upload file fail: we should upload %s files, " \
                      "there is %d " "files didn't upload succeed. fail "
                      "file is : %s" % (user_id, file_num, len(num_list),
                                        num_list))
        raise Exception("%s,upload file fail: we should upload %s files, " \
                        "there is %d " "files didn't upload succeed. fail "
                        "file is : %s" % (user_id, file_num, len(num_list),
                                          num_list))
    logging.info("%s ,upload file number is equal with the server" % user_id)
    data_integrity_valitation(source_data_size=file_num * file_size,
                              target_file_path=real_path)


def data_integrity_valitation(source_data_size, target_file_path):
    tar_file_list = os.listdir(target_file_path)
    target_file_size = 0
    for tar_file in tar_file_list:
        try:
            tar_file = os.path.join(target_file_path, tar_file)
            target_file_size += os.path.getsize(tar_file)
        except:
            logging.error("tar_file is : %s" % tar_file)
            # time.sleep(2)
            # target_file_size += os.path.getsize(tar_file)
    user_id = target_file_path.split("/")[4]
    if source_data_size != target_file_size:
        logging.error("Upload file size is %s , actual size is %d, "
                      "user_id is : %s." % (
                          source_data_size, target_file_size, user_id))
        raise Exception("Upload file size is %s , actual size is %d, "
                        "user_id is : %s." % (
                            source_data_size, target_file_size, user_id))
    logging.info("%s ,the file you upload is complete." % user_id)


def validate_upload_files(process_num=1, file_num=0, file_size=262152):
    if process_num < 1:
        return
    upload_process_error_number = 0
    upload_fail_list = []
    process_num += 1
    for i in range(1, process_num):
        try:
            user_id = "TestUserID%s" % i
            device_id = "TestDeviceID%s" % i
            data_validation(user_id=user_id, device_id=device_id,
                            file_num=file_num, file_size=file_size)
        except:
            upload_process_error_number += 1
            upload_fail_list.append(user_id)
            pass
    return upload_process_error_number, upload_fail_list


if __name__ == '__main__':
    print validate_upload_files(50, 1000)
    pass
