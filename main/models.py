from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255)
    seats = models.IntegerField()
    is_projector = models.BooleanField()


class Reservation(models.Model):
    date = models.DateField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField()


class Meta:
    unique_together = ('date', 'room_id')
