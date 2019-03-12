
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.db import DatabaseError
import logging
from django.contrib import auth


# Create your views here.
from userinfo.models import *


def register_(request):
    #判断post还是get
    if request.method == 'POST':
        new_user = UserInfo()
        new_user.username = request.POST.get('username')
        olduser = UserInfo.objects.filter(username=new_user.username)
        print(olduser)
        if olduser:
            return render(request,'register.html',{'msg':'用户名已存在'})
        if request.POST.get('upwd') != request.POST.get('cpwd'):
            return render(request,'register.html',{'msg':'密码不一致'})
        new_user.password = make_password(request.POST.get('upwd'),None,'pbkdf2_sha1')
        try:
            new_user.save()
        except DatabaseError as e:
            logging.warning(e)
        if 'tobuy' in request.POST:
            return render(request,'index.html')
        elif 'tosale' in request.POST:
            return render(request,'info-message.html')

    elif request.method == 'GET':
        return render(request, 'register.html')

#get返回注册页面
#post
#　　获取数据
# 　　判断用户名是否存在
#      存在：返回注册页面
# 　　　不存在：
# 　　　　　判断密码是否一致
# 　　　　　密码加密
# 　　　　　保存用户
# 　　判断卖车买车
# 　　　买车：首页
# 　　　卖车：完善卖车信息

def login_(request):
    # 1.判断post/get
    # 2.get:返回登录页
    # 3.post:
    # 　　　查询用户名
    # 　　　　　不存在：返回登录页用户名不存在
    # 　　　　　
    # 　　　获取数据库中该用户密码
    # 　　　check_password(前端获取密码和数据库密码)
    # 　　　　　False:返回登录页，密码错误
    # 　　　session:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('upwd')
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None and user.is_active:
            auth.login(request,user)
            return render(request, 'info-message.html')
        else:
            return render(request,'login.html',{'msg':'用户名密码错误'})
    elif request.method =='GET':
        return render(request,'login.html')

def loginout(request):
    auth.logout(request)
    return render(request,'index.html')

def salecar(request):
    # 1.POST/GET
    # 2.获取信息：用户信息userinfo
    #             所卖车型信息carinfo
    # 下拉列表　单选　图片
    # 3.保存
    if request.method == 'POST':
        cellname = request.POST.get('')