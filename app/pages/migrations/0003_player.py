# Generated by Django 5.0.7 on 2025-02-17 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_team_east_team_west_delete_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(choices=[('PG', 'Point Guard'), ('SG', 'Shooting Guard'), ('SF', 'Small Forward'), ('PF', 'Power Forward'), ('C', 'Center')], max_length=2)),
                ('team_east', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.team_east')),
            ],
        ),
    ]
