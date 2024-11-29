from django.db import models

# Create your models here.
class Dept(models.Model):
    deptno=models.IntegerField(primary_key=True)
    dname=models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.dname}'

class Employee(models.Model):
    empno=models.IntegerField(primary_key=True)
    ename=models.CharField(max_length=30)
    job=models.CharField(max_length=15)
    sal=models.FloatField()
    dept=models.ForeignKey(Dept,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.ename}'
