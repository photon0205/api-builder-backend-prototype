# Generated by Django 4.2.3 on 2023-07-21 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0004_remove_datasetfile_columns_column'),
        ('api_builder', '0003_api_dataset_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='api',
            name='selected_columns',
        ),
        migrations.AddField(
            model_name='api',
            name='selected_columns',
            field=models.ManyToManyField(to='dataset.column'),
        ),
    ]
