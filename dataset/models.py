from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DatasetFile(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='datasets/')
    name = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dataset.name} - {self.file.name}"

class Column(models.Model):
    dataset_file = models.ForeignKey(DatasetFile, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
