from django.shortcuts import render
import requests
import json
from . import models
import core.travel as travel

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
    username = None
    username = request.user.username
    tour_context       = search_data(username, 12, areacode)
    culture_context    = search_data(username, 14, areacode)
    festival_context   = search_data(username, 15, areacode)
    leports_context    = search_data(username, 28, areacode)
    stay_context       = search_data(username, 32, areacode)
    shopping_context   = search_data(username, 38, areacode)
    restaurant_context = search_data(username, 39, areacode)

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


def search_data(username, c_type, loc):
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
    try:
        if username != None:
            context['reco_list'] = travel.reco_data(username, c_type, loc)
    except:
        pass
    
    return context
