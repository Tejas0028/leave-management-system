from django.urls import path
from . import views

urlpatterns = [
    #employee
    path("apply/", views.ApplyLeaveApi.as_view(),name="apply-leave"),
    path("my/",views.MyLeaveAPI.as_view(),name="my-leaves"),

    #manager
    path("pending/",views.PendingLeavesAPI.as_view(),name="pending-leaves"),
    path("action/<int:pk>/",views.LeaveActionAPI.as_view(),name="leave-action"),
]