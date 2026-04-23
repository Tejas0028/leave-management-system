from django.contrib import admin
from .models import LeaveRequest
# Register your models here.

class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'status', 'manager', 'created_at')
    list_filter = ('status', 'created_at')

    search_fields = ('employee__email',)
    ordering = ('-created_at',)

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Employee Info', {
            'fields': ('employee', 'manager')
        }),
        ('Leave Details', {
            'fields': ('start_date', 'end_date', 'reason')
        }),
        ('Status Info', {
            'fields': ('status','leave_type')
        }),
        ('Manager Info', {
            'fields': ('manager_remarks',)
        }),
        ('System Info', {
            'fields': ('created_at',)
        }),
    )

admin.site.register(LeaveRequest,LeaveRequestAdmin)