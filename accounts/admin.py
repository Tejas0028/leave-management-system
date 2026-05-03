from django.contrib import admin
from .models import User,Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.utils.html import format_html


# Register your models here.

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        Model = User
        fields = '__all__'

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Password does not match")
        return cleaned_data
    
    def save(self, commit = True):
        user =  super().save(commit = False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'role')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        ('Login Info', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'profile_image_preview')
    search_fields = ('user__email',)
    list_filter = ('user',)

    fieldsets = (
        ('User Info', {'fields': ('user',)}),
        ('Personal Info', {'fields': ('phone_number', 'date_of_birth', 'address')}),
        ('Profile Image', {'fields': ('profile_picture',)}),
    )

    def profile_image_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:50%;" />',
                obj.profile_picture.url
            )
        return "No Image"

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)