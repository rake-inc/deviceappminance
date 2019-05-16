from deviceapp.serializer import BaseHyperLinkedSerializer
from .models import Device

class DeviceSerializer(BaseHyperLinkedSerializer):
    class Meta:
        model = Device
