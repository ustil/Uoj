# coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from jsonfield import JSONField

class UserManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    real_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    admin_type = models.IntegerField(default=0)
    reset_password_token = models.CharField(max_length=40, blank=True, null=True)
    reset_password_token_create_time = models.DateTimeField(blank=True, null=True)
    problems_status = JSONField(default={})
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        db_table = "user"

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    rank = models.IntegerField(default=65535)
    accepted_number = models.IntegerField(default=0)
    submissions_number = models.IntegerField(default=0)
    school = models.CharField(max_length=200, blank=True, null=True)
    student_id = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = "user_profile"