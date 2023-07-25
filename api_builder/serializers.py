from rest_framework import serializers
from dataset.serializers import ColumnSerializer
from .models import API

class APISerializer(serializers.ModelSerializer):
    selected_columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = API
        fields = ('id', 'dataset_file', 'endpoint', 'selected_columns', 'access_key')
