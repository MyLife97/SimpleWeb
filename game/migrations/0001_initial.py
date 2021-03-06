# Generated by Django 2.1.2 on 2018-12-15 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='球员id')),
                ('player_Eng_name', models.CharField(max_length=64, verbose_name='球员英文姓名')),
                ('player_Ch_name', models.CharField(blank=True, max_length=128, verbose_name='球员中文姓名')),
                ('player_birthday', models.DateField(blank=True, verbose_name='球员生日')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_name', models.CharField(max_length=64, primary_key=True, serialize=False, unique=True, verbose_name='球队名称')),
                ('team_city', models.CharField(max_length=64, verbose_name='球队所在城市')),
                ('team_main_coach', models.CharField(max_length=64, verbose_name='主教练姓名')),
                ('team_wins', models.IntegerField(default=0, verbose_name='球队胜场数')),
                ('team_loss', models.IntegerField(default=0, verbose_name='球队负场数')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('usr_name', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('email', models.CharField(max_length=100, verbose_name='邮箱')),
                ('homeTeam', models.CharField(blank=True, default='', max_length=20, verbose_name='最爱球队')),
                ('coins', models.IntegerField(blank=True, default=0, verbose_name='金币余额')),
                ('img', models.BooleanField(blank=True, default='0', verbose_name='用户头像')),
            ],
        ),
    ]
