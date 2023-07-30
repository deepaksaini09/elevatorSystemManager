from rest_framework import serializers
from .models import Elevator, FloorRequest

# elevator_system/models.py
from django.db import models


# convert complex python data  to json data
# and also convert json data to python data
class elevatorSerializers(serializers.Serializer):
    lift_number = serializers.IntegerField()
    is_operational = serializers.BooleanField()
    is_maintenance = serializers.BooleanField()
    is_available = serializers.BooleanField()
    current_floor = serializers.IntegerField()
    moving_up = serializers.IntegerField()
    is_upward = serializers.IntegerField()


class floorRequestSerializers(serializers.Serializer):
    floor_number = serializers.IntegerField()
    is_door_close_open = serializers.BooleanField()
    archived_at = serializers.DateTimeField()
    lift_id = serializers.IntegerField()


class elevatorAndFloorSerializedData(serializers.Serializer):
    lift_number = serializers.IntegerField()
    is_operational = serializers.BooleanField()
    is_maintenance = serializers.BooleanField(default=False)
    is_available = serializers.BooleanField(default=True)
    current_floor = serializers.IntegerField(default=1)
    moving_up = serializers.IntegerField()
    is_upward = serializers.IntegerField()
    floor_number = serializers.IntegerField()
    is_door_close_open = serializers.BooleanField()
    archived_at = serializers.CharField(default='Not archived')
    lift_id = serializers.IntegerField()


class elevatorMovingUpOrDownSerializers(serializers.Serializer):
    lift_number = serializers.IntegerField()
    moving_up = serializers.IntegerField()


class elevatorDoorStatusSerializers(serializers.Serializer):
    lift_number = serializers.IntegerField()
    is_door_close_open = serializers.BooleanField()


class elevatorIsMaintenanceStatusSerializers(serializers.Serializer):
    lift_number = serializers.IntegerField()
    is_maintenance = serializers.BooleanField()


class saveUserRequestForElevators(serializers.Serializer):
    floor_number = serializers.IntegerField()
    lift_id = serializers.IntegerField()

    def create(self, validated_data):
        return FloorRequest.objects.create(**validated_data)
