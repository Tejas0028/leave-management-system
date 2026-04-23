from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class LeaveRequest(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1, "Pending"
        APPROVED = 2, "Approved"
        REJECTED = 3, "Rejected"

    class LeaveType(models.IntegerChoices):
        CASUAL = 1, "Casual"
        SICK = 2, "Sick"

    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name="leave_requests")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name="managed_leaves")

    start_date = models.DateField()
    end_date = models.DateField()

    reason = models.TextField()

    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.PENDING
    )

    leave_type = models.PositiveSmallIntegerField(
        choices=LeaveType.choices,
        default= LeaveType.CASUAL
    )
    
    manager_remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.email} - {self.get_status_display()}"
    
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date")
        
    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1