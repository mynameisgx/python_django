from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from app01.models import Department,UserInfo,PrettyNum
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination

def depart_list(request):
    depart_title=Department.objects.all()
    page_object = Pagination(request, depart_title, page_size=10)
    for obj in depart_title:
        obj.id,obj.title
    context = {
        'depart_title': depart_title,
        'page_string': page_object.html()
    }
    return render(request, 'depart_list.html',context)

def depart_add(request):
    if request.method == 'GET':
         return render(request,'depart_add.html')
    #获取提交过来的数据
    title=request.POST.get('title')
    #保存到数据库
    Department.objects.create(title=title)
    #重定向回部门列表
    return redirect('/depart/list/')


def depart_delete(request):
    #获取id
    nid=request.GET.get('nid')
    #删除
    Department.objects.filter(id=nid).delete()
    #重定向回部门列表
    return redirect('/depart/list/')

def depart_edit(request,nid):
    if request.method == 'GET':
        row_object = Department.objects.filter(id=nid).first()
        print(row_object.id, row_object.title)
        return render(request, 'depart_edit.html', {"row_object": row_object})
    #获取用户提交的标题
    title=request.POST.get('title')
    #根据id找到对应数据库数据并且更新
    Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')

def user_list(request):
    #获取所有的用户信息
    queryset=UserInfo.objects.all()
    page_object=Pagination(request,queryset,page_size=2)
    for obj in queryset:
        print(obj.id,obj.name,obj.password,obj.age,obj.account,obj.create_time.strftime("%Y-%m-%d"),obj.depart,obj.get_gender_display(),obj.depart.title)
    context={
        'queryset': page_object.page_queryset,
        'page_string':page_object.html()
    }
    return render(request, 'user_list.html',context)


def user_add(request):
    if request.method == 'GET':
        context ={
            'gender_choice':UserInfo.gender_choice,#元组
            'depart_list':Department.objects.all()#列表
        }
        return render(request, 'user_add.html',context)
    #获取用户提交的数据
    name=request.POST.get('name')
    pw=request.POST.get('pw')
    age=request.POST.get('age')
    account=request.POST.get('ac')
    time=request.POST.get('time')
    gender=request.POST.get('gender')
    depart=request.POST.get('depart')
    #将数据添加到数据库中
    UserInfo.objects.create(name=name,password=pw,age=age,account=account,create_time=time,gender=gender,depart_id=depart)
    #返回用户列表
    return redirect('/user/list/')

class UserModelForm(forms.ModelForm):
    #验证规则
    # name=forms.CharField(min_length=2,label='用户名')
    # password=forms.CharField(label='密码')
    class Meta:
        model=UserInfo
        fields=['name','password','age','account','create_time','gender','depart']
        print(fields)
        # widgets={
        #     'name': forms.TextInput(attrs={'class':'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class':'form-control'}),
        #     'age': forms.TextInput(attrs={'class':'form-control'})
        # }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
            #循环找到所有的插件，添加class="form-control"样式
        for name,field in self.fields.items():
                # if name=='password':
                #     continue
                #     print(name,field)
            field.widget.attrs={"class":"form-control","placeholder":field.label}
            #在ModelForm中，每个字段都有一个对应的widget对象，attrs是一个字典，用于存储HTML元素的属性。

#添加用户（modelform）
def user_model_form_add(request):
    if request.method=='GET':
        form=UserModelForm()
        return render(request,'user_model_form_add.html',{'form':form})
    form=UserModelForm(data=request.POST)
    #ModelForm封装了校验代码，我们调用is_valid()方法即可，它的返回值是Boolean类型，我们可以和if组合使用。如果是True，就可以通过cleaned_data属性查看数据；如果是False，就可以调用errors属性查看报错信息
    if form.is_valid():
        #如果数据合法，保存到数据库
        # UserInfo.objects.create()
        form.save()#is_valid()为True时，就得把cleaned_data写入数据库。
        return redirect('/user/list/')
    #校验失败，显示错误信息
    return render(request,'user_model_form_add.html',{'form':form})


def user_edit(request,nid):
    # 根据id获取要编辑的那行数据
    row_obj = UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':

        form=UserModelForm(instance=row_obj)#只要加上instance这个字段，modelform会自动将数据填充到表单中
        return render(request,'user_edit.html',{'form':form})


    form=UserModelForm(data=request.POST,instance=row_obj)#传入instance参数，让ModelForm知道，是改哪一行的值。
    if form.is_valid():
        #默认保存用户输入的所有值，如果想要在用户输入以外增加一点值，可设置form.instance.字段名=值
        form.save()#保存到数据库中
        return redirect('/user/list/')
    return render(request,'user_edit.html',{'form':form})#form会有错误信息

def user_delete(request,nid):
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


#靓号列表（查找）
def pretty_list(request):
    #创建300个数据
    # for i in range(300):
    #     PrettyNum.objects.create(mobile="22222222222",price=500,level=1,status=1)

    data_dict={}# 创建一个空字典，用于存储查询条件。
    search_data=request.GET.get('q','')#从请求的 GET 参数中获取名为 'q' 的值，如果没有获取到，则默认为空字符串。
    if search_data:
        data_dict['mobile__contains']=search_data#'mobilecontains' 表示对 'mobile' 字段进行包含搜索，键值为搜索数据。


    #根据用户想要访问的页码计算出起始位置
    queryset=PrettyNum.objects.filter(**data_dict).order_by('-level')
    page_object=Pagination(request,queryset)

    context={'queryset': page_object.page_queryset,#分完页的数据
             "search_data": search_data, #页码
             "page_string": page_object.html()}
    return render(request,'pretty_list.html',context)

class PrettyModelForm(forms.ModelForm):
    #校验提交的数据(方法1)
    # mobile=for  ms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1\d{11}$','手机号格式错误')]#必须以1开头并且必须是11位
    # )
    class Meta:
        model=PrettyNum
        fields=["mobile","price","level","status"]#自定义字段
        #fields="__all__"获取所有字段
        #exclude=["status"]#排除字段

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
            #循环找到所有的插件，添加class="form-control"样式
        for name,field in self.fields.items():
            field.widget.attrs={"class":"form-control","placeholder":field.label}
    #校验的方法2(钩子方法)
    def clean_mobile(self):
        txt_mobile=self.cleaned_data["mobile"]
        if len(txt_mobile)!=11:
            #验证不通过
            raise ValidationError("格式错误")
        #验证通过，返回用户提交的数据
        return txt_mobile

#靓号添加
def pretty_add(request):
    if request.method=="GET":
       form = PrettyModelForm()
       return render(request,'pretty_add.html',{'form':form})
    form =PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request,'pretty_add.html',{'form':form})


class PrettyEditModelForm(forms.ModelForm):
    # mobile=forms.CharField(disabled=True,label="手机号")#设置不可编辑
    #校验手机号是否11位
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1\d{10}$', '手机号格式错误')]  # 必须以1开头并且必须是11位
    )
    class Meta:
        model=PrettyNum
        fields=["mobile","price","level","status"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
            #循环找到所有的插件，添加class="form-control"样式
        for name,field in self.fields.items():
            field.widget.attrs={"class":"form-control","placeholder":field.label}
    #校验手机号是否重复

    def clean_mobile(self):
        print(self.instance.pk)
        txt_mobile=self.cleaned_data["mobile"]
        exists=PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        #验证通过，返回用户提交的数据
        return txt_mobile

def pretty_edit(request,nid):
    row_obj=PrettyNum.objects.filter(id=nid).first()
    if request.method=="GET":
        form=PrettyEditModelForm(instance=row_obj)#将 row_obj 对象传递给 instance 参数，以便在表单中显示该对象的数据。
        return render(request,'pretty_edit.html',{'form':form})
    form = PrettyEditModelForm(data=request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request,'pretty_edit.html',{'form':form})


def pretty_delete(request,nid):
    PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')