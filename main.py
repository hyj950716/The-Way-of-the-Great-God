from Util import *
from data_handler import *
from html_report import report_html
import time
from send_mail import send_mail


total_test_case = 0  # 记录总共测试用例数
success_test_case = 0  # 记录成功用例数
failed_test_case = 0  # 记录失败用例数
test_cases_log_file_path = "test_interface_cases_procedure.log"
test_cases = get_test_data("test_data.txt")
test_results = []
for test_case in test_cases:  # 逐一执行测试用例
    #print("test_case",test_case)
    print("___" * 20, "new testcase:")
    print("test_case:",test_case)
    url = test_case[0]
    data = test_case[1]
    test_case_result = ""
    if "%" in data:  # 如果数据中有关联数据
        data = after_data_handler(data)  # 处理关联数据
    result_key = test_case[2]
    start_time = time.time()
    requst_type = test_case[4]
    r = send_request(url, data, requst_type)
    print("请求的接口地址：", r.url)
    print("请求请求的数据：", data)
    print("请求执行的结果：", r.text)
    end_time = time.time()
    test_time = int((end_time - start_time) * 1000)
    total_test_case += 1
    test_result = assert_result(r, result_key)
    if assert_result(r, result_key):
        success_test_case += 1
        test_case_result = "成功"
    else:
        failed_test_case += 1
        test_case_result = "失败"
    try:
        test_data_post_handler(r.text, test_case[3])
        print("获取关联变量成功")
    except Exception as e:
        print("从请求结果%s中，尝试获取关联变量失败，表达式%s" % (r.text, test_case[3]))
    test_results.append((r.url, data, r.text, test_time, test_case[3], test_case_result))
    write_test_case_execute_log(test_cases_log_file_path, url, requst_type, data, r.text, test_time,
                                test_result, result_key)

# 查看结果
output_test_result(total_test_case,success_test_case,failed_test_case)

html_name = '接口测试报告'
report_html(test_results, html_name)

send_mail()