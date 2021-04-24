from sklearn.linear_model import LinearRegression 
from sklearn.model_selection import train_test_split 
import pandas as pd
import numpy as np

from accommodations.models import Accommodation
from users.models import User
from reviews.models import Review

def init():
    accommodations = Accommodation.objects.all()
    users = User.objects.all()
    reviews = Review.objects.all()
    
    hotel_df = pd.DataFrame([ accommodation.name for accommodation in accommodations], columns=['hotel'])
    user_df = pd.DataFrame([user.username for user in users], columns=['user']) 
    sparse_matrix = pd.DataFrame(index=user_df['user'].values, columns=hotel_df['hotel'].values)

    for review in reviews:
        sparse_matrix.loc[review.user.username, review.accommodation.name] = review.rating_average()

    sparse_matrix = sparse_matrix.astype(float)
    return sparse_matrix


def fill_nan_with_user_mean(rating_data):
    filled_data = np.copy(rating_data)  
    row_mean = np.nanmean(filled_data, axis=0)  
    inds = np.where(np.isnan(filled_data))  
    filled_data[inds] = np.take(row_mean, inds[1])    
    return filled_data

def sim_pearson(user_1, user_2):
  avg_user1 = np.mean(user_1)
  avg_user2 = np.mean(user_2)

  sum = np.sum((user_1 - avg_user1) * (user_2 - avg_user2))
  sum_name1 = np.sum((user_1 - avg_user1)**2)
  sum_name2 = np.sum((user_2 - avg_user2)**2)

  return sum / (np.sqrt(sum_name1) * np.sqrt(sum_name2))

def get_k_neighbors(user, k, distance=sim_pearson):
    sparse_matrix = init()
    users = sparse_matrix.index.values
    user_id = np.where(users == user)[0][0]

    filled_data = fill_nan_with_user_mean(sparse_matrix)
    distance_data = np.append(filled_data, np.zeros((filled_data.shape[0], 1)), axis=1) 
     
    for i in range(len(distance_data)):
        row = distance_data[i] 
        if i == user_id:  
            row[-1] = -np.inf 
        else:  
            row[-1] = distance(distance_data[user_id][:-1], row[:-1]) 
     
    distance_data = distance_data[np.argsort(distance_data[:, -1])[::-1]]
    first = np.argmax(distance_data[:k, :-1], axis=1)[0]
    second = np.argmax(distance_data[:k, :-1], axis=1)[1]
    third = np.argmax(distance_data[:k, :-1], axis=1)[2]
    return (sparse_matrix.columns.values[first],  sparse_matrix.columns.values[second], sparse_matrix.columns.values[third])