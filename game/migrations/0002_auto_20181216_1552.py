# Generated by Django 2.1.2 on 2018-12-16 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.IntegerField(default=0)),
                ('home_team_point', models.IntegerField(default=0)),
                ('visit_team_point', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Player_Game_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(default='', max_length=20)),
                ('is_start', models.BooleanField(default=False)),
                ('times', models.FloatField()),
                ('two_point', models.IntegerField(default=0)),
                ('two_point_all', models.IntegerField(default=0)),
                ('three_point', models.IntegerField(default=0)),
                ('three_point_all', models.IntegerField(default=0)),
                ('free_throw', models.IntegerField(default=0)),
                ('free_throw_all', models.IntegerField(default=0)),
                ('rebound', models.IntegerField(default=0)),
                ('assist', models.IntegerField(default=0)),
                ('fault', models.IntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('year', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('regular_season_begin', models.DateField()),
                ('playoff_begin', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='player',
            name='player_id',
        ),
        migrations.RemoveField(
            model_name='team',
            name='team_loss',
        ),
        migrations.RemoveField(
            model_name='team',
            name='team_wins',
        ),
        migrations.AddField(
            model_name='player',
            name='pick_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='pick_year',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='player_name',
            field=models.CharField(default='', max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='player',
            name='salary',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='school_name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='game.Team'),
        ),
        migrations.AddField(
            model_name='team',
            name='arena',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='team',
            name='manager',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='img',
            field=models.BooleanField(blank=True, default=0, verbose_name='用户头像'),
        ),
        migrations.AddField(
            model_name='season',
            name='east_champion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_east_champ', to='game.Team'),
        ),
        migrations.AddField(
            model_name='season',
            name='final_champion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_final_champ', to='game.Team'),
        ),
        migrations.AddField(
            model_name='season',
            name='fmvp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_fmvp', to='game.Player'),
        ),
        migrations.AddField(
            model_name='season',
            name='mip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_mip', to='game.Player'),
        ),
        migrations.AddField(
            model_name='season',
            name='mvp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_mvp', to='game.Player'),
        ),
        migrations.AddField(
            model_name='season',
            name='roy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_roy', to='game.Player'),
        ),
        migrations.AddField(
            model_name='season',
            name='smoy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_smoy', to='game.Player'),
        ),
        migrations.AddField(
            model_name='season',
            name='west_champion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_west_champ', to='game.Team'),
        ),
        migrations.AddField(
            model_name='player_game_data',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_home_team', to='game.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Season'),
        ),
        migrations.AddField(
            model_name='game',
            name='visit_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_visit_team', to='game.Team'),
        ),
        migrations.AlterUniqueTogether(
            name='player_game_data',
            unique_together={('player', 'game')},
        ),
    ]
