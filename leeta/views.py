import functools
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import EnterpriseDirectory,User
import json

def login_required(func):
    @functools.wraps(func)
    def inner(request,*args,**kwargs):
        is_login = request.COOKIES.get('is_login')
        if is_login=="False" or is_login is None:
            return render(request,"login.html")
        else:
            return func(request, *args, **kwargs)
    return inner


def login(request):
    if request.POST:
        user_name = request.POST["user_name"]
        password = request.POST["password"]
        if not user_name.isdigit():
            users = User.objects.filter(user_name=user_name, password=password)
            if users:
                resp = render(request,"leeta_index.html",{"welcome_message":f"欢迎你{users[0].user_name}"})
                resp.set_cookie('is_login', True, expires=60*60*24*7)
                resp.set_cookie('user', users[0].user_name, expires=60*60*24*7)
                return resp
        elif user_name.isdigit():
            users = User.objects.filter(phone_num=int(user_name), password=password)
            if users:
                resp = render(request,"leeta_index.html",{"welcome_message":f"欢迎你{users[0].user_name}"})
                resp.set_cookie('is_login', True, expires=60*60*24*7)
                resp.set_cookie('user',users[0].user_name,expires=60*60*24*7)
                return resp
    resp = render(request,"login.html",{"error_message":"密码或者用户名输入错误，请重新输入。"})
    resp.set_cookie('is_login', False, expires=60)
    return resp



@login_required
def index(request):
    book_list=[1, 2, 3]
    user = request.COOKIES.get("user")
    return render(request,"leeta_index.html",{"book_list":book_list,"welcome_message":f"欢迎你{user}"})

# 展示所有企业
@login_required
def enterprises_show(request):
    print(request.COOKIES)
    ents = EnterpriseDirectory.objects.all().values()
    phone_status_map = {0:"未拨打" ,1:"错误号码" ,2:"打不通", 3:"接听但无效" ,4:"接听且有效"}
    for ent in ents:
        ent["visited"]="访问过了"if ent["visited"] else "没访问过"
        ent["phoned"]="已拨打" if ent["phoned"] else "未拨打"
        ent["phoned_status"]=phone_status_map[ent["phoned_status"]]
    return render(request,"show_ents.html",{"enterprises":ents})

@login_required
def enterprises_search(request):
    """
    :param request:
    :return:按企业名搜索和按照电话状态搜索
    """
    request.encoding = 'utf-8'
    phone_status_map = {0: "未拨打", 1: "错误号码", 2: "打不通", 3: "接听但无效", 4: "接听且有效"}
    if 'q' in request.GET and request.GET['q']:
        ents = EnterpriseDirectory.objects.filter(enterprise__contains=request.GET['q']).values()
        for ent in ents:
            ent["visited"] = "访问过了" if ent["visited"] else "没访问过"
            ent["phoned"] = "已拨打" if ent["phoned"] else "未拨打"
            ent["phoned_status"] = phone_status_map[ent["phoned_status"]]
        return render(request,"show_ents.html",{"enterprises":ents})
    else:
        message = '你提交了空表单'
    return HttpResponse(message)

@login_required
def enterprise_update(request):
    request.encoding = 'utf-8'
    if request.method == "GET":
        if 'ent_id' in request.GET and request.GET['ent_id']:
            ent = EnterpriseDirectory.objects.filter(id=int(request.GET['ent_id'])).values()[0]
            return render(request,"update.html",{"ent":ent})
        else:
            return HttpResponse("无效输入")
    else:
        text = dict(request.POST)
        print(request.POST)
        ent = EnterpriseDirectory.objects.get(id=int(text["ent_id"][0]))
        ent.enterprise = text["enterprise"][0]
        ent.phone_num = text["phone_num"][0]
        ent.location = text["location"][0]
        ent.website = text["website"][0]
        ent.visited = text["visited"][0] == "True"
        ent.phoned = text["phoned"][0] == "True"
        ent.phoned_date = text["phoned_date"][0]
        ent.remark = text["remark"][0]
        ent.legal_person = text["legal_person"][0]
        ent.phoned_date = text["phoned_date"][0]
        ent.save()
        return render(request,"update.html",{"ent":ent,"reminder":f"您已经成功修改{ent.enterprise}信息！！"})

