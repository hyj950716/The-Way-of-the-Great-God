ip = "101.42.247.45"
port = "8080"

register = "http://%s:%s/register/" % (ip, port)  # 用户注册
login = "http://%s:%s/login/" % (ip, port)  # 用户登录
create = "http://%s:%s/create/" % (ip, port)  # 创建博文
getBlogsOfUser = "http://%s:%s/getBlogsOfUser/" % (ip, port)  # 查询用户的博文
update = "http://{}:{}/update/".format(ip, port)  # 修改博文
getBlogContent = "http://%s:%s/getBlogContent/" % (ip, port)  # 查询博文内容
getBlogsContent = "http://%s:%s/getBlogsContent/articleIds=" % (ip, port)  # 批量查询博文内容
delete = "http://%s:%s/delete/" % (ip, port)  # 批量查询博文内容
