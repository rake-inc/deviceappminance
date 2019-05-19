from django.db import models
# from employee.models import Employee
import uuid
from django.core.exceptions import ValidationError
from deviceapp.app import app
from .task import send_mail
# Create your models here.


class Device(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid1)
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE)
    number = models.TextField(null=False, unique=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.employee or not self.number:
            raise ValidationError("Please enter the required fields")
        send_mail.apply_async((self.employee.email, str(self.number)))
        super(Device, self).save(args, kwargs)
