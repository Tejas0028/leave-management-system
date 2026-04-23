from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)

        user = self.model(
            email = email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        extra_fields['role'] = self.model.Roles.ADMIN

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin): 
    
    class Roles(models.IntegerChoices):
        EMPLOYEE = 1, "Employee"
        MANAGER = 2, "Manager"
        ADMIN = 3, "Admin"
    
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    role = models.PositiveSmallIntegerField(
        choices=Roles.choices,
        default=Roles.EMPLOYEE
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def is_manager(self):
        return self.role == self.Roles.MANAGER
    

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=12, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    profile_picture = models.ImageField(upload_to='profile/', null=True, blank=True)

    def __str__(self):
        return self.user.email
