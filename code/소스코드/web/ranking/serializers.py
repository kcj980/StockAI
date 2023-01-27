from rest_framework.serializers import RelatedField, ModelSerializer, CharField, ReadOnlyField
from accounts.models import *


class UserRankingSerializer(ModelSerializer):
    class Meta:
        model = Userdata
        fields = '__all__'