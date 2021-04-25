import numpy as np
import pandas as pd
import math
from math import sqrt

from users.models import Survey


def init():
    surveys = Survey.objects.all()

    survey_df = pd.DataFrame(
      [
        [survey.user.username, survey.theme]
        for survey in surveys
      ],
      columns = ['user', 'themacode']
    )
    survey_df['rating'] = 1
    
    theme_data = survey_df.pivot_table('rating', index='user', columns='themacode').fillna(0).astype(int)
    return theme_data.T.to_dict()


def dropna(data): 
    for i in data:
        for j in data[i]:
            name=i
            theme=j
            value=data[i][j]
        data[i]={travel: value for travel, value in data[i].items() if pd.isnull(value)==False}
    return data

def sim_pearson(data, n1, n2): 
    sumX=0
    sumY=0
    sumSqX=0 # x 제곱합 
    sumSqY=0 # y 제곱합 
    sumXY=0 # XY 합
    global cnt # 테마 갯수
    cnt=0
    for i in data[n1]:
        if i in data[n2]:
            sumX+=data[n1][i]
            sumY+=data[n2][i]
            sumSqX+=pow(data[n1][i],2)
            sumSqY+=pow(data[n2][i],2)
            sumXY+=(data[n1][i])*(data[n2][i])
            cnt+=1
            global num
            global den
            num=sumXY-((sumX*sumY)/cnt)
            den= (sumSqX-(pow(sumX,2)/cnt))*(sumSqY-(pow(sumY,2)/cnt))
    return num/sqrt(den+0.00001) # 분모=0방지

def top_match(data, name, rank=3, simf=sim_pearson):
    simList=[] # 유사한 테마들이 저장될 리스트
    for i in data:
        if name!=i: # 자기 자신 제외
            simList.append((simf(data, name, i),i))
    simList.sort() # 오름차순
    simList.reverse() # 내림차순
    return simList[:rank]

def main(username):
  theme_data_dic = init()
  theme_data_dic_drop = dropna(theme_data_dic)    
  return top_match(theme_data_dic_drop, username, 3)