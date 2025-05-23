# Generated by Django 4.2 on 2025-05-04 14:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anemometer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('tags', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WindSpeedReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speed_knots', models.FloatField()),
                ('recorded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('anemometer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='api.anemometer')),
            ],
            options={
                'ordering': ['-recorded_at'],
            },
        ),
    ]
