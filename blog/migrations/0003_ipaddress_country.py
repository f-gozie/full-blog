# Generated by Django 3.2.4 on 2021-07-05 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_ipaddress_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipaddress',
            name='country',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
