from django.contrib import admin
from game.models import Player, Team, Season, Player_Game_Data, Game, User, User_Favorite_Team, User_Game_Gamble

# Register your models here.
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Season)
admin.site.register(Player_Game_Data)
admin.site.register(Game)
admin.site.register(User)
admin.site.register(User_Favorite_Team)
admin.site.register(User_Game_Gamble)