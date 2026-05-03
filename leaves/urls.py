from django.urls import path
from . import views


urlpatterns = [
    path("apply/", views.apply_leave, name="apply_leave"),
    path("my/", views.my_leaves, name="my_leaves"),
    path("manage/", views.manage_leaves, name="manage_leaves"),
    path("action/<int:pk>/", views.update_leave_status, name="update_leave_status"),
]