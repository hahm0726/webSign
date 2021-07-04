from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        verbose_name="아이디", max_length=150, unique=True)
    name = models.CharField(verbose_name="이름", max_length=50, blank=True, null=True)
    department = models.CharField(verbose_name="부서", max_length=50, blank=True, null=True)
    company = models.CharField(
        verbose_name="회사코드", max_length=4
    )
