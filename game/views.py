from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import *
from django.db.models import Q, F
import datetime
from decimal import *


teams_dict = \
        {'Grizzlies': 'Grizzlies.png', 'Mavericks': 'Mavericks.png', 'Pelicans': 'Pelicans.png', 'Spurs': 'Spurs.png',
         'Rockets': 'Rockets.png', 'Warriors': 'Warriors.png', 'Clippers': 'Clippers.png', 'Lakers': 'Lakers.png',
         'Kings': 'Kings.png', 'Suns': 'Suns.png', 'Nuggets': 'Nuggets.png', 'Thunder': 'Thunder.png',
         'Blazers': 'Blazers.png', 'Jazz': 'Jazz.png', 'Timberwolves': 'Timberwolves.png', 'Raptors': 'Raptors.png',
         '76ers': '76ers.png', 'Celtics': 'Celtics.png', 'Nets': 'Nets.png', 'Knicks': 'Knicks.png',
         'Hornets': 'Hornets.png', 'Magic': 'Magic.png', 'Heat': 'Heat.png', 'Wizards': 'Wizards.png',
         'Hawks': 'Hawks.png',
         'Bucks': 'Bucks.png', 'Pacers': 'Pacers.png', 'Pistons': 'Pistons.png', 'Cavaliers': 'Cavaliers.png',
         'Bulls': 'Bulls.png'}


# Create your views here.
class HomeView(generic.ListView):
    template_name = 'game/home.html'
    context_object_name = 'teams'

    def get_queryset(self):
        return teams_dict


def home(request):
    today = datetime.date.today()
    days = datetime.timedelta(days=12)
    today = today - days
    games = Game.objects.filter(date=today)
    return render(request, 'game/home.html', {'teams': teams_dict, 'games': games})


def login(request):
    if request.session.get('is_login', None):
        return HttpResponseRedirect("/game/home")
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get('usr_name', None)
        password = request.POST.get('pwd', None)
        message = "所有字段都必须填写！"
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            print(username)
            print(password)
            try:
                user = User.objects.get(usr_name=username)
                if user.password == password:
                    print(request.session)
                    request.session['is_login'] = True
                    request.session['user_name'] = user.usr_name
                    request.session['email'] = user.email
                    request.session['homeTeam'] = user.homeTeam
                    request.session['coins'] = user.coins
                    request.session['img'] = user.imgName
                    return HttpResponseRedirect('/game/home')
                    # return HttpResponseRedirect('home')
                else:
                    message = "密码不正确！"
            except Exception:
                print(Exception)
                message = "用户名不存在！"
        return render(request, 'game/login.html', {"message": message})
    return render(request, 'game/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/game/home")
    request.session.flush()
    return HttpResponseRedirect("/game/home")


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return HttpResponseRedirect("/game/home")
    else:
        post = request.POST
        if (request.POST):
            user = User()
            user.usr_name = post['usr_name']
            user.password = post['pwd1']
            user.email = post['email']
            user.save()
            return render(request, 'game/register_jump.html')
        return render(request, 'game/register.html')


def changePassword(request):
    success = False
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/game/home")
    if request.method == "POST":
        username = request.POST['usr_name']
        newpwd1 = request.POST['newpwd1']
        newpwd2 = request.POST['newpwd2']
        oldpwd = request.POST['oldpwd']
        if oldpwd and newpwd1 and newpwd2 and username:
            try:
                user = User.objects.get(usr_name=username)
                if newpwd2 != newpwd1:
                    message = '两个新密码不一致'
                    render(request, 'game/changepwd.html', locals())
                if user.password == oldpwd:
                    user.password = newpwd1
                    user.save()
                    success = True
                    render(request, 'game/changepwd.html', locals())
                else:
                    message = "旧密码错误"
                    render(request, 'game/changepwd.html', locals())
            except:
                message = "用户名不存在"
                render(request, 'game/changepwd.html', locals())
    return render(request, 'game/changepwd.html', locals())


def check_user_name(request, username):
    counter = User.objects.filter(usr_name=username).count()
    if counter == 0:
        return HttpResponse("true")
    else:
        return HttpResponse("false")


def charge(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/game/home")
    if request.method == "POST":
        print(request.POST)
        username = request.session['user_name']
        email = request.POST['email']
        amount = request.POST['amount']
        if username and amount:  # 确保用户名和密码都不为空
            username = username.strip()
            print(username)
            try:
                user = User.objects.get(usr_name=username)
                print(request.session)
                user.coins += int(amount)
                request.session['coins'] = user.coins
                user.save()
                return HttpResponseRedirect('/game/home/')
                # return HttpResponseRedirect('home')
            except:
                message = "用户名不存在！"
        return render(request, 'game/charge.html', {"message": message})
    return render(request, 'game/charge.html')


def schedule(request):
    games = Game.objects.all().order_by('-date')
    t = datetime.datetime.today()
    return render(request, 'game/schedule.html', locals())

def teams(request):
    def cmpfun(a, b):
        if a[3] > b[3]:
            return 1
        elif a[3] < b[3]:
            return -1
        elif a[1] > b[1]:
            return 1
        elif a[1] < b[1]:
            return -1
        else:
            return 0
    east_team_list = []
    west_team_list = []
    teams = Team.objects.all()
    for i in teams:
        wins = 0
        gameset = Game.objects.filter(Q(home_team=i) | Q(visit_team=i))
        n = gameset.count()
        for g in gameset:
            if g.home_team.team_name == i.team_name:
                if g.home_team_point > g.visit_team_point:
                    wins += 1
            else:
                if g.home_team_point < g.visit_team_point:
                    wins += 1
        if n == 0:
            rate = 0
        else:
            rate = round(wins/n, 4)
        # item = {'team': i, 'wins':wins, 'loses':n-wins, 'rate':rate}
        item = [i, wins, n-wins, rate]
        if i.west_east:
            west_team_list.append(item)
        else:
            east_team_list.append(item)
    east_team_list.sort(key=lambda x: (-x[3], -x[1], x[2]))
    west_team_list.sort(key=lambda x: (-x[3], -x[1], x[2]))
    for item in east_team_list:
        item[3] = str(item[3]*100) + "%"
    for item in west_team_list:
        item[3] = str(item[3]*100) + "%"
    east_teams = [x[0] for x in east_team_list]
    west_teams = [x[0] for x in west_team_list]
    return render(request, 'game/teams.html', locals())


def player(request, player_name):
    try:
        player = Player.objects.get(player_name=player_name)

        # 今天日期
        today = datetime.date.today()

        # 该球员最近四场比赛数据
        latest_games = Player_Game_Data.objects.filter(player=player_name).order_by('-game__date')[:4]

        all_points = []
        for item in latest_games:
            temp = 0
            temp += item.two_point * 2
            temp += item.three_point * 3
            temp += item.free_throw * 1
            all_points.append(temp)

        # 生涯计算
        all_games = Player_Game_Data.objects.filter(player=player_name)

        # 一共打了哪些赛季
        all_season = set()
        for item in all_games:
            game = item.game.season
            all_season.add(game)

        life_data = {}
        #
        for season in all_season:
            season_games = Player_Game_Data.objects.filter(Q(player=player_name) & Q(game__season=season))
            game_number = 0
            start_number = 0
            time_all = 0
            point_all = 0
            two_point_in_all = 0
            two_point_all = 0
            three_point_in_all = 0
            three_point_all = 0
            free_throw_in_all = 0
            free_throw_all = 0

            for item in season_games:
                game_number += 1
                if (item.is_start):
                    start_number += 1
                time_all += item.times
                point_all += item.two_point * 2 + item.three_point * 3 + item.free_throw * 1
                two_point_in_all += item.two_point
                two_point_all += item.two_point_all
                three_point_in_all += item.three_point
                three_point_all += item.three_point_all
                free_throw_in_all += item.free_throw
                free_throw_all += item.free_throw_all

            if game_number != 0:
                time_all = round(time_all / game_number, 2)
                point_all = round(point_all / game_number, 2)
                two_point_in_all = round(two_point_in_all / game_number, 2)
                two_point_all = round(two_point_all / game_number, 2)
                three_point_in_all = round(three_point_in_all / game_number, 2)
                three_point_all = round(three_point_all / game_number, 2)
                free_throw_in_all = round(free_throw_in_all / game_number, 2)
                free_throw_all = round(free_throw_all / game_number, 2)

            if two_point_all == 0:
                average_two_point_percentage = 0
            else:
                average_two_point_percentage = round(two_point_in_all / two_point_all * 100, 2)
            if three_point_all == 0:
                average_three_point_percentage = 0
            else:
                average_three_point_percentage = round(three_point_in_all / three_point_all * 100, 2)
            if free_throw_all == 0:
                average_free_throw_percentage = 0
            else:
                average_free_throw_percentage = round(free_throw_in_all / free_throw_all * 100, 2)

            life_data[season] = {'game_number': game_number, 'start_number': start_number, 'time_all': time_all,
                                 'point_all': point_all, 'two_point_in_all': two_point_in_all,
                                 'two_point_all': two_point_all,
                                 'three_point_in_all': three_point_in_all, 'three_point_all': three_point_all,
                                 'free_throw_in_all': free_throw_in_all, 'free_throw_all': free_throw_all,
                                 'average_two_point_percentage': average_two_point_percentage,
                                 'average_three_point_percentage': average_three_point_percentage,
                                 'average_free_throw_percentage': average_free_throw_percentage}

        return render(request, 'game/player.html', {'today': today, 'player': player, 'latest_games': latest_games,
                                                    'all_games': all_games, 'all_points': all_points,
                                                    'life_data': life_data})

    except Team.DoesNotExist:
        return HttpResponse("Player %s is Not in the Table!" % player_name)


def team(request, team_name):
    try:
        team = Team.objects.get(team_name=team_name)
        players = Player.objects.filter(team=team_name)

        players_list = []
        for item in players:
            players_list.append(item)

        # 今天日期
        today = datetime.date.today()

        # 该队所有比赛和最近四场比赛
        all_games = Game.objects.filter(Q(home_team=team_name) | Q(visit_team=team_name))
        latest_games = Game.objects.filter(Q(home_team=team_name) | Q(visit_team=team_name)).order_by('-date')[:4]

        # 胜负场计算
        win_number = 0
        lose_number = 0
        for item in all_games:
            if (item.home_team.team_name == team_name and item.home_team_point > item.visit_team_point
                    or item.visit_team.team_name == team_name and item.visit_team_point > item.home_team_point):
                win_number += 1
            else:
                lose_number += 1

        return render(request, 'game/team.html', {'players_list': players_list, 'team': team, 'today': today,
                                                  'latest_games': latest_games, 'win_number': win_number,
                                                  'lose_number': lose_number})

    except Team.DoesNotExist:
        return HttpResponse("Team %s is Not in the Table!" % team_name)


def game(request, game_id):
    try:
        # 今天日期
        today = datetime.date.today()

        # 主队和客队
        game = Game.objects.get(game_id=game_id)
        home_team = game.home_team
        visit_team = game.visit_team
        home_team_player_data = Player_Game_Data.objects.filter(Q(player__team=home_team) & Q(game_id=game_id))
        visit_team_player_data = Player_Game_Data.objects.filter(Q(player__team=visit_team) & Q(game_id=game_id))
        home_team_player_point = []

        # 每个队员总分
        for item in home_team_player_data:
            temp_point = item.two_point * 2 + item.three_point * 3 + item.free_throw * 1
            home_team_player_point.append(temp_point)

        visit_team_player_point = []
        for item in visit_team_player_data:
            temp_point = item.two_point * 2 + item.three_point * 3 + item.free_throw * 1
            visit_team_player_point.append(temp_point)

        # 胜负场计算
        home_team_all_games = Game.objects.filter(Q(home_team=home_team) | Q(visit_team=home_team))
        visit_team_all_games = Game.objects.filter(Q(home_team=visit_team) | Q(visit_team=visit_team))

        home_team_win_number = 0
        home_team_lose_number = 0

        visit_team_win_number = 0
        visit_team_lose_number = 0

        for item in home_team_all_games:
            if (item.home_team.team_name == home_team.team_name and item.home_team_point > item.visit_team_point
                    or item.visit_team.team_name == home_team.team_name and item.visit_team_point > item.home_team_point):
                home_team_win_number += 1
            else:
                home_team_lose_number += 1

        for item in visit_team_all_games:
            if (item.home_team.team_name == visit_team.team_name and item.home_team_point > item.visit_team_point
                    or item.visit_team.team_name == visit_team.team_name and item.visit_team_point > item.home_team_point):
                visit_team_win_number += 1
            else:
                visit_team_lose_number += 1

        return render(request, 'game/game.html', {'today': today, 'home_team': home_team, 'visit_team': visit_team,
                                                  'game': game, 'home_team_player_data': home_team_player_data,
                                                  'visit_team_player_data': visit_team_player_data,
                                                  'home_team_player_point': home_team_player_point,
                                                  'visit_team_player_point': visit_team_player_point,
                                                  'home_team_win_number': home_team_win_number,
                                                  'home_team_lose_number': home_team_lose_number,
                                                  'visit_team_win_number': visit_team_win_number,
                                                  'visit_team_lose_number': visit_team_lose_number})

    except Team.DoesNotExist:
        return HttpResponse("game %s is Not in the Table!" % game_id)


def ranking(request):
    today = datetime.date.today()

    # Today Shooter
    top_4_player_today = Player_Game_Data.objects.filter(game__date=today).order_by(-(F('two_point') * 2
                                                                                      + F('three_point') * 3 + F(
                'free_throw')))[:4]

    top_4_player_today_point = []
    top_4_player_today_percentage = []
    for index, item in enumerate(top_4_player_today):
        top_4_player_today_point.append(item.two_point * 2 + item.three_point * 3 + item.free_throw * 1)
        if top_4_player_today_point[0] == 0:
            top_4_player_today_percentage.append(0)
        else:
            top_4_player_today_percentage.append(
                round(top_4_player_today_point[index] / top_4_player_today_point[0] * 100, 2))

    # Today Defender
    top_4_defender_today = Player_Game_Data.objects.filter(game__date=today).order_by('-rebound')[:4]
    top_4_defender_today_percentage = []
    for item in top_4_defender_today:
        if top_4_defender_today[0].rebound == 0:
            top_4_defender_today_percentage.append(0)
        else:
            top_4_defender_today_percentage.append(round(item.rebound / top_4_defender_today[0].rebound * 100, 2))

    # Today Assistant
    top_4_assistant_today = Player_Game_Data.objects.filter(game__date=today).order_by('-assist')[:4]
    top_4_assistant_today_percentage = []
    for item in top_4_assistant_today:
        if top_4_assistant_today[0].assist == 0:
            top_4_assistant_today_percentage.append(0)
        else:
            top_4_assistant_today_percentage.append(round(item.assist / top_4_assistant_today[0].assist * 100, 2))

    # Today Fault
    top_4_fault_today = Player_Game_Data.objects.filter(game__date=today).order_by('-fault')[:4]
    top_4_fault_today_percentage = []
    for item in top_4_fault_today:
        if top_4_fault_today[0].fault == 0:
            top_4_fault_today_percentage.append(0)
        else:
            top_4_fault_today_percentage.append(round(item.fault / top_4_fault_today[0].fault * 100, 2))

    # Season Shooter
    top_4_player_season = Player_Game_Data.objects.filter(game__season=2018).order_by(-(F('two_point') * 2
                                                                                        + F('three_point') * 3 + F(
                'free_throw')))[:4]

    top_4_player_season_point = []
    top_4_player_season_percentage = []
    for index, item in enumerate(top_4_player_season):
        top_4_player_season_point.append(item.two_point * 2 + item.three_point * 3 + item.free_throw * 1)
        if top_4_player_season_point[0] == 0:
            top_4_player_season_percentage.append(0)
        else:
            top_4_player_season_percentage.append(
                round(top_4_player_season_point[index] / top_4_player_season_point[0] * 100, 2))

    # Season Defender
    top_4_defender_season = Player_Game_Data.objects.filter(game__season=2018).order_by('-rebound')[:4]
    top_4_defender_season_percentage = []
    for item in top_4_defender_season:
        if top_4_defender_season[0].rebound == 0:
            top_4_defender_season_percentage.append(0)
        else:
            top_4_defender_season_percentage.append(round(item.rebound / top_4_defender_season[0].rebound * 100, 2))

    # Season Assistant
    top_4_assistant_season = Player_Game_Data.objects.filter(game__season=2018).order_by('-assist')[:4]
    top_4_assistant_season_percentage = []
    for item in top_4_assistant_season:
        if top_4_assistant_season[0].assist == 0:
            top_4_assistant_season_percentage.append(0)
        else:
            top_4_assistant_season_percentage.append(round(item.assist / top_4_assistant_season[0].assist * 100, 2))

    # Season Fault
    top_4_fault_season = Player_Game_Data.objects.filter(game__season=2018).order_by('-fault')[:4]
    top_4_fault_season_percentage = []
    for item in top_4_fault_season:
        if top_4_fault_season[0].fault == 0:
            top_4_fault_season_percentage.append(0)
        else:
            top_4_fault_season_percentage.append(round(item.fault / top_4_fault_season[0].fault * 100, 2))

    # All Player Season Data

    # 生涯计算
    season_all_player_game_data = Player_Game_Data.objects.filter(game__season=today.year)

    # 一共有多少个球员
    all_player = set()
    for item in season_all_player_game_data:
        game = item.player
        all_player.add(game)

    all_player_season_data = {}
    #
    for player in all_player:
        player_game = season_all_player_game_data.filter(Q(player=player))

        game_number = 0
        start_number = 0
        time_all = 0
        point_all = 0
        two_point_in_all = 0
        two_point_all = 0
        three_point_in_all = 0
        three_point_all = 0
        free_throw_in_all = 0
        free_throw_all = 0

        for item in player_game:
            game_number += 1
            if (item.is_start):
                start_number += 1
            time_all += item.times
            point_all += item.two_point * 2 + item.three_point * 3 + item.free_throw * 1
            two_point_in_all += item.two_point
            two_point_all += item.two_point_all
            three_point_in_all += item.three_point
            three_point_all += item.three_point_all
            free_throw_in_all += item.free_throw
            free_throw_all += item.free_throw_all
        try:
            time_all = round(time_all / game_number, 2)
            point_all = round(point_all / game_number, 2)
            two_point_in_all = round(two_point_in_all / game_number, 2)
            two_point_all = round(two_point_all / game_number, 2)
            three_point_in_all = round(three_point_in_all / game_number, 2)
            three_point_all = round(three_point_all / game_number, 2)
            free_throw_in_all = round(free_throw_in_all / game_number, 2)
            free_throw_all = round(free_throw_all / game_number, 2)
        except DivisionByZero:
            pass
        if two_point_all == 0:
            average_two_point_percentage = 0
        else:
            average_two_point_percentage = round(two_point_in_all / two_point_all * 100, 2)
        if three_point_all == 0:
            average_three_point_percentage = 0
        else:
            average_three_point_percentage = round(three_point_in_all / three_point_all * 100, 2)
        if free_throw_all == 0:
            average_free_throw_percentage = 0
        else:
            average_free_throw_percentage = round(free_throw_in_all / free_throw_all * 100, 2)

        all_player_season_data[player] = {'game_number': game_number, 'start_number': start_number,
                                          'time_all': time_all,
                                          'point_all': point_all, 'two_point_in_all': two_point_in_all,
                                          'two_point_all': two_point_all,
                                          'three_point_in_all': three_point_in_all, 'three_point_all': three_point_all,
                                          'free_throw_in_all': free_throw_in_all, 'free_throw_all': free_throw_all,
                                          'average_two_point_percentage': average_two_point_percentage,
                                          'average_three_point_percentage': average_three_point_percentage,
                                          'average_free_throw_percentage': average_free_throw_percentage}

    return render(request, 'game/ranking.html', {'top_4_player_today': top_4_player_today,
                                                 'top_4_player_today_point': top_4_player_today_point,
                                                 'top_4_player_today_percentage': top_4_player_today_percentage,
                                                 'top_4_defender_today': top_4_defender_today,
                                                 'top_4_defender_today_percentage': top_4_defender_today_percentage,
                                                 'top_4_assistant_today': top_4_assistant_today,
                                                 'top_4_assistant_today_percentage': top_4_assistant_today_percentage,
                                                 'top_4_fault_today': top_4_fault_today,
                                                 'top_4_fault_today_percentage': top_4_fault_today_percentage,
                                                 'top_4_player_season': top_4_player_season,
                                                 'top_4_player_season_point': top_4_player_season_point,
                                                 'top_4_player_season_percentage': top_4_player_season_percentage,
                                                 'top_4_defender_season': top_4_defender_season,
                                                 'top_4_defender_season_percentage': top_4_defender_season_percentage,
                                                 'top_4_assistant_season': top_4_assistant_season,
                                                 'top_4_assistant_season_percentage': top_4_assistant_season_percentage,
                                                 'top_4_fault_season': top_4_fault_season,
                                                 'top_4_fault_season_percentage': top_4_fault_season_percentage,
                                                 'all_player_season_data': all_player_season_data})


def update(request):

    return home(request)



