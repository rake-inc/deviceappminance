from django.db import models
from django.core.exceptions import ValidationError
import uuid
from device.models import Device
# Create your models here.


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid1)
    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    email = models.EmailField()
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['first_name', 'email', 'last_name'])]

    def save(self, *args, **kwargs):
        if not self.first_name or not self.last_name or not self.email:
            raise ValidationError("Please enter the required fields")
        super(Employee, self).save(args, kwargs)

    def delete(self, *args, **kwargs):

        device_objects = Device.objects.filter(employee=self)

        for device in device_objects:
            
            device.active = False
            device.save()
            
        super(Employee, self).delete(args, kwargs)
