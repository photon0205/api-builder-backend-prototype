# Generated by Django 4.2.3 on 2023-07-25 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0004_remove_datasetfile_columns_column'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasetfile',
            name='name',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
    ]
