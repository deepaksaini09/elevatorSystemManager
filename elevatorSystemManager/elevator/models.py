# elevator_system/models.py
from django.db import models


class Elevator(models.Model):
    """ elevator table and its attribute"""
    lift_number = models.AutoField(primary_key=True)
    is_operational = models.BooleanField(default=True)
    is_maintenance = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    current_floor = models.IntegerField(default=0)
    moving_up = models.SmallIntegerField(default=0)
    is_upward = models.SmallIntegerField(default=0)
    requests = models.ManyToManyField('FloorRequest', related_name='elevators')
    is_door_close_open = models.BooleanField(default=0)


class FloorRequest(models.Model):
    """ elevator floor request and elevator id(lift_id)"""
    floor_number = models.IntegerField()
    lift_id = models.IntegerField(null=True)
    archived_at = models.DateTimeField(null=True)


