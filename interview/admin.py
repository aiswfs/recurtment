import codecs

from django.contrib import admin
from interview.models import Candidate
from datetime import datetime
from django.http import HttpResponse
import csv

# Register your models here.

exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'degree', 'first_score', 'first_result',
                     'first_interviewer', 'second_result', 'second_interviewer', 'hr_score', 'hr_result',
                     'hr_interviewer')


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
        'username', 'city', 'bachelor_school', 'first_score', 'first_result', 'first_interviewer',
        'second_result', 'second_interviewer', 'hr_score', 'hr_result', 'last_editor'
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
        'city', 'first_result', 'second_result', 'hr_result', 'first_interviewer', 'second_interviewer',
        'hr_interviewer'
    )

    ordering = (
        'hr_result', 'second_result', 'first_result',
    )

    # 定义分组列表 一个列表，每一个元素是个二元组，第一个字段展示的是分组名字，第二个字段是一个map，定义了有哪些字段
    fieldsets = (
        # 在元组内重复通过括号，括号内的内容分为一组，合并显示
        (None, {'fields': ("userid", ("username", "city", "phone"), ("email", "apply_position", "born_address"),
                           ("gender", "candidate_remark"), ("bachelor_school", "master_school", "doctor_school"),
                           ("major", "degree"), ("test_score_of_general_ability", "paper_score"), "last_editor",)}),
        ('第一轮面试记录', {'fields': (("first_score", "first_learning_ability", "first_professional_competency"),
                                "first_advantage", "first_disadvantage", "first_result", "first_recommend_position",
                                "first_interviewer", "first_remark",)}),
        ('第二轮面试记录', {'fields': (("second_score", "second_learning_ability", "second_professional_competency"),
                                (
                                    "second_pursue_of_excellence", "second_communication_ability",
                                    "second_pressure_score"),
                                "second_advantage", "second_disadvantage", "second_result", "second_recommend_position",
                                "second_interviewer", "second_remark",)}),
        ('第三轮面试记录', {'fields': (("hr_score", "hr_responsibility", "hr_communication_ability"), ("hr_logic_ability",
                                                                                                "hr_potential",
                                                                                                "hr_stability"),
                                "hr_advantage", "hr_disadvantage", "hr_result",
                                "hr_interview", "hr_remark",)})
    )


admin.site.register(Candidate, CandidateAdmin)
