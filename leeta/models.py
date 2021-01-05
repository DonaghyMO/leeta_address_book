from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=20,primary_key=True)
    class Meta:
        db_table = 'leeta_user'

class EnterpriseDirectory(models.Model):
    enterprise = models.CharField(max_length = 100)  #企业名称
    phone_num = models.CharField(max_length = 50, blank = '')  #企业电话
    location = models.CharField(max_length = 200,blank=True)  #企业地址
    website = models.CharField(max_length = 100,blank=True) # 企业官网
    visited = models.BooleanField(default=False)  #是否拜访
    phoned = models.BooleanField(default=False)  #是否拨打
    phoned_status = models.IntegerField(default=0) #拨打状态 0、未拨打 1、错误号码 2、打不通 3、接听但无效 4、接听且有效
    phoned_date = models.CharField(max_length=100)# 拨打日期
    remark = models.CharField(max_length=500) #备注
    legal_person = models.CharField(max_length=50,blank=True) #企业法人
    registrant = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.enterprise
    class Meta:  #按时间下降排序
        db_table = 'leeta_enterprise_directory'



