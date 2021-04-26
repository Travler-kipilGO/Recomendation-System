from travels.models import TravelSpot, TravelRating
from math import sqrt
import pandas as pd

def reco_data(username, c_type, loc):
    # 여행지 불러오기
    data   = pd.DataFrame(TravelSpot.objects.all().values())
    # 여행지 평가 불러오기
    data_r = pd.DataFrame(
        [
            [travelRating.user.username, travelRating.mytripdata.travelspot.content_id, travelRating.mytripdata.travelspot.content_type, travelRating.rating]
            for travelRating in TravelRating.objects.filter(mytripdata__travelspot__content_type=c_type, mytripdata__travelspot__areacode=loc)
            
        ],
        columns=['user_id', 'content_id', 'content_type', 'rating'])
    data_r[['content_id', 'content_type']] = data_r[['content_id', 'content_type']].astype(int)
    data_r[['rating']] = data_r[['rating']].astype(float)

    # 현재 로그인 된 유저 아이디 받기
    user = username

    # 메트릭스 만들기
    matrix = pd.pivot_table(data_r, index="user_id", columns="content_id", values='rating')
    matrix.fillna(-1, inplace=True)

    # 추천 받기
    li = []
    for rate, c_id in recommendation(matrix, user):
        li.append((rate, data.loc[ data['content_id'] == c_id, 'title' ].values[0]))
    reco_li = li[:5]
 
    # title 기반으로 좌표값 불러오기
    t_li = []
    x_li = []
    y_li = []
    for i in range(len(reco_li)) :
        t_li.append(data[ data['title']== reco_li[i][1]].title.values[0])
        x_li.append(data[ data['title']== reco_li[i][1]].mapx.values[0])
        y_li.append(data[ data['title']== reco_li[i][1]].mapy.values[0])
    
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