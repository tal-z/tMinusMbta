from django.db import models

# Create your models here.
class StoredTimer(models.Model):
    stop_id = models.CharField(max_length=200)
    route_id = models.CharField(max_length=200)
    direction_id = models.CharField(max_length=200)
    timer_id = models.CharField(max_length=200)
    predictions_url = models.CharField(max_length=5000)
    schedule_url = models.CharField(max_length=5000)
    stop_name = models.CharField(max_length=200)
    route_name = models.CharField(max_length=200)
    direction_name = models.CharField(max_length=200)

    def __str__(self):
        return self.timer_id