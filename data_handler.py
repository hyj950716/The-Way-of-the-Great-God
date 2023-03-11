# encoding = utf-8
import re
from server_info import *
from Util import get_uniquenumber, md5

'''
前置条件：创建uniquenumber.txt文件存储数字，然后每次读取uniquenumber里面的数字，使用后将数字+1再写回去，可保证数字完全不会重复使用
'''
global_values = {}


def pre_data_handler(data):
    '''处理测试用例里面的数据参数'''
    global global_values
    if re.search(r"\$\{unique_\w+\}", data):  # 匹配用户名参数
        var_name = re.search(r"\$\{(unique_\w+)\}", data).group(1)
        var_name = var_name.split("_")[1]
        unique_num = get_uniquenumber()
        print("替换前 data:", data)
        data = re.sub(r"\$\{unique_\w+\}", unique_num, data)
        global_values[var_name] = str(unique_num)  # 将注册的用户名的唯一数取出用于后续用户名拼接
        print("替换后 data:", data)

    if re.search(r"\$\{(\w+)\}", data):  # 拼接登录等用户名
        # print("all", re.findall(r"\$\{(\w+)\}", data))
        for var_name in re.findall(r"\$\{(\w+)\}", data):
            print("替换前 data:", data)
            data = re.sub(r"\$\{%s\}" % var_name, str(global_values[var_name]), data)
            print("替换后 data:", data)

    if re.search(r"\$\{\w+\(.+\)\}", data):  # 匹配密码参数
        var_pass = re.search(r"\$\{(\w+\(.+\))\}", data).group(1)  # 获取密码参数
        print("替换前 data:", data)
        data = re.sub(r"\$\{\w+\(.+\)\}", eval(var_pass), data)  # 将data里面的参数内容通过eval修改为实际变量值
        print("替换前 data:", data)

    return data


def test_data_post_handler(data, regx):
    """拿到接口返回中需要后续接口使用的数据并存入到全局字典中"""
    global global_values
    if regx.lower().find("None") >= 0:  # 接口返回结果为空时，直接退出
        return
    var_name = regx.split("----")[0]
    regx_exp = regx.split("----")[1]
    if re.search(regx_exp, data):
        global_values[var_name] = re.search(regx_exp, data).group(1)

    return data


def get_test_data(data_file):
    '''读取测试数据文件获取测试数据'''
    test_cases = []
    with open(data_file, 'r') as fp:
        for line in fp:
            line = line.strip()
            interface_name = eval(line.split("||")[0].strip())
            print(interface_name)
            test_data = pre_data_handler(line.split("||")[1].strip())
            result_key = line.split("||")[2].strip()
            var_regx = line.split("||")[3].strip()
            request_type = line.split("||")[4].strip()
            test_cases.append((interface_name, test_data, result_key, var_regx, request_type))
    return test_cases


def after_data_handler(data):
    '''处理关联数据'''
    global global_values
    try:
        while re.search(r"\%\{\w+\}", data):
            var_name = re.search(r"\%\{(\w+)\}", data).group(1)
            print(var_name)
            print("关联替换前 data:", data)
            data = re.sub(r"\%\{(\w+)\}", global_values[var_name], data, 1)
            print("关联替换后 data:", data)
    except Exception as e:
        print(e)
    return data


# 测试数据
"""
if __name__ == "__main__":
    # data = '{"username":"hxf01${unique_num1}","password":"hxf950716","email": "hxf@qq.com"}'
    # print(pre_data_handler(data))
    print(get_test_data("test_data.txt"))
    data = '{"userid":%{userid}, "token": %{token}, "title":"python", "content":"python port test"}'
    print(after_data_handler(data))
"""

