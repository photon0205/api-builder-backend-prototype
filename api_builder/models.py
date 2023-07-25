from django.db import models
from dataset.models import Column, DatasetFile

class API(models.Model):
    dataset_file = models.ForeignKey(DatasetFile, on_delete=models.CASCADE, related_name='apis')
    endpoint = models.CharField(max_length=100)
    selected_columns = models.ManyToManyField(Column)
    access_key = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.endpoint