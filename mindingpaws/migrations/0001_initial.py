# Generated by Django 3.2.20 on 2023-07-14 18:18

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('role', models.TextField(choices=[('pet-owner', 'Pet Owner'), ('minder', 'Minder'), ('admin', 'Admin')], max_length=9)),
                ('pet_name', models.TextField(blank=True, max_length=50, null=True)),
                ('pet_species', models.TextField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Minder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('usual_availability', models.TextField()),
                ('photo', cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.TextField()),
                ('service_description', models.TextField()),
                ('pet_name', models.TextField(blank=True)),
                ('pet_species', models.TextField(blank=True)),
                ('minder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mindingpaws.minder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
