import requests
import pandas as pd
import numpy  as np

import random
from scipy import sparse
from scipy.sparse.linalg import spsolve
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MaxAbsScaler

from travels.models import UserLogData


def init():
    userLogDatas = UserLogData.objects.all()    
    userlog_df = pd.DataFrame(
      [
        [userLogData.user.username, userLogData.travelspot.content_id, userLogData.travelspot.title, userLogData.click, userLogData.date]
        for userLogData in userLogDatas
      ],
      columns = ['user', 'content_id', 'content_title', 'click', 'date']
    )
    return userlog_df

def make_train (matrix, percentage = .2):
    '''
    -----------------------------------------------------
    설명
    유저-아이템 행렬 (matrix)에서 
    1. 0이상의 값을 가지면 1의 값을 갖도록 binary하게 테스트 데이터를 만들고
    2. 훈련 데이터는 원본 행렬에서 percentage 비율만큼 0으로 바뀜
    
    -----------------------------------------------------
    반환
    training_set: 훈련 데이터에서 percentage 비율만큼 0으로 바뀐 행렬
    test_set:     원본 유저-아이템 행렬의 복사본
    user_inds:    훈련 데이터에서 0으로 바뀐 유저의 index
    '''
    test_set = matrix.copy()
    test_set[test_set !=0] = 1 # binary하게 만들기
    
    training_set = matrix.copy()
    nonzero_inds = training_set.nonzero()
    nonzero_pairs = list(zip(nonzero_inds[0], nonzero_inds[1]))
    
    random.seed(0)
    num_samples = int(np.ceil(percentage * len(nonzero_pairs)))
    samples = random.sample(nonzero_pairs, num_samples)
    
    user_inds = [index[0] for index in samples]
    item_inds = [index[1] for index in samples]
    
    # eliminate_zeros(): Remove zero entries from the matrix
    training_set[user_inds, item_inds] = 0
    training_set.eliminate_zeros()
    
    return training_set, test_set, list(set(user_inds))


def main(username):
    userlog_df = init()
    item_lookup = userlog_df[['content_id','content_title']].drop_duplicates()
    item_lookup['content_id'] = item_lookup['content_id']
    cleaned_log = userlog_df[['user','content_id','click']]
    grouped_cleaned = cleaned_log.groupby(['user','content_id']).sum().reset_index() #reset_index() 행 인덱스 초기화
    grouped_purchased = grouped_cleaned[grouped_cleaned['click'] > 0]
    customers = list(np.sort(grouped_purchased['user'].unique()))
    products = list (grouped_purchased['content_id'].unique())
    quantity = list(grouped_purchased['click'])
    rows = grouped_purchased['user'].astype('category').cat.codes 
    cols = grouped_purchased['content_id'].astype('category').cat.codes
    purchase_sparse = sparse.csr_matrix((quantity, (rows, cols)), shape = (len(customers),len(products)))

    product_train, product_test, product_users_altered = make_train(purchase_sparse, 0.2)

    
    pref_vec = product_train[0,:].toarray() # Get the ratings from the training set ratings matrix
    pref_vec = pref_vec.reshape(-1) + 1 # Add 1 to everything, so that items not purchased yet become equal to 1
    pref_vec[pref_vec > 1] = 0 # Make everything already purchased zero

    user_vecs, item_vecs = implicit_weighted_ALS (product_train
                                              , lambda_val = 0.1
                                              , alpha = 15
                                              , n_iter = 10
                                              , rank_size = 20)
    
    rec_vector = user_vecs[0,:].dot(item_vecs) # Get dot product of user vector and all item vectors
    rec_vector = rec_vector.toarray()

    # Scale this recommendation vector between 0 and 1
    min_max = MinMaxScaler()
    rec_vector_scaled = min_max.fit_transform(rec_vector.reshape(-1,1))[:,0] 

    recommend_vector = pref_vec*rec_vector_scaled
    #print(recommend_vector)
    
    customers_arr = np.array(customers)
    products_arr = np.array(products)
    product_idx = np.argsort(recommend_vector)[::-1][:5]
    purchaseData = get_items_purchased(username, product_train, customers_arr, products_arr, item_lookup)
    recData = rec_items(username, product_train, user_vecs, item_vecs, customers_arr, products_arr, item_lookup, num_items = 10)
    return purchaseData.values.tolist(), recData.values.tolist()


def implicit_weighted_ALS(training_set, lambda_val =.1, alpha = 40, n_iter = 10, rank_size = 20, seed = 0):
    '''
    협업 필터링에 기반한 ALS
    -----------------------------------------------------
    input
    1. training_set : m x n 행렬로, m은 유저 수, n은 아이템 수를 의미. csr 행렬 (희소 행렬) 형태여야 함 
    2. lambda_val: ALS의 정규화 term. 이 값을 늘리면 bias는 늘지만 분산은 감소. default값은 0.1
    3. alpha: 신뢰 행렬과 관련한 모수 (C_{ui} = 1 + alpha * r_{ui}). 이를 감소시키면 평점 간의 신뢰도의 다양성이 감소
    4. n_iter: 반복 횟수. 논문에서는 10~ 15회 정도 설정
    5. rank_size: 유저/ 아이템 특성 벡터의 잠재 특성의 개수. 논문에서는 20 ~ 200 사이를 추천하고 있음. 이를 늘리면 과적합 위험성이 있으나 
    bias가 감소
    6. seed: 난수 생성에 필요한 seed
    -----------------------------------------------------
    반환
    유저와 아이템에 대한 특성 벡터
    '''
    
    # 1. Confidence matrix
    # C = 1+ alpha * r_{ui}
    conf = (alpha*training_set) # sparse 행렬 형태를 유지하기 위해서 1을 나중에 더함
    
    num_user = conf.shape[0]
    num_item = conf.shape[1]

    # X와 Y 초기화
    rstate = np.random.RandomState(seed)
    X = sparse.csr_matrix(rstate.normal(size = (num_user, rank_size)))
    Y = sparse.csr_matrix(rstate.normal(size = (num_item, rank_size)))
    # sparse.eye: Sparse matrix with ones on diagonal 
    X_eye = sparse.eye(num_user)
    Y_eye = sparse.eye(num_item)
    
    # 정규화 term: 𝝀I
    lambda_eye = lambda_val * sparse.eye(rank_size)
    
    # 반복 시작
    for i in range(n_iter):
        yTy = Y.T.dot(Y)
        xTx = X.T.dot(X)
        
        # Y를 고정해놓고 X에 대해 반복
        # Xu = (yTy + yT(Cu-I)Y + 𝝀I)^{-1} yTCuPu
        for u in range(num_user):
            conf_samp = conf[u,:].toarray() # Cu
            pref = conf_samp.copy()
            pref[pref!=0] = 1
            # Cu-I: 위에서 conf에 1을 더하지 않았으니까 I를 빼지 않음 
            CuI = sparse.diags(conf_samp, [0])
            # yT(Cu-I)Y
            yTCuIY = Y.T.dot(CuI).dot(Y)
            # yTCuPu
            yTCupu = Y.T.dot(CuI+Y_eye).dot(pref.T)
            
            X[u] = spsolve(yTy + yTCuIY + lambda_eye, yTCupu)
        
        # X를 고정해놓고 Y에 대해 반복
        # Yi = (xTx + xT(Cu-I)X + 𝝀I)^{-1} xTCiPi
        for i in range(num_item):
            conf_samp = conf[:,i].T.toarray()
            pref = conf_samp.copy()
            pref[pref!=0] = 1
            
            #Ci-I
            CiI = sparse.diags(conf_samp, [0])
            # xT(Ci-I)X
            xTCiIX = X.T.dot(CiI).dot(X)
            # xTCiPi
            xTCiPi = X.T.dot(CiI+ X_eye).dot(pref.T)
            
            Y[i] = spsolve(xTx + xTCiIX + lambda_eye, xTCiPi)
            
        return X, Y.T

def get_items_purchased(customer_id, mf_train, customer_list, products_list, item_lookup):
    '''
    특정 유저가 구매한 목록을 보여주는 함수
    ----------------------------------------
    INPUT
    1. customer_id: 고객 ID
    2. mf_train: 훈련 데이터 평점
    3. customers_list: 훈련 데이터에 쓰인 고객 목록
    4. products_list: 훈련 데이터에 쓰인 아이템 목록
    5. item_lookup: 유니크한 아이템 ID와 설명을 담은 테이블
    '''
    cust_ind = np.where (customer_list == customer_id)[0][0]
    purchased_ind = mf_train[cust_ind,:].nonzero()[1]
    prod_codes = products_list[purchased_ind]
    
    return item_lookup[item_lookup.content_id.isin(prod_codes.tolist())]

def rec_items(customer_id, mf_train, user_vecs, item_vecs, customer_list, item_list, item_lookup, num_items = 10):
    '''
    유저의 추천 아이템 반환
    -----------------------------------------------------
    INPUT
    1. customer_id - Input the customer's id number that you want to get recommendations for
    2. mf_train: 훈련 데이터
    3. user_vecs: 행렬 분해에 쓰인 유저 벡터
    4. item_vecs: 행렬 분해에 쓰인 아이템 벡터
    5. customer_list: 평점 행렬의 행에 해당하는 고객 ID
    6. item_list: 평점 행렬의 열에 해당하는 아이템 ID
    7. item_lookup: 아이템 ID와 설명을 담은 테이블
    8. num_items: 추천할 아이템 개수
    -----------------------------------------------------
    반환    
    구매한 적이 없는 아이템 중 예측 평점이 높은 최고 n개의 추천 아이템
    '''
    
    pref_vec = mf_train[0,:].toarray() # Get the ratings from the training set ratings matrix
    pref_vec = pref_vec.reshape(-1) + 1 # Add 1 to everything, so that items not purchased yet become equal to 1
    pref_vec[pref_vec > 1] = 0 # Make everything already purchased zero
    rec_vector = user_vecs[0,:].dot(item_vecs) # Get dot product of user vector and all item vectors
    rec_vector = rec_vector.toarray()

    # Scale this recommendation vector between 0 and 1
    min_max = MinMaxScaler()
    rec_vector_scaled = min_max.fit_transform(rec_vector.reshape(-1,1))[:,0] 

    recommend_vector = pref_vec*rec_vector_scaled
    
    product_idx = np.argsort(recommend_vector)[::-1][:num_items] # Sort the indices of the items into order 
    # of best recommendations
    rec_list = [] # start empty list to store items
    
    for index in product_idx:
        code = item_list[index]
        rec_list.append([code, item_lookup.content_title.loc[item_lookup.content_id == code].iloc[0]]) 
        # Append our descriptions to the list
        
    codes = [item[0] for item in rec_list]
    descriptions = [item[1] for item in rec_list]
    final_frame = pd.DataFrame({'content_id': codes, 'content_title': descriptions}) # Create a dataframe 
    return final_frame[['content_id', 'content_title']] # Switch order of columns around

