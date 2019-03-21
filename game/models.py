from django.db import models

# Create your models here.


class Team(models.Model):
    # team msg
    team_name = models.CharField(max_length=64, unique=True, primary_key=True, verbose_name="球队名称")
    team_city = models.CharField(max_length=64, verbose_name="球队所在城市")
    team_main_coach = models.CharField(max_length=64, verbose_name="主教练姓名")
    manager = models.CharField(max_length=20, default='经理')
    arena = models.CharField(max_length=20, default='球馆')
    imgPath = models.CharField(max_length=200, default='', blank=True, verbose_name='球队图标路径')
    # west: true, east: false
    west_east = models.BooleanField(default=True, blank=True, verbose_name="东西部")

    def __str__(self):
        return '%s, %s' % (self.team_city, self.team_name)


class Game(models.Model):
    game_id = models.AutoField(primary_key = True)
    date = models.DateField()
    season = models.ForeignKey('Season', on_delete = models.CASCADE)
    time = models.IntegerField(default = 0)
    home_team = models.ForeignKey('Team', on_delete = models.CASCADE, related_name = 'game_home_team')
    visit_team = models.ForeignKey('Team', on_delete = models.CASCADE, related_name = 'game_visit_team')

    home_team_point = models.IntegerField(default = 0)
    visit_team_point = models.IntegerField(default = 0)

    def __str__(self):
        return self.date.strftime("MMMM dd, yyyy") + ": " + self.visit_team.team_name + " vs " + self.home_team.team_name


class Player(models.Model):
    # game msg
    player_birthday = models.DateField(blank=True, verbose_name="球员生日")

    player_name = models.CharField(primary_key=True, max_length=100, default='')
    # begin_date = models.DateField('date been selected')
    salary = models.IntegerField(default=0)
    pick_year = models.IntegerField(default=0)
    school_name = models.CharField(max_length=100, default='')
    pick_number = models.IntegerField(default=0)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.player_name


class Player_Game_Data(models.Model):
    player = models.ForeignKey('Player', on_delete = models.CASCADE)
    game = models.ForeignKey('Game', on_delete = models.CASCADE)

    position = models.CharField(max_length = 20, default = '')
    is_start = models.BooleanField(default = False)
    times = models.FloatField()
    # goal = models.FloatField()
    # goal_percentage = models.FloatField()
    two_point = models.IntegerField(default = 0)
    two_point_all = models.IntegerField(default = 0)
    three_point = models.IntegerField(default = 0)
    three_point_all = models.IntegerField(default = 0)
    free_throw = models.IntegerField(default = 0)
    free_throw_all = models.IntegerField(default = 0)
    rebound = models.IntegerField(default = 0)
    assist = models.IntegerField(default = 0)
    fault = models.IntegerField(default = 0)

    class Meta:
        unique_together = ("player", "game")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        total_points = self.two_point * 2 + self.three_point * 3 + self.free_throw
        if self.player.team.team_name == self.game.home_team.team_name:
            self.game.home_team_point += total_points
        else:
            self.game.visit_team_point += total_points
        super().save()
        self.game.save()

    def __str__(self):
        return  str(self.game.date.month) + "-" + str(self.game.date.day) + " "+ \
                self.game.visit_team.team_name + "vs" + \
                self.game.home_team.team_name + ":  " + \
                self.player.player_name


class Season(models.Model):
    year = models.IntegerField(primary_key = True, default = 0)
    regular_season_begin = models.DateField()
    playoff_begin = models.DateField()

    roy = models.ForeignKey('Player', on_delete = models.CASCADE, blank=True, related_name = 'season_roy')
    mip = models.ForeignKey('Player', on_delete = models.CASCADE, blank=True, related_name = 'season_mip')
    smoy = models.ForeignKey('Player', on_delete = models.CASCADE, blank=True, related_name = 'season_smoy')
    mvp = models.ForeignKey('Player', on_delete = models.CASCADE, blank=True, related_name = 'season_mvp')
    fmvp = models.ForeignKey('Player', on_delete = models.CASCADE, blank=True, related_name = 'season_fmvp')

    east_champion = models.ForeignKey('Team', on_delete = models.CASCADE, related_name = 'season_east_champ') #有问题
    west_champion = models.ForeignKey('Team', on_delete = models.CASCADE, related_name = 'season_west_champ')
    final_champion = models.ForeignKey('Team', on_delete = models.CASCADE, related_name = 'season_final_champ')
    # east_champion = models.CharField(max_length = 20, default = '')
    # west_champion = models.CharField(max_length = 20, default = '')
    # final_champion = models.CharField(max_length = 20, default = '')

    def __str__(self):
        return str(self.year)


class User(models.Model):
    usr_name = models.CharField(max_length=20, unique=True, primary_key=True, verbose_name="用户名")
    password = models.CharField(max_length=100, verbose_name="密码")
    email = models.CharField(max_length=100, verbose_name="邮箱")
    homeTeam = models.CharField(default="", blank=True, max_length=20, verbose_name="最爱球队")
    coins = models.IntegerField(default=0, blank=True, verbose_name="金币余额")
    img = models.BooleanField(default=0, blank=True, verbose_name="用户头像")

    def __str__(self):
        return self.usr_name

