from django.db import models

# Create your models here.


# class Team(models.Model):
#     # team msg
#     team_name = models.CharField(max_length=64, unique=True, primary_key=True, verbose_name="球队名称", default = '')
#     team_city = models.CharField(max_length=64, verbose_name="球队所在城市", default = '')
#     team_main_coach = models.CharField(max_length=64, verbose_name="主教练姓名", default = '')
#     team_wins = models.IntegerField(default=0, verbose_name="球队胜场数", default = 0)
#     team_loss = models.IntegerField(default=0, verbose_name="球队负场数", default = 0)

#     def __str__(self):
#         return '%s, %s' % (self.team_city, self.team_name)


# class Player(models.Model):
#     # game msg
#     player_id = models.CharField(max_length=10, unique=True, primary_key=True, verbose_name="球员id", default = '')
#     player_Eng_name = models.CharField(max_length=64, blank=False, verbose_name="球员英文姓名", default = '')
#     player_Ch_name  = models.CharField(max_length=128, blank=True, verbose_name="球员中文姓名", default = '')
#     player_birthday = models.DateField(blank=True, verbose_name="球员生日")

#     def __str__(self):
#         return "%4s: %s, %s" % (self.player_id, self.player_Eng_name, self.player_Ch_name)


# Create your models here.

class Team(models.Model):
    
    team_name = models.CharField(primary_key = True, max_length = 20, default = '')
    team_city = models.CharField(max_length = 20, default = '')
    coach = models.CharField(max_length = 20, default = '')
    manager = models.CharField(max_length = 20, default = '')
    arena = models.CharField(max_length = 20, default = '')
    
    def __str__(self):
        return self.team_name

class Player(models.Model):

    player_name = models.CharField(primary_key = True, max_length = 20, default = '')
    #begin_date = models.DateField('date been selected')
    salary = models.IntegerField(default = 0)
    pick_year = models.IntegerField(default = 0)
    school_name = models.CharField(max_length = 20, default = '')
    pick_number = models.IntegerField(default = 0)
    
    team = models.ForeignKey(Team, on_delete = models.CASCADE, default = '')

    def __str__(self):
        return self.player_name

    # def was_published_recently(self):
        # return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)

class Season(models.Model):
    year = models.IntegerField(primary_key = True, default = 0)
    regular_season_begin = models.DateField()
    playoff_begin = models.DateField()

    # roy = models.CharField(max_length = 20, default = '')
    # mip = models.CharField(max_length = 20, default = '')
    # smoy = models.CharField(max_length = 20, default = '')
    # mvp = models.CharField(max_length = 20, default = '')
    # fmvp = models.CharField(max_length = 20, default = '')

    roy = models.ForeignKey('Player', on_delete = models.CASCADE, related_name = 'season_roy')
    mip = models.ForeignKey('Player', on_delete = models.CASCADE, related_name = 'season_mip')
    smoy = models.ForeignKey('Player', on_delete = models.CASCADE, related_name = 'season_smoy')
    mvp = models.ForeignKey('Player', on_delete = models.CASCADE, related_name = 'season_mvp')
    fmvp = models.ForeignKey('Player', on_delete = models.CASCADE, related_name = 'season_fmvp')


    east_champion = models.ForeignKey('Team', on_delete = models.CASCADE, related_name = 'season_east_champ') #有问题
    west_champion = models.ForeignKey('Team', on_delete = models.CASCADE, related_name = 'season_west_champ')
    final_champion = models.ForeignKey('Team', on_delete = models.CASCADE, related_name = 'season_final_champ')
    # east_champion = models.CharField(max_length = 20, default = '')
    # west_champion = models.CharField(max_length = 20, default = '')
    # final_champion = models.CharField(max_length = 20, default = '')

    def __str__(self):
        return str(self.year)

# class Honor(models.Model):
    # year = models.ForeignKey(Season, on_delete = models.CASCADE)

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

class Game(models.Model):
    game_id = models.AutoField(primary_key = True)
    date = models.DateField()
    season = models.ForeignKey('Season', on_delete = models.CASCADE)
    time = models.IntegerField(default = 0)
    home_team = models.ForeignKey('Team', on_delete = models.CASCADE, related_name = 'game_home_team') 
    visit_team = models.ForeignKey('Team', on_delete = models.CASCADE, related_name = 'game_visit_team')

    home_team_point = models.IntegerField(default = 0)
    visit_team_point = models.IntegerField(default = 0)

class User(models.Model):
    user_id = models.CharField(primary_key = True, max_length = 20, default = '')
    password = models.CharField(max_length = 20, default = '')
    money = models.IntegerField(default = 0)

class User_Favorite_Team(models.Model):
    user = models.ForeignKey('User', on_delete = models.CASCADE)
    team = models.ForeignKey('Team', on_delete = models.CASCADE)
    class Meta:
        unique_together = ('user', 'team')

class User_Game_Gamble(models.Model):
    game = models.ForeignKey('Game', on_delete = models.CASCADE)
    user = models.ForeignKey('User', on_delete = models.CASCADE)
    money = models.IntegerField(default = 0)

    class Meta:
        unique_together = ('game', 'user')
    # home_team_odds = models.FloatField()
    # visit_team_odds = models.FloatField()
    # attend_number = models.IntegerField(, default = 0)

