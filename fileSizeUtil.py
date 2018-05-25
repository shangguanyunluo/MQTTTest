#!/usr/bin/python
# coding:utf-8

import os


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


# if __name__ == '__main__':
#     sourceFile = "./sim_data_test_3_hours/0.bin"
#     targetFile = "./sim_data_test_3_hours/300MB.bin"
#     createFileWithSpecifizedSize(sourceFile, targetFile, "300mb")
