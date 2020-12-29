from django.shortcuts import render
from .models import EnterpriseDirectory
# Create your views here.
def index(request):
    book_list=[1, 2, 3]
    return render(request,"index.html",{"book_list":book_list,"string":"111"})

def enterprises_show(request):
    ents = EnterpriseDirectory.objects.all().values()
    phone_status_map = {0:"未拨打" ,1:"错误号码" ,2:"打不通", 3:"接听但无效" ,4:"接听且有效"}
    for ent in ents:
        ent["visited"]="访问过了"if ent["visited"] else "没访问过"
        ent["phoned"]="已拨打" if ent["phoned"] else "未拨打"
        ent["phoned_status"]=phone_status_map[ent["phoned_status"]]


    return render(request,"show_ents.html",{"enterprises":ents})