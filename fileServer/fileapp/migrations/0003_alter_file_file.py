# Generated by Django 4.2.1 on 2023-05-15 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileapp', '0002_file_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files'),
        ),
    ]