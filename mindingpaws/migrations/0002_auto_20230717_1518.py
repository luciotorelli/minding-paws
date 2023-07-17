# Generated by Django 3.2.20 on 2023-07-17 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindingpaws', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='minder_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='pet_owner_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='pet_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='pet_species',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('accepted', 'Accepted'), ('pending', 'Pending'), ('declined', 'Declined'), ('completed', 'Completed')], max_length=20),
        ),
        migrations.AlterField(
            model_name='minder',
            name='usual_availability',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='pet_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='pet_species',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('pet-owner', 'Pet Owner'), ('minder', 'Minder'), ('admin', 'Admin')], max_length=9),
        ),
    ]
