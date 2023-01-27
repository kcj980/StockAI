from rest_framework.serializers import ModelSerializer
from accounts.models import *


class DictSerializer(ModelSerializer):
    class Meta:
        model = Dictionary
        fields = '__all__'