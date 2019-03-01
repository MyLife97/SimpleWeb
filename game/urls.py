from django.conf.urls import url
from . import views
from django.urls import path

app_name = "game"

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='nbaHome'),
    url(r'^players$', views.players, name='players'),
    url(r'^team$', views.team, name='team'),
    url(r'^team/(?P<teamname>[a-zA-Z0-9]+)/$', views.team, name='team'),
    url(r'^schedule$', views.schedule, name='schedule'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),

    path('team=<str:team_name>/', views.search_team, name = 'search_team'),
    path('players=<str:players_name>/', views.search_players, name = 'search_players'),
    path('game=<str:game_id>/', views.search_game, name = 'search_game'),
    path('ranking', views.ranking, name = 'ranking')
]
