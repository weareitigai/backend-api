from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('partner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='status',
            field=models.CharField(
                max_length=20,
                choices=[('in-process', 'In Process'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                default='in-process',
            ),
        ),
    ] 