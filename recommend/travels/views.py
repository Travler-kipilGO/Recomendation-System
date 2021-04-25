from django.shortcuts import render
import requests
import json
from math import sqrt
from . import models
import pandas as pd
# Create your views here.

def home(request):
    return render(request, 'travels/home.html')


def n_map(request):
    areacode      = request.GET.get('loc', False)
    contents_type = request.GET.get('theme', False)
    request.session['areacode']      = areacode
    request.session['contents_type'] = contents_type

    # 맵 중앙 좌표 설정
    if areacode == '1':
        map_center = (37.56099073728087, 126.9888542058965)
    elif areacode == '2':
        map_center = (37.469865204921014, 126.70146425886135)
    elif areacode == '3':
        map_center = (36.34141096399956, 127.39360630587186)
    elif areacode == '4':
        map_center = (35.83394171476235, 128.5658367309032)
    elif areacode == '5':
        map_center = (35.16066738624785, 126.83692058211457)
    elif areacode == '6':
        map_center = (35.17217626215749, 129.04434051065476)
    elif areacode == '7':
        map_center = (35.552624380057935, 129.2615077003808)
    elif areacode == '8':
        map_center = (36.5613704176564, 127.25756722506266)
    elif areacode == '31':
        map_center = (37.2820719546124, 127.00679578588812)
    elif areacode == '32':
        map_center = (37.8906058762612, 127.73837096643754)
    elif areacode == '33':
        map_center = (36.62972250605737, 127.49307575575378)
    elif areacode == '34':
        map_center = (36.57182436023331, 126.60960011755672)
    elif areacode == '35':
        map_center = (36.57819644307364, 128.78265408075143)
    elif areacode == '36':
        map_center = (35.22747853906293, 128.6780491168389)
    elif areacode == '37':
        map_center = (35.81341565877149, 127.1475287246022)
    elif areacode == '38':
        map_center = (34.815157577762854, 126.46303922198267)
    else:
        map_center = (33.38026768427147, 126.53863521202281)

    # 테마 선택
    if contents_type == '12':
        theme_marker = 'tour'
    elif contents_type == '14':
        theme_marker = 'culture'
    elif contents_type == '15':
        theme_marker = 'festival'
    elif contents_type == '28':
        theme_marker = 'leports'
    elif contents_type == '32':
        theme_marker = 'stay'
    elif contents_type == '38':
        theme_marker = 'shopping'
    else:
        theme_marker = 'restaurant'

    # 테마별 좌표 리스트
    # 로그인 된 유저 ID필요
    # user_id = User.object.get('user_id')
    tour_context       = search_data(12, areacode)
    culture_context    = search_data(14, areacode)
    festival_context   = search_data(15, areacode)
    leports_context    = search_data(28, areacode)
    stay_context       = search_data(32, areacode)
    shopping_context   = search_data(38, areacode)
    restaurant_context = search_data(39, areacode)

    context = {}
    context['tour_context']       = tour_context
    context['culture_context']    = culture_context
    context['festival_context']   = festival_context
    context['leports_context']    = leports_context
    context['stay_context']       = stay_context
    context['shopping_context']   = shopping_context
    context['restaurant_context'] = restaurant_context
    context['areacode']           = map_center
    context['content_type']      = theme_marker
    # print(context['content_type'])

    context_json = json.dumps(context)
    # print( {'context_json': context_json}, type( {'context_json': context_json} )   ) 
    # print( {'context': context_json}, type( {'context': context_json} )   ) 

    return render(request, 'travels/n_map.html', {'context': context_json} )


def search_data(c_type, loc):
    # dataset = get_api_data(1000)
    
    # 여행지 불러오기
    data = models.TravelSpot.objects.all()
    # 여행지 평가 불러오기

    context  = {}
    title_li = []
    x_li     = []
    y_li     = []
    for i in range(0, len(data)):
        if (data[i].content_type == int(c_type)) & (data[i].areacode == int(loc)):    
            title_li.append(data[i].title)
            x_li.append(data[i].mapx)
            y_li.append(data[i].mapy)

    context['title'] = title_li[:5]
    context['mapx']  = x_li[:5]
    context['mapy']  = y_li[:5]
    # context['reco_list'] = li

    return context

def reco_data(request, c_type, loc):
    # 여행지 불러오기
    datas   = models.TravelSpot.objects.all()
    # 여행지 평가 불러오기
    data_r = models.TravelRating.objects.filter(content_type=c_type, areacode=loc)

    # 현재 로그인 된 유저 아이디 받기
    user = request.user.get_username

    # 메트릭스 만들기
    matrix = data_r.pivot_table(index='user_id', columns='content_id')['rating']
    matrix.fillna(-1, inplace=True)
    
    # 추천 받기
    li = []
    for rate, c_id in recommendation(matrix, user):
        li.append((rate, datas.loc[ datas['content_id'] == c_id, 'title' ].values[0]))
    reco_li = li[:5]

    # title 기반으로 좌표값 불러오기
    t_li = []
    x_li = []
    y_li = []
    for i in range(len(reco_li)) :
        t_li.append(datas[ datas['title']== reco_li[i][1]].title.values[0])
        x_li.append(datas[ datas['title']== reco_li[i][1]].mapx.values[0])
        y_li.append(datas[ datas['title']== reco_li[i][1]].mapy.values[0])
    
    # 추천 결과
    context = {}
    context['title'] = t_li
    context['mapx']  = x_li
    context['mapy']  = y_li

    return context


# kdd 유사도 함수
def sim_distance(data, n1, n2):
    sum = 0
    # 두 사용자가 모두 간 여행지를 기준으로 해야해서 i로 변수 통일(j따로 안 써줌)
    for i in data.loc[n1, data.loc[n1, :] >= 0].index:
        if data.loc[n2, i] >= 0:
            sum += pow(data.loc[n1, i]-data.loc[n2, i], 2) # 누적합
    return sqrt(1/(sum+1))  # 유사도 형식으로 출력

    # 나와 유사도가 높은 user 매칭 함수


def top_match(data, name, rank=5, simf= sim_distance):
    simList = []
    for i in data.index[-10:]:
        if name != i:
            simList.append((simf(data, name, i), i))
    simList.sort()
    simList.reverse()
    return simList[:rank]

    # 추천 시스템 함수


def recommendation(data, person, simf=sim_distance):
    res = top_match(data, person, len(data))
    score_dic = {}
    sim_dic = {}
    myList = []
    for sim, name in res:
        if sim < 0:
            continue
        for movie in data.loc[person, data.loc[person, :] < 0].index:
            simSum = 0
            if data.loc[name, movie] >= 0:
                simSum += sim * data.loc[name, movie]

                score_dic.setdefault(movie, 0)
                score_dic[movie] += simSum

                sim_dic.setdefault(movie, 0)
                sim_dic[movie] += sim
    for key in score_dic:
        myList.append((score_dic[key] / sim_dic[key], key))
    myList.sort()
    myList.reverse()

    return myList