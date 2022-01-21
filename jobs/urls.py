from django.conf.urls import url
from jobs import views

urlpatterns = [
    url(r"^joblist/", views.joblist, name="joblist"),

    # 传递参数 job_id
    url(r"^job/(?P<job_id>\d+)/$", views.detail, name="detail"),
]