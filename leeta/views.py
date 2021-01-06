import functools
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import EnterpriseDirectory, User
from datetime import date

def login(request):
    if request.method == "POST":
        user_name = request.POST["user_name"]
        password = request.POST["password"]
        if not user_name.isdigit():
            users = User.objects.filter(user_name=user_name, password=password)
            if users:
                resp = render(request, "leeta_index.html", {"welcome_message": f"欢迎你{users[0].user_name}"})
                resp.set_cookie('is_login', True, expires=60 * 60 * 24 * 7)
                resp.set_cookie('user', users[0].phone_num, expires=60 * 60 * 24 * 7)
                return resp
        elif user_name.isdigit():
            users = User.objects.filter(phone_num=int(user_name), password=password)
            if users:
                resp = render(request, "leeta_index.html", {"welcome_message": f"欢迎你{users[0].phone_num}"})
                resp.set_cookie('is_login', True, expires=60 * 60 * 24 * 7)
                resp.set_cookie('user', users[0].phone_num, expires=60 * 60 * 24 * 7)
                return resp
    resp = render(request, "login.html", {"error_message": "密码或者用户名输入错误，请重新输入。"})
    resp.set_cookie('is_login', False, expires=60)
    return resp


def logout(request):
    if request.method == "GET":
        resp = render(request, "login.html")
        resp.delete_cookie('user')
        resp.delete_cookie('is_login')
        return resp



def modify_password(request):
    if request.method == "POST":
        user_name = request.POST["user_name"]
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        if not user_name.isdigit():
            users = User.objects.filter(user_name=user_name, password=old_password)
            if users:
                users[0].password = new_password
                users[0].save()
                resp = render(request, "leeta_index.html", {"welcome_message": f"欢迎你{users[0].user_name}"})
                resp.set_cookie('is_login', True, expires=60 * 60 * 24 * 7)
                resp.set_cookie('user', users[0].phone_num, expires=60 * 60 * 24 * 7)
                return resp
        elif user_name.isdigit():
            users = User.objects.filter(phone_num=int(user_name), password=old_password)
            if users:
                users[0].password = new_password
                users[0].save()
                resp = render(request, "leeta_index.html", {"welcome_message": f"欢迎你{users[0].phone_num}"})
                resp.set_cookie('is_login', True, expires=60 * 60 * 24 * 7)
                resp.set_cookie('user', users[0].phone_num, expires=60 * 60 * 24 * 7)
                return resp
    message = "用户名或者密码错误" if request.method == "POST" and not users else ""
    return render(request, "modify_password.html", {"message": message})


@User.login_required
def index(request):
    book_list = [1, 2, 3]
    user = request.COOKIES.get("user")
    return render(request, "leeta_index.html", {"book_list": book_list, "welcome_message": f"欢迎你{user}"})


# 展示所有企业
@User.login_required
def enterprises_show(request):
    if request.method=="GET":
        ents = EnterpriseDirectory.objects.all()
        return render(request, "show_ents.html", {"enterprises": EnterpriseDirectory.convert_display_form(ents)})


@User.login_required
def enterprises_search(request):
    request.encoding = 'utf-8'
    if request.method == "POST":
        post = dict(request.POST)
        ents = EnterpriseDirectory.search_enterprises(post)
        return render(request, "show_ents.html", {"enterprises": ents})


@User.login_required
def enterprise_update(request):
    request.encoding = 'utf-8'
    if request.method == "GET":
        if 'ent_id' in request.GET and request.GET['ent_id']:
            ent = EnterpriseDirectory.objects.filter(id=int(request.GET['ent_id']))[0]
            ent.phoned_date = ent.phoned_date.__str__()
            return render(request, "update.html", {"ent": ent})
    else:
        text = dict(request.POST)
        print(text)
        ent = EnterpriseDirectory.objects.get(id=int(text["ent_id"][0]))
        try:
            phoned_date = date.fromisoformat(text["phoned_date"][0])
            phoned_date = phoned_date.__str__()
        except Exception:
            return render(request, "update.html", {"ent": ent, "reminder": "日期输入有误输入格式为“年-月-日 例如：2021-01-05”，请重新输入"})
        if "phoned_status" in text.keys():
            ent.phoned_status = int(text["phoned_status"][0])
        ent.phoned_date = ent.phoned_date.__str__()
        ent.enterprise = text["enterprise"][0]
        ent.phone_num = text["phone_num"][0]
        ent.location = text["location"][0]
        ent.website = text["website"][0]
        if "phoned" in text.keys():
            ent.phoned = text["phoned"][0] == "1"
        if "visited" in text.keys():
            ent.visited = text["visited"][0] == "1"
        else:
            ent.visited = False
        ent.phoned_date = phoned_date
        ent.remark = text["remark"][0]
        ent.contact = text["contact"][0]
        ent.ent_situation = text["ent_situation"][0]
        ent.legal_person = text["legal_person"][0]
        ent.save()
        return render(request, "update.html", {"ent": ent, "reminder": f"已经成功修改{ent.enterprise}信息！！"})


@User.login_required
def enterprise_insert(request):
    if request.method == "GET":
        return render(request, "enterprise_insert.html")
    elif request.method == "POST":
        ent = dict(request.POST)
        if EnterpriseDirectory.objects.filter(enterprise__contains=ent["enterprise"][0]):
            return render(request, "enterprise_insert.html", {"message": "此公司已经在数据库中！！"})
        EnterpriseDirectory.objects.create(enterprise=ent["enterprise"][0],
                                           phone_num=ent["phone_num"][0],
                                           location=ent["location"][0],
                                           website=ent["website"][0],
                                           legal_person=ent["legal_person"][0],
                                           registrant=request.COOKIES.get("user")
                                           )
        return render(request, "enterprise_insert.html", {"message": "添加成功！！"})
