# Generated by Django 2.1.2 on 2018-12-16 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20181216_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='player_name',
            field=models.CharField(default='', max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='player',
            name='school_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]