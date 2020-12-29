import xlrd
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'blog.settings'
django.setup()
from leeta.models import EnterpriseDirectory
data = xlrd.open_workbook(r'hunan_enterprise.xlsx')
sheets = data.sheets()
# print(EnterpriseDirectory.objects.all())
ls= []
for row in sheets[0].get_rows():
    temp={}
    temp["enterprise"] = row[0].value
    temp["phone_num"] =str(int(row[1].value)) if isinstance(row[1].value,float) else row[1].value
    temp["location"]=row[2].value
    temp["website"] = row[3].value
    temp["visited"] = False
    temp["phoned"] = True if row[5].value == '√' else False
    temp["phoned_status"] = 0
    temp["remark"] = row[6].value
    temp['legal_person'] = ""
    ls.append(temp)
for temp in ls:
    EnterpriseDirectory.objects.create(enterprise=temp["enterprise"],phone_num=temp["phone_num"],location=temp["location"],website=temp["website"],visited=temp["visited"],phoned=temp["phoned"],remark=temp["remark"],phoned_status=temp["phoned_status"],legal_person=temp["legal_person"])


