# Generated by Django 5.1.6 on 2025-02-23 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_alter_player_awards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='ast',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='blk',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='bpm',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='dbpm',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='drb',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='dws',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='ftr',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='g',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='gs',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='mp',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='obpm',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='orb',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='ows',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='par',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='per',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='stl',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='tov',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='trb',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='ts',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='usg',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='vorp',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='ws',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='ws48',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
