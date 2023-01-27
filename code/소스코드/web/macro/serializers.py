from rest_framework.serializers import RelatedField, ModelSerializer, CharField, ReadOnlyField
from accounts.models import *


class MacroSerializer(ModelSerializer):
    class Meta:
        model = Macroeconomicindicators
        fields = '__all__'