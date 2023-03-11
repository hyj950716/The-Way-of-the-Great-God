import requests
import json
import hashlib
import time


def get_uniquenumber():
    """读取用户名的数字部分，用于和合成唯一用户名"""
    with open("uniquenumber.txt", "r+", encoding="utf-8") as fp:
        uniquenumber = int(fp.read().strip())
        fp.seek(0, 0)
        fp.write(str(uniquenumber + 1))
    return str(uniquenumber)


def md5(data):
    """MD5加密数据"""
    m5 = hashlib.md5()
    m5.update(data.encode("utf-8"))
    md5_data = m5.hexdigest()
    return md5_data


def send_request(url, data, request_type):
    """请求接口，获取返回数据"""
    if "{" in data and "}" in data:  # 请求数据类型是字典格式
        if request_type == "post":
            print('post')
            response = requests.post(url, data)
        elif request_type == "get":
            response = requests.get(url, data)
        elif request_type == "put":
            print('put')
            response = requests.put(url, data)
    else:  # 请求数据类型非字典格式
        url = url + data
        if request_type == "post":
            response = requests.post(url)
        elif request_type == "get":
            response = requests.get(url)
        elif request_type == "put":
            response = requests.put(url)
    return response


def assert_result(response, key_word):
    """验证数据正确性"""
    global success_test_case
    global failed_test_case
    try:
        assert key_word in response.text  # 验证返回文本是否包含预期字段
        print('断言成功')
        return True
    except AssertionError as e:
        print('断言失败：')
        return False
    except:
        print('未知异常')
        return False


def output_test_result(total_test_cases,success_test_cases,failed_test_cases):
    """封装输出测试统计信息的函数"""
    print("---"*50)
    print("测试结果汇总：")
    print("一共执行了%s个测试用例" %total_test_cases)
    print("一共成功执行了%s个测试用例" %success_test_cases)
    print("一共失败执行了%s个测试用例" %failed_test_cases)


def write_test_case_execute_log(log_file_path, test_interface_url, test_interface_http_method, request_data,
                                response_data, elapse_time, assert_result, *assert_words):
    """把接口请求的所有信息，写入到指定的日志文件中"""
    """
    :param log_file_path:
    :param test_interface_url:
    :param test_interface_http_method:
    :param request_data:
    :param response_data:
    :param elapse_time:
    :param assert_result:
    :param assert_words:
    :return:
    """
    with open(log_file_path, "a", encoding="utf-8") as fp:
        fp.write("___________" * 10 + "\n")
        fp.write("测试执行时间：%s\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
        fp.write("接口请求地址：%s \n" % test_interface_url)
        fp.write("接口请求的http方法：%s \n" % test_interface_http_method)
        fp.write("接口请求的数据：%s \n" % request_data)
        fp.write("接口响应的结果：%s \n" % response_data)
        fp.write("接口响应的耗时：%s 秒\n" % elapse_time)
        if len(assert_words) > 1:
            for i in range(len(assert_words)):
                fp.write("接口的断言内容%s:%s\n" % (i + 1, assert_words[i]))
        if assert_result != "成功":
            fp.write("****************接口断言结果：%s \n" % assert_result)
        else:
            fp.write("接口断言结果：%s \n" % assert_result)
        fp.write("___________" * 10)

