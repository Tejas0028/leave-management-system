from rest_framework import serializers
from leaves.models import LeaveRequest
from datetime import date


class LeaveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ["leave_type", "start_date", "end_date", "reason"]

    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Start date cannot be in the past")
        return value

    def validate(self, data):
        if data["end_date"] < data["start_date"]:
            raise serializers.ValidationError("End date cannot be before start date")
        return data


class LeaveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ["id", "leave_type", "start_date", "end_date", "status", "manager_remarks"]


class ManagerLeaveSerializer(serializers.ModelSerializer):
    leave_type = serializers.CharField(source = "get_leave_type_display")
    status = serializers.CharField(source="get_status_display")
    employee_email = serializers.CharField(source="employee.email")

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "employee_email",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "status",
            "manager_remarks",
            "created_at"
        ]