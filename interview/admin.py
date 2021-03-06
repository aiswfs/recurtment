import codecs
import csv
import logging
from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse

from interview.models import Candidate

# Register your models here.

logger = logging.getLogger(__name__)

exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'degree', 'first_score', 'first_result',
                     'first_interviewer_user', 'second_result', 'second_interviewer_user', 'hr_score', 'hr_result',
                     'hr_interviewer_user')


# 定义actions里面的自定义功能
def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response.write(codecs.BOM_UTF8)
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=recruitment-candidates-list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )

    for object in queryset:
        # 当行的记录
        csv_line = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(object)
            csv_line.append(field_value)
        writer.writerow(csv_line)

    logger.info("%s exported %s candidates recoreds" % (request.user, len(queryset)))
    return response


# 定义actions中的中文显示
export_model_as_csv.short_description = "以CSV格式导出应聘者信息"


class CandidateAdmin(admin.ModelAdmin):
    # 设置行动里面的字段(功能)
    actions = [
        export_model_as_csv,
    ]

    # 修改页面隐藏字段
    exclude = ('creator', 'created_date', 'modified_date')

    # 展示字段
    list_display = (
        'username', 'city', 'bachelor_school', 'first_score', 'first_result', 'first_interviewer_user',
        'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'last_editor'
    )

    # 设置可以搜索的字段   查询字段
    search_fields = (
        'username',
        'phone',
        'email',
        'bachelor_school',
    )

    # 设置筛选字段
    list_filter = (
        'city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user', 'second_interviewer_user',
        'hr_interviewer_user'
    )

    ordering = (
        'hr_result', 'second_result', 'first_result',
    )

    # 获取登录的用户的群组角色列表
    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    # 设置只读字段（详情页修改面试官）
    # # plane 1:对所有的用户只读
    # readonly_fields = (
    #     'first_interviewer_user', 'second_interviewer_user', 'hr_interviewer_user'
    # )
    # plane 2:对对应的用户只读
    def get_readonly_fields(self, request, obj):
        # 先获取登录的账号所属于的群组角色
        group_names = self.get_group_names(request.user)

        # 如果interviewer在他的角色列表里面 就返回readonly_fields字段
        if '面试官' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    # 总页面修改面试官
    # # plane 1:直接指定哪些字段可以编辑 缺点：没有权限控制，对所有的用户都能使用
    # list_editable = (
    #     'first_interviewer_user', 'second_interviewer_user',
    # )
    # plane 2:只让hr才能看到list_editable属性
    # stp1 : 定义一个可编辑的字段元组
    default_list_editable = (
        'first_interviewer_user', 'second_interviewer_user',
    )

    # stp2 : 完成获取该院组的方法
    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'HR' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return self.default_list_editable
        return ()

    # stp3 : 由于django的父类中并没有list_editable获取值的相关方法，所以要重写父类方法
    # 覆盖掉父类中list_editable的获取，使他从我们的函数 get_list_editable中获取
    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    # 定义分组列表 一个列表，每一个元素是个二元组，第一个字段展示的是分组名字，第二个字段是一个map，定义了有哪些字段
    fieldsets = (
        # 在元组内重复通过括号，括号内的内容分为一组，合并显示
        (None, {'fields': ("userid", ("username", "city", "phone"), ("email", "apply_position", "born_address"),
                           ("gender", "candidate_remark"), ("bachelor_school", "master_school", "doctor_school"),
                           ("major", "degree"), ("test_score_of_general_ability", "paper_score"), "last_editor",)}),
        ('第一轮面试记录', {'fields': ("first_score", ("first_learning_ability", "first_professional_competency"),
                                "first_advantage", "first_disadvantage", "first_result", "first_recommend_position",
                                "first_interviewer_user", "first_remark",)}),
        ('第二轮面试记录', {'fields': ("second_score", ("second_learning_ability", "second_professional_competency"),
                                (
                                    "second_pursue_of_excellence", "second_communication_ability",
                                    "second_pressure_score"),
                                "second_advantage", "second_disadvantage", "second_result", "second_recommend_position",
                                "second_interviewer_user", "second_remark",)}),
        ('第三轮面试记录', {'fields': (("hr_score", "hr_responsibility", "hr_communication_ability"), ("hr_logic_ability",
                                                                                                "hr_potential",
                                                                                                "hr_stability"),
                                "hr_advantage", "hr_disadvantage", "hr_result",
                                "hr_interviewer_user", "hr_remark",)})
    )


admin.site.register(Candidate, CandidateAdmin)
