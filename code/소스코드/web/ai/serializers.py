from rest_framework.serializers import RelatedField, ModelSerializer, CharField, ReadOnlyField
from accounts.models import *


class AIrateSerializer(ModelSerializer):
    class Meta:
        model = Airate
        fields = ['date_time','synthesis_rate']