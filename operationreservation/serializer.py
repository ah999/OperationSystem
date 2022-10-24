from rest_framework import serializers
from .models import Operation,OpRoom,Department

class OperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operation
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class OpRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpRoom
        fields = '__all__'
