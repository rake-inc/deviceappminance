from deviceapp.serializer import BaseHyperLinkedSerializer
from .models import Employee

class EmployeeSerializer(BaseHyperLinkedSerializer):
    class Meta:
        model = Employee
