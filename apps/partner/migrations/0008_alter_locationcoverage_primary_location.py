# Generated manually on 2025-07-25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0007_remove_tour_description_remove_tour_end_date_and_more'),
    ]

    operations = [
        # Remove the old primary_location field
        migrations.RemoveField(
            model_name='locationcoverage',
            name='primary_location',
        ),
        # Add the new city field
        migrations.AddField(
            model_name='locationcoverage',
            name='city',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        # Add the new state field
        migrations.AddField(
            model_name='locationcoverage',
            name='state',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
    ] 