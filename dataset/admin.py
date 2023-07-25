from django.contrib import admin
from .models import Dataset, DatasetFile, Column

class ColumnInline(admin.StackedInline):
    model = Column
    extra = 1

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_at']

@admin.register(DatasetFile)
class DatasetFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'dataset', 'uploaded_at']
    list_filter = ['dataset']
    inlines = [ColumnInline]
