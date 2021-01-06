from django.db import models
from datetime import date
import functools
from django.shortcuts import render
class User(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=20, primary_key=True)

    class Meta:
        db_table = 'leeta_user'

    def login_required(func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            is_login = request.COOKIES.get('is_login')
            if is_login == "False" or is_login is None:
                return render(request, "login.html")
            else:
                return func(request, *args, **kwargs)

        return inner

class EnterpriseDirectory(models.Model):
    enterprise = models.CharField(max_length=100)  # 企业名称
    phone_num = models.CharField(max_length=50, blank='')  # 企业电话
    location = models.CharField(max_length=200, blank=True)  # 企业地址
    website = models.CharField(max_length=100, blank=True)  # 企业官网
    visited = models.BooleanField(default=False)  # 是否拜访
    phoned = models.BooleanField(default=False)  # 是否拨打
    phoned_status = models.IntegerField(default=0)  # 拨打状态 0、未拨打 1、错误号码 2、打不通 3、接听但无效 4、接听且有效 5、沟通完成
    phoned_date = models.DateField(default=date.today().__str__())  # 拨打日期
    remark = models.CharField(max_length=500)  # 备注
    legal_person = models.CharField(max_length=50, blank=True)  # 企业法人
    registrant = models.CharField(max_length=50, default="17680152306")
    insert_date = models.DateField(default=date.today().__str__())
    contact = models.CharField(default="", max_length=40)
    enterprise_situation = models.CharField(default="", max_length=1000)

    def __str__(self):
        return self.enterprise

    class Meta:  # 按时间下降排序
        db_table = 'leeta_enterprise_directory'

    @classmethod
    def convert_display_form(cls,ents):
        phone_status_map = {0: "未拨打", 1: "错误号码", 2: "打不通", 3: "接听但无效", 4: "接听且有效", 5: "沟通完成"}
        for ent in ents:
            ent.visited = "已访问" if ent.visited else "未访问"
            ent.phoned = "已拨打" if ent.phoned else "未拨打"
            ent.phoned_status = phone_status_map[ent.phoned_status]
        return ents

    @classmethod
    def search_enterprises(cls,post):
        enterprise = post["enterprise"][0]
        phoned_status = int(post["phoned_status"][0])
        phoned_date_start = post["phoned_date_start"][0]
        phoned_date_end = post["phoned_date_end"][0]
        insert_date_start = post["insert_date_start"][0]
        insert_date_end = post["insert_date_end"][0]
        ents = EnterpriseDirectory.objects.all()
        if enterprise:
            ents = ents.filter(enterprise__contains=enterprise)
        if phoned_status != -1:
            ents = ents.filter(phoned_status=phoned_status)
        # 按拨打日期分类
        if phoned_date_start and phoned_date_end:
            ents = ents.filter(
                phoned_date__range=[date.fromisoformat(phoned_date_start), date.fromisoformat(phoned_date_end)])
        elif phoned_date_start:
            ents = ents.filter(phoned_date__range=[date.fromisoformat(phoned_date_start), date.today()])
        elif phoned_date_end:
            ents = ents.filter(
                phoned_date__range=[date.fromisoformat("2020-11-14"), date.fromisoformat(phoned_date_end)])
        # 按录入日期分类
        if insert_date_start and insert_date_end:
            ents = ents.filter(
                insert_date__range=[date.fromisoformat(insert_date_start), date.fromisoformat(insert_date_end)])
        elif insert_date_start:
            ents = ents.filter(insert_date__range=[date.fromisoformat(insert_date_start), date.today()])
        elif insert_date_end:
            ents = ents.filter(
                insert_date__range=[date.fromisoformat("2020-11-14"), date.fromisoformat(insert_date_end)])
        ents = cls.convert_display_form(ents)
        return ents


