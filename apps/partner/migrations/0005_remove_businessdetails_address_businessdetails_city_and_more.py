# Generated by Django 4.2.7 on 2025-07-23 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0004_merge_20250722_0815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessdetails',
            name='address',
        ),
        migrations.AddField(
            model_name='businessdetails',
            name='city',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='businessdetails',
            name='country',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='businessdetails',
            name='state',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
