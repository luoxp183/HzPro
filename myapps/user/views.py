import json
import uuid

import os

from django.contrib.auth.hashers import check_password
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from HArtPro import settings
from user import helper
from user.forms import UserForm
from user.models import UserProfile


def regist(request):
    if request.method == 'POST':
        # 读取 request.POST字典中的数据，借助UserProfile模型保存到数据库
        # 通过ModelForm模型表单类 验证数据并保存到数据库中
        userForm = UserForm(request.POST)
        if userForm.is_valid(): # 判断必须要字段是否都存在数据
            user = userForm.save()  # 保存数据
            # 注册成功,将用户的id,用户名和头像地址写入到session(同时session数据存入到redis缓存中)
            helper.addLoginSession(request,user)

            return redirect('/')

        # post提交时有验证错误，将验证错误转成json－> dict对象
        errors = json.loads(userForm.errors.as_json())
        print(errors)

    return render(request, 'user/regist.html', locals())


@csrf_exempt  # 不需要crsf_token的验证
def uploadPhoto(request):
    # 上传头像-> request.FILES 字典中 ｛'字段名': InMemoryUploadedFile｝
    if request.method == 'POST':
        uploadFile:InMemoryUploadedFile = request.FILES.get('photoImg')  # 上传文件表单的字段名为photoImg

        # 生成新的文件名
        newFileName = str(uuid.uuid4()).replace('-', '')+'.'+uploadFile.name.split('.')[-1]

        # 确定生成新的文件的目录
        dirPath = os.path.join(settings.BASE_DIR, 'static/users/photo/')
        if not os.path.exists(dirPath):  # 判断目录是否存在
            os.makedirs(dirPath)

        with open(os.path.join(dirPath, newFileName), 'wb') as f:
            for chunk in uploadFile.chunks():   # 分段的方式写入到新的文件中(缓存块)
                f.write(chunk)

        return JsonResponse({'status': 200,
                             'path': '/static/users/photo/'+newFileName})

    return JsonResponse({'status': 200,
                         'msg': '上传失败，目前请求只支持POST!'})


def logout(request):
    login_user = helper.getLoginInfo(request)
    if login_user:
        # 从session中删除登录信息
        del request.session['login_user']
        # request.session.clear()
    return redirect('/')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')

        errors = {}
        if not username or len(username.strip()) < 8:
            errors['username'] = [{'message': '用户名不能为空或不能低于8位字符'}]

        if not passwd or len(passwd.strip()) < 8:
            errors['passwd'] = [{'message': '口令不能为空或不能低于8位字符'}]

        if not errors:
            # 验证通过
            qs = UserProfile.objects.filter(username=username)  # 返回queryset 查询结果
            if not qs.exists():
                errors['username'] = [{'message': '查无此用户!'}]
            else:
                user = qs.first()  # 读取查询结果中第一条记录
                if not check_password(passwd, user.passwd):
                    errors['passwd'] = [{'message': '口令错误！'}]
                else:
                    helper.addLoginSession(request, user)
                    return redirect('/')

    return render(request, 'user/login.html', locals())