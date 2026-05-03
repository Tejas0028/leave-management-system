from django import forms
from .models import LeaveRequest
from datetime import date

class LeaveForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["leave_type", "start_date", "end_date", "reason"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and start < date.today():
            raise forms.ValidationError("Start date cannot be in past")

        if start and end and end < start:
            raise forms.ValidationError("End date must be after start date")

        return cleaned_data