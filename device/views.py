from django.shortcuts import render
from deviceapp.views import BaseView
from django.core.exceptions import ValidationError
from rest_framework import status
from django.db.utils import IntegrityError
from .models import Device
from employee.models import Employee
from .serializer import DeviceSerializer
from rest_framework.serializers import UUIDField
# Create your views here.

class DeviceListView(BaseView):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        
        try:
            emp_obj = Employee.objects.get(pk=pk)
            devices = Device.objects.filter(employee=emp_obj)
        except (IntegrityError, Employee.DoesNotExist):
            return status.HTTP_417_EXPECTATION_FAILED

        instance = DeviceSerializer(
                instance=devices,
                # lookup_field="employee",
                context={'request':None},
                read_only=True,
                # allow_null=True,
                many=True
            )
        return instance

    def post(self, request, *args, **kwargs):
        emp_pk = kwargs['emp_pk']
        
        try:
            emp_obj = Employee.objects.get(pk=emp_pk)
        except (IntegrityError, Employee.DoesNotExist):
            return status.HTTP_417_EXPECTATION_FAILED

        data = dict(request.data.copy())
        data['employee'] = emp_obj
        try:
            device = Device(**data)
            device.save()
        except (IntegrityError, ValidationError):
            return status.HTTP_400_BAD_REQUEST
        return status.HTTP_201_CREATED

class DeviceDetailView(BaseView):
    def patch(self, *args, **kwargs):
        emp_pk = kwargs['emp_pk']
        device_pk = kwargs['device_pk']
        
        query = request.query_params.dict().copy()

        try:
            emp_obj = Employee.objects.get(pk=emp_pk)
        except Employee.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        except ValidationError:
            return status.HTTP_417_EXPECTATION_FAILED

        try:
            device_obj = Device.objects.get(pk=device_pk)
            if device_obj.employee.pk != emp_obj.pk:
                raise ValidationError("Device does not belong to the employee")
            device_obj.update(**query)
        except Device.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        except ValidationError:
            return status.HTTP_417_EXPECTATION_FAILED
        return HTTP_202_ACCEPTED



    def delete(self, *args, **kwargs):
        emp_pk = kwargs['emp_pk']
        device_pk = kwargs['device_pk']

        try:
            emp_obj = Employee.objects.get(pk=emp_pk)
        except Employee.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        except ValidationError:
            return status.HTTP_417_EXPECTATION_FAILED

        try:
            device_obj = Device.objects.get(pk=device_pk)
            device_obj.delete()
        except Device.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        except ValidationError:
            return status.HTTP_417_EXPECTATION_FAILED
        return HTTP_202_ACCEPTED
