# Generated by Django 3.1.7 on 2021-03-17 09:36

from django.db import migrations, models
import tracker.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_auto_20210316_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, validators=[tracker.validators.SpecialSymbolsValidator(['@', '#', '$', '&'])]),
        ),
    ]