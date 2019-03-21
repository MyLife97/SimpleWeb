from django.conf.urls import url
from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path('', views.home, name='nbaHome'),
    path('home/', views.home, name='nbaHome'),
    path('schedule', views.schedule, name='schedule'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('charge', views.charge),
    path('register/checkname/<str:username>', views.check_user_name, name='register_check_user_name'),
    path('register/checkname/<str:username>', views.check_user_name, name="register_checkname"),
    path('changePassword', views.changePassword, name='change_password'),

    path('teams', views.teams, name='teams_ranking'),
    path('player=<str:player_name>/', views.player, name='player'),
    path('game=<str:game_id>/', views.game, name='game'),
    path('team=<str:team_name>', views.team, name='team'),
    path('ranking', views.ranking, name='ranking'),


    path('update', views.update, name='update'),
    # path('players=<str:players_name>/', views.players, name='search_players'),
    # url(r'^$', views.HomeView.as_view(), name='nbaHome'),
    # url(r'^players$', views.players, name='players'),
    # url(r'^team$', views.team, name='team'),
    # url(r'^schedule$', views.schedule, name='schedule'),
    # url(r'^login$', views.login, name='login'),
    # url(r'^register$', views.register, name='register'),
    # url(r'^register/checkname/(?P<username>\w{1-20})$', views.check_user_name, name='register_user_name_check'),
    # url(r'^home$', views.HomeView.as_view(), name='nbaHome'),
    # url(r'^register/(?P<username>\w{1,20})/count/$', views.usr_name_count, name='usrnameCount'),
    # url(r'^team/(?P<teamname>[a-zA-Z0-9]+)/$', views.team, name='team'),
]
