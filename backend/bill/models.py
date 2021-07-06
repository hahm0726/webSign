from django.db import models

# Create your models here.
class Bill(models.Model):
    idx = models.IntegerField(verbose_name="연번",unique=True) #연번
    name= models.CharField(verbose_name="이름",max_length=20, null=True) #이름
    birthDate = models.CharField(verbose_name="생년월일",max_length=10, null=True, blank=True) #생년월일(YYYY-MM-DD)
    location = models.CharField(verbose_name="거주동",max_length=20, null=True, blank=True) #거주동
    amount = models.IntegerField(verbose_name="수량",default=0, blank=True, null=True) #수량
    receivedDate = models.CharField(verbose_name="수령일",max_length=10, null=True, blank=True) #수령일(YYYY-MM-DD)
    signature = models.TextField(verbose_name="서명",null=True, blank=True) #서명
    created = models.DateTimeField(verbose_name="생성일", auto_now_add=True)#생성일
    updated = models.DateTimeField(verbose_name="수정일", auto_now=True)#수정일

    class Meta:
        verbose_name = '인수증'
        verbose_name_plural = '인수증'
        ordering = ['idx', ]