from django.contrib import admin
from game.models import *

# Register your models here.
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(User)
admin.site.register(Season)
admin.site.register(Game)
admin.site.register(Player_Game_Data)
# admin.site.register(User_Favorite_Team)
# admin.site.register(User_Game_Gamble)