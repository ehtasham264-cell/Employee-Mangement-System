from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)

    def __str__(self):         
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):          
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, default='')  # Fix: was IntegerField
    hire_date = models.DateField()
    bonus = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"