# Generated by Django 3.0.3 on 2020-04-07 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0003_auto_20200218_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='description',
            field=models.CharField(max_length=100),
        ),
    ]