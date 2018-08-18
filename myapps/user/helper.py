import json


def getLoginInfo(request)-> dict:
    '''
    获取当前登录用户的信息
    :param request: 请求对象
    :return: 返回None或 {'id':1,'name':'x', 'photo':'/static/xxx.png' }
    '''
    login_user = request.session.get('login_user')
    if login_user:
        login_user = json.loads(login_user)  # 将字符串转成 dict对象

    print('--getLoginInfo---->',login_user)
    return login_user

def addLoginSession(request, user):
    '''
    向session中添加登录用户的信息
    :param request:
    :param user:
    :return:
    '''
    request.session['login_user'] = json.dumps({'id': user.id,
                                                'name': user.username,
                                                'photo': user.photo})