# Generated by Django 3.2.20 on 2023-07-18 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindingpaws', '0003_auto_20230718_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='minder_name',
            field=models.CharField(blank=True, help_text='This field will be prepopulated on save based on the minder selected', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='pet_owner_name',
            field=models.CharField(blank=True, help_text='This field will be prepopulated on save based on the pet owner selected', max_length=50, null=True),
        ),
    ]
