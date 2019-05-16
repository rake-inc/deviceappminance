from rest_framework import serializers
from urllib.parse import urlparse

class BaseHyperLinkedSerializer(serializers.HyperlinkedModelSerializer):
    url_field_name = 'resource_url'

    @staticmethod
    def construct_url(url):
        return urlparse(url).path

    def to_representation(self, instance):
        ret = super(BaseHyperLinkedSerializer,
                    self).to_representation(instance)
        ret.update({
            self.url_field_name:
            self.construct_url(ret.get(self.url_field_name))
        })
        if hasattr(self, 'foreign_key_fields'):
            for foreign_key_field in self.foreign_key_fields:
                ret.update({
                    foreign_key_field + "_url":
                    self.construct_url(ret.pop(foreign_key_field))
                })
        return ret


class BasePrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        ret = super(BasePrimaryKeyRelatedField, self).to_representation(value)
        if not isinstance(ret, int):
            return str(ret)
        return ret
