import json
j = """
{"login":"登录","register":"注册","noAccount":"没有账号?点我注册!","submit":"提交","logged":"你已经登陆过了!","password":"密码","username":"用户名","fillThis":"填写此字段","post":"帖子","postTitle":"帖子标题","postList":"帖子列表","user":"用户","userList":"用户列表","plzLogin":"访客,请先登录","newMembers":"新成员","newPost":"新帖子","reload":"重新加载","cancel":"取消","copyright":"版权所有","sureReload":"你确定重新加载吗?","dataLoss":"未保存的数据将会丢失!","loginError":"登录失败,请检查网络连接!","notFoundTitle":"未找到您访问的路由记录","notFoundCheckUrl":"检查您是否拼错URL?","backHome":"返回主页","noData":"没有数据","networkError":"网络错误","jumpTip":"跳转提示","missingArg":"参数缺失","back":"返回","newBlankAndBack":"在新标签页打开并返回","notBelong":"不属于","continueTo":"继续前往","logout":"登出","logoutDone":"登出成功","notLogin":"未登录"}
"""

jObj = json.loads(j)

sObj = sorted(jObj.items(), key=lambda x: x[0], reverse=False)

print(json.dumps(dict(sObj), ensure_ascii=False))
