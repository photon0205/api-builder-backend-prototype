from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Column, Dataset, DatasetFile
from .serializers import ColumnSerializer, DatasetFileSerializer, DatasetSerializer
import pandas as pd

class UploadDataset(APIView):
    def post(self, request):
        name = request.data.get('name')
        if name:
            dataset = Dataset.objects.create(name=name)
            return Response({'dataset_id': dataset.id}, status=status.HTTP_201_CREATED) # type: ignore
        return Response({'error': 'Invalid data. "name" field is required.'}, status=status.HTTP_400_BAD_REQUEST)

class UploadDatasetFiles(APIView):
    def post(self, request, dataset_id):
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found.'}, status=status.HTTP_404_NOT_FOUND)

        file = request.FILES.get('file')
        if file:
            if file.size == 0:
                return Response({'error': 'The uploaded file is empty.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                df = pd.read_csv(file)
                column_headings = df.columns.tolist()
            except Exception as e:
                return Response({'error': f'Error while reading the CSV file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

            if len(column_headings) == 0:
                return Response({
                    'error': 'The uploaded CSV file does not contain any column headings.',
                    'file_contents': df.to_dict(orient='records')
                }, status=status.HTTP_400_BAD_REQUEST)

            dataset_file = DatasetFile.objects.create(dataset=dataset, file=file)

            for column_heading in column_headings:
                Column.objects.create(dataset_file=dataset_file, name=column_heading)

            return Response({'message': 'File uploaded successfully.', 'columns': column_headings}, status=status.HTTP_201_CREATED)

        return Response({'error': 'Invalid data. "file" field is required.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, dataset_id):
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found.'}, status=status.HTTP_404_NOT_FOUND)

        files = DatasetFile.objects.filter(dataset=dataset)
        serializer = DatasetFileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListAllDatasets(APIView):
    def get(self, request):
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListFilesInDataset(APIView):
    def get(self, request, dataset_id):
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found.'}, status=status.HTTP_404_NOT_FOUND)

        files = DatasetFile.objects.filter(dataset=dataset)

        files_with_columns = []
        for file in files:
            columns = Column.objects.filter(dataset_file=file)
            column_serializer = ColumnSerializer(columns, many=True)
            file_serializer = DatasetFileSerializer(file)
            data = []
            try:
                df = pd.read_csv(file.file) # type: ignore
                df = df.replace([float('inf'), float('-inf')], 'Infinity')
                df = df.where(pd.notna(df), None)
                for column in columns:
                    column_data = df[column.name].tolist()
                    data.append({
                        'column_name': column.name,
                        'data': column_data,
                    })
            except Exception as e:
                return Response({'error': f'Error while reading data: {str(e)}'}, status=500)
            files_with_columns.append({
                'file': file_serializer.data,
                'columns': column_serializer.data,
                'data': data
            })

        dataset_serializer = DatasetSerializer(dataset)

        return Response({'files': files_with_columns, 'dataset': dataset_serializer.data}, status=status.HTTP_200_OK)
