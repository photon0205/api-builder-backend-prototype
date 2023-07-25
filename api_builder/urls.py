from django.urls import path
from .views import APIViewWithData, CreateAPIView, ListAPIs

urlpatterns = [
    path('create/', CreateAPIView.as_view(), name='create_api'),
    path('all/', ListAPIs.as_view(), name='list_apis'),
    path('data/<str:endpoint_name>/', APIViewWithData.as_view(), name='api-with-data'),
]
