from rest_framework.views import APIView
from rest_framework.response import Response
from api_builder.authentication import APIKeyAuthentication
from api_builder.serializers import APISerializer
from dataset.models import Dataset, DatasetFile, Column
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import API
import uuid
import pandas as pd

def generate_api_key():
    return str(uuid.uuid4())

class APIViewWithData(APIView):
    authentication_classes = [APIKeyAuthentication]

    def get(self, request, endpoint_name):
        api_key = request.headers.get('Authorization', '').split()[-1]
        try:
            api = API.objects.get(access_key=api_key, endpoint=f'/{endpoint_name}')
        except API.DoesNotExist:
            return Response({'error': 'API endpoint not found or unauthorized.'}, status=404)

        dataset_file = api.dataset_file
        selected_columns = api.selected_columns.all()

        data = []
        try:
            df = pd.read_csv(dataset_file.file) # type: ignore
            for column in selected_columns:
                column_data = df[column.name].tolist()
                data.append({
                    'column_name': column.name,
                    'data': column_data,
                })
        except Exception as e:
            return Response({'error': f'Error while reading data: {str(e)}'}, status=500)

        return Response(data, status=200)

class CreateAPIView(APIView):
    def post(self, request):
        print(request.data)
        selected_columns_ids = request.data.get('selected_columns', [])
        endpoint_name = request.data.get('endpoint_name')
        file_id = request.data.get('file_id')
        selected_columns = Column.objects.filter(id__in=selected_columns_ids)
        if not selected_columns.exists():
            return Response({'error': 'Invalid selected_columns IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)

        dataset_files_with_selected_columns = DatasetFile.objects.get(id=file_id)
        api = API.objects.create(
            dataset_file=dataset_files_with_selected_columns,
            endpoint=f'/{endpoint_name}',
            access_key=generate_api_key()
        )
        api.selected_columns.set(selected_columns)
        serializer = APISerializer(api)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

class ListAPIs(APIView):
    def get(self, request):
        apis = API.objects.all()
        serializer = APISerializer(apis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
