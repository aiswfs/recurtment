from django.contrib import admin
from jobs.models import Job
# Register your models here.


# 定义这个类可以自定义到后台管理界面列表页展示内容
class JobAdmin(admin.ModelAdmin):
    # 这里的作用是让这些字段为默认值同时不展示到填写页面
    exclude = ('creator', 'create_date', 'modified_date')
    
    # 加入想要展示的列 
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'create_date', 'modified_date')

    # 保存属性
    def save_model(self, request, obj, form, change):
        # 设置当前登录的用户设置为创建人
        obj.creator = request.user
        super().save_model(request, obj, form, change)


# 注册到管理后台
admin.site.register(Job, JobAdmin)
