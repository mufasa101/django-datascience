# Generated by Django 3.2.9 on 2021-11-11 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_alter_sale_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='created_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
