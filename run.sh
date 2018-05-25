nosetests -s test_ecg_upload.py:ECGUploadTest.test_mutiple_device_concurrency_upload

nosetests -s login_and_ecgupload_test:LoginAndEcgUploadTest.test_login_upload

nosetests -s login_and_ecgupload_test:LoginAndEcgUploadTest.test_login_upload_with_delay

nosetests -s ecg_upload_specifized_file_test:ECGUploadSpecifizedFileTest.testUploadFile1B

nosetests -s ecg_upload_specifized_file_test:ECGUploadSpecifizedFileTest.testUploadFile256KB

nosetests -s ecg_upload_specifized_file_test:ECGUploadSpecifizedFileTest.testUploadFile300KB

nosetests -s ecg_upload_continuously_test:ECGUploadContinuouslyTest.test_continue_upload_in300s

nosetests -s ecg_upload_continuously_test:ECGUploadContinuouslyTest.test_noncontinue_upload_in300s

nosetests -s ecg_upload_continuously_test:ECGUploadContinuouslyTest.test_continue_upload_greater_than_300s

nosetests -s ecg_upload_continuously_test:ECGUploadContinuouslyTest.test_continue_upload_file_1_5GB

nosetests -s ech_network_failure_upload_test:ECGNetworkFailureUploadTest.test_network_latency_upload

nosetests -s ech_network_failure_upload_test:ECGNetworkFailureUploadTest.test_network_pack_repeat_upload