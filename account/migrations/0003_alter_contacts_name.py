# Generated by Django 5.1.2 on 2024-12-08 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_contacts_mobile_number_contacts_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='name',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
