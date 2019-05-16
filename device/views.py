from django.shortcuts import render
from deviceapp.views import BaseView
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import Device
from employee.models import Employee
from .serializer import DeviceSerializer

# Create your views here.

class DeviceListView(BaseView):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        
        try:
            emp_obj = Employee.objects.get(pk=emp_pk)
            devices = Device.objects.filter(employee=emp_obj)
        except (IntegrityError, Employee.DoesNotExist):
            return status.HTTP_417_EXPECTATION_FAILED

        instance = DeviceSerializer(
                instance=obj,
                context={'request':None},
                read_only=True,
                many=True
            )
        return instance.data

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        
        try:
            emp_obj = Employee.objects.get(pk=emp_pk)
        except (IntegrityError, Employee.DoesNotExist):
            return status.HTTP_417_EXPECTATION_FAILED

        data = dict(request.data.copy())
        try:
            employee_obj = Device(**data)
            employee_obj.save()
        except (IntegrityError, ValidationError):
            return status.HTTP_400_BAD_REQUEST
        return status.HTTP_201_CREATED

class DeviceDetailView(BaseView):
    def patch(self, *args, **kwargs):
        emp_pk = kwargs['emp_pk']
        device_pk = kwargs['device_pk']
        
        query = request.query_params.dict().copy()

        try:
            emp_obj = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        except ValidationError:
            return status.HTTP_417_EXPECTATION_FAILED

        try:
            device_obj = Device.objects.get(pk=pk)
            if device_obj.employee.pk != employee.pk:
                raise ValidationError("Device does not belong to the employee")
            obj.update(**query)
        except Device.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        except ValidationError:
            return status.HTTP_417_EXPECTATION_FAILED
        return HTTP_202_ACCEPTED



    def delete(self, *args, **kwargs):
        emp_pk = kwargs['emp_pk']
        device_pk = kwargs['device_pk']

        try:
            emp_obj = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        except ValidationError:
            return status.HTTP_417_EXPECTATION_FAILED

        try:
            device_obj = Device.objects.get(pk=pk)
            device_obj.delete()
        except Device.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        except ValidationError:
            return status.HTTP_417_EXPECTATION_FAILED
        return HTTP_202_ACCEPTED
