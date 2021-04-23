from django.shortcuts import render
import requests
import json
from math import sqrt
# import pandas as pd

# Create your views here.


def index(request):
    loc = request.POST.get('loc', False)
    theme = request.POST.get('theme', False)

    # 세션
    request.session['loc'] = loc
    request.session['theme'] = theme

    print('\n<<<<<<<<<<<<<<<<<<<<', loc, theme, '>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')

    return render(request, 'index.html')


def n_map(request):
    # Tour API 3.0
    api_data = get_api_data(10)

    # 조건 검색
    contents_type = request.session['theme']
    areacode = request.session['loc']

    # 맵 중앙 좌표 설정
    if areacode == 1:
        map_center = (37.56099073728087, 126.9888542058965)
    elif areacode == 2:
        map_center = (37.469865204921014, 126.70146425886135)
    elif areacode == 3:
        map_center = (36.34141096399956, 127.39360630587186)
    elif areacode == 4:
        map_center = (35.83394171476235, 128.5658367309032)
    elif areacode == 5:
        map_center = (35.16066738624785, 126.83692058211457)
    elif areacode == 6:
        map_center = (35.17217626215749, 129.04434051065476)
    elif areacode == 7:
        map_center = (35.552624380057935, 129.2615077003808)
    elif areacode == 8:
        map_center = (36.5613704176564, 127.25756722506266)
    elif areacode == 31:
        map_center = (37.2820719546124, 127.00679578588812)
    elif areacode == 32:
        map_center = (37.8906058762612, 127.73837096643754)
    elif areacode == 33:
        map_center = (36.62972250605737, 127.49307575575378)
    elif areacode == 34:
        map_center = (36.57182436023331, 126.60960011755672)
    elif areacode == 35:
        map_center = (36.57819644307364, 128.78265408075143)
    elif areacode == 36:
        map_center = (35.22747853906293, 128.6780491168389)
    elif areacode == 37:
        map_center = (35.81341565877149, 127.1475287246022)
    elif areacode == 38:
        map_center = (34.815157577762854, 126.46303922198267)
    else:
        map_center = (33.38026768427147, 126.53863521202281)

    # 테마 선택
    if contents_type == 12:
        theme_marker = 'tour'
    elif contents_type == 14:
        theme_marker = 'culture'
    elif contents_type == 15:
        theme_marker = 'festival'
    elif contents_type == 28:
        theme_marker = 'leports'
    elif contents_type == 32:
        theme_marker = 'stay'
    elif contents_type == 38:
        theme_marker = 'shopping'
    else:
        theme_marker = 'restaurant'

    # 테마별 좌표 리스트
    # 로그인 된 유저 ID필요
    # user_id = User.object.get('user_id')
    tour_context = search_data(12, areacode)
    culture_context = search_data(14, areacode)
    festival_context = search_data(15, areacode)
    leports_context = search_data(28, areacode)
    stay_context = search_data(32, areacode)
    shopping_context = search_data(38, areacode)
    restaurant_context = search_data(39, areacode)

    context = {}
    context['tour_context'] = tour_context
    context['culture_context'] = culture_context
    context['festival_context'] = festival_context
    context['leports_context'] = leports_context
    context['stay_context'] = stay_context
    context['shopping_context'] = shopping_context
    context['restaurant_context'] = restaurant_context
    context['loc'] = map_center
    context['theme'] = theme_marker

    # context = {}
    # id_li = []
    # x_li = []
    # y_li = []
    # for i in range(0, len(api_data)):
    #     x = api_data[i]
    #     id_li.append(x['contentid'])
    #     x_li.append(x['mapx'])
    #     y_li.append(x['mapy'])

    # context['contentid'] = id_li
    # context['mapx'] = x_li
    # context['mapy'] = y_li

    context_json = json.dumps(context)
    # print({'context_json': context_json}, type({'context_json': context_json}))

    return render(request, 'n_map.html', {'context_json': context_json})


def get_api_data(call_num):
    api_key = 'T4ebYJHsl1CoTek15CyU8BnOmjVBlp84r7KkJKJpMJxueYXFf0HVjQgPxy7xc7sZ1XbNGJsIWXOf9LEDr893Xg%3D%3D'
    api_url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey={}&contentTypeId=&areaCode=&sigunguCode=&cat1=&cat2=&cat3=&listYN=Y&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&arrange=A&numOfRows={}&pageNo=1&_type=json'.format(
        api_key, call_num)
    api_data = requests.get(api_url).json()
    dataset = []
    for i in range(0, len(api_data['response']['body']['items']['item'])):
        x = api_data['response']['body']['items']['item'][i]
        dataset.append(x)

    return dataset


def search_data(contents_type, areacode):
    dataset = get_api_data(1000)
    
    # 여행지 불러오기
    # 여행지 평가 불러오기

    # 25번 user가 안본 여행지중에서
    # 추천 점수가 가장 높은 순으로 예상평점과 여행지를 추천 (10개까지)
    li = []
    for rate, m_id in recommendation(data_table, user_id):
        li.append(
            (rate, spot_data.loc[spot_data['content_id'] == m_id, 'theme1'].values[0]))

    context = {}
    id_li = []
    x_li = []
    y_li = []
    for i in range(0, len(dataset)):
        if dataset[i]['contenttypeid'] == contents_type and dataset[i]['areacode'] == areacode:
            id_li.append(dataset[i]['contentid'])
            x_li.append(dataset[i]['mapx'])
            y_li.append(dataset[i]['mapy'])

    context['contentid'] = id_li[:5]
    context['mapx'] = x_li[:5]
    context['mapy'] = y_li[:5]
    context['reco_list'] = li

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
