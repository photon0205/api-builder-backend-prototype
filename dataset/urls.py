from django.urls import path
from .views import UploadDataset, UploadDatasetFiles, ListAllDatasets, ListFilesInDataset

urlpatterns = [
    path('upload/', UploadDataset.as_view(), name='upload_dataset'),
    path('files/<int:dataset_id>/', UploadDatasetFiles.as_view(), name='upload_dataset_files'),
    path('all/', ListAllDatasets.as_view(), name='list_all_datasets'),
    path('all-files/<int:dataset_id>/', ListFilesInDataset.as_view(), name='list_files_in_dataset'),
]
