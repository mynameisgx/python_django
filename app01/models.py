from django.db import models
#部门表
class Department(models.Model):
    title = models.CharField(verbose_name='标题',max_length=32)
    #指定输出对象时所输出的内容
    def __str__(self):
        return self.title
# Department.objects.create(title='销售部')
# Department.objects.create(title='运营部')

#员工表
class UserInfo(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=16)
    password = models.CharField(verbose_name='密码',max_length=64)
    age=models.IntegerField(verbose_name='年龄')
    account=models.DecimalField(verbose_name='账户余额',max_digits=10,decimal_places=2,default=0)
    create_time=models.DateField(verbose_name='入职时间')#DateTimeField包含年月日和时分秒，DateField只包含年月日
    #有约束。to是与哪张表关联，to_field是与表中的那一列关联
    depart=models.ForeignKey(verbose_name='部门',to="Department",to_field="id",null=True,on_delete=models.CASCADE)
    #在django中的约束
    gender_choice=((1,"男"),(2,"女"))
    gender=models.SmallIntegerField(verbose_name="性别",choices=gender_choice)

#靓号表
class PrettyNum(models.Model):
    mobile=models.CharField(verbose_name="手机号",max_length=11)
    price=models.IntegerField(verbose_name="价格",default=0)#允许为空设置null=True
    level_choice={
        (1,"1级"),
        (2,"2级"),
        (3,"3级"),
        (4,"4级"),
    }
    level=models.SmallIntegerField(verbose_name="级别",choices=level_choice,default=1)#小整形
    status_choice={
        (1,"已占用"),
        (2,"未占用"),
    }
    status=models.SmallIntegerField(verbose_name="状态",choices=status_choice,default=2)

