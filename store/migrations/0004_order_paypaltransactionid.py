# Generated by Django 3.1.7 on 2021-04-07 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210329_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paypalTransactionId',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
