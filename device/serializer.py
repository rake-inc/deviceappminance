from deviceapp.serializer import BaseHyperLinkedSerializer, BasePrimaryKeyRelatedField
from .models import Device
from employee.serializer import EmployeeSerializer

class DeviceSerializer(BaseHyperLinkedSerializer):
    
    class Meta:
        model = Device
        fields='__all__'