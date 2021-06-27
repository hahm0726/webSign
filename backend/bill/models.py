from django.db import models

# Create your models here.
class Bill(models.Model):
    idx = models.IntegerField(verbose_name="연번",primary_key=True, blank=False) #연번
    name= models.CharField(verbose_name="이름",max_length=20, null=True) #이름
    birthDate = models.CharField(verbose_name="생년월일",max_length=10, null=True, blank=True) #생년월일(YYYY-MM-DD)
    location = models.CharField(verbose_name="거주동",max_length=20, null=True, blank=True) #거주동
    amount = models.IntegerField(verbose_name="수량",default=0, blank=True) #수량
    receiveDate = models.CharField(verbose_name="수령일",max_length=10, null=True, blank=True) #수령일(YYYY-MM-DD)
    state = models.BooleanField(verbose_name="수령상태",default=False, null=True, blank=True) #수령상태(수령:True / 수령전:False)
