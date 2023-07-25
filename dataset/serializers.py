from rest_framework import serializers
from .models import Column, Dataset, DatasetFile

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ('id', 'name')

class DatasetFileSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = DatasetFile
        fields = ('id', 'file', 'uploaded_at', 'columns', 'name')

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'uploaded_at')