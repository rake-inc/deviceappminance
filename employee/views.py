from django.shortcuts import render
from deviceapp.views import BaseView
from employee.serializer import EmployeeSerializer
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import Employee

# Create your views here.

class EmployeeListView(BaseView):
    
    def get(self, request, *args, **kwargs):
        obj = Employee.objects.all()
        instance = EmployeeSerializer(
                instance=obj,
                context={'request':None},
                read_only=True,
                many=True
            )
        return instance.data

    def post(self, request, *args, **kwargs):
        data = dict(request.data.copy())
        try:
            employee_obj = Employee(**data)
            employee_obj.save()
        except (IntegrityError, ValidationError):
            return status.HTTP_400_BAD_REQUEST
        return status.HTTP_201_CREATED

class EmployeeDetailView(BaseView):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']

        try:
            obj = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        except ValidationError:
            return status.HTTP_417_EXPECTATION_FAILED

        instance = EmployeeSerializer(
                instance=obj, context={'request':None}
            )
        return instance.data

    def patch(self, request, *args, **kwargs):
        pk = kwargs['pk']
        query = request.query_params.dict().copy()

        try:
            obj = Employee.objects.get(pk=pk)
            obj.update(**query)
        except Employee.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        except ValidationError:
            return status.HTTP_417_EXPECTATION_FAILED
        return HTTP_202_ACCEPTED

    def delete(self, request, *args, **kwargs):
        pk = kwargs['pk']

        try:
            obj = Employee.objects.get(pk=pk)
            obj.delete()
        except (IntegrityError, Employee.DoesNotExist):
            return status.HTTP_417_EXPECTATION_FAILED
        return status.HTTP_202_ACCEPTED
