import streamlit as st
from random import random
import json
import datetime
import pandas as pd
import numpy as np


# save the activities as a file
def save_activities():
    with open('activities.json', 'w') as outfile:
        json.dump(st.session_state['activities'], outfile)


def save_ratings():
    st.session_state['ratings'].to_csv('ratings.csv', index=False)

# function that processes an activity


def activity(id, activity):
    data = {'content_id': id, 'activity': activity,
            'user_id': st.session_state['user'], 'datetime': str(datetime.datetime.now())}
    # add to the session state
    st.session_state['activities'].append(data)
    # directly save the activities
    save_activities()


def rating(content_id, rating):
    user = st.session_state['user']
    ratings = st.session_state['ratings']

    if content_id in ratings.loc[(ratings['user'] == user), 'content_id'].values:
        ratings.loc[(ratings['user'] == user) & (
            ratings['content_id'] == content_id), 'rating'] = rating
    else:
        data = {'user': st.session_state['user'],
                'content_id': content_id, 'rating': rating}
        st.session_state['ratings'] = ratings.append(
            data, ignore_index=True)
    save_ratings()


# set episode session state
def select_show(title):
    st.session_state['titles'] = title
    activity(title, 'Select title')


def tile_item(column, item):
    with column:
        st.button('▶️', key=random(), on_click=select_show,
                  args=(item['titles'], ))
        st.image(item['pictures'], use_column_width='always')
        st.caption(item['titles'])


def recommendations(df):

    # check the number of items
    nbr_items = df.shape[0]
    cols = 6

    if nbr_items != 0:

        # create columns with the corresponding number of items
        columns = st.columns(nbr_items)

        # convert df rows to dict lists
        items = df.to_dict(orient='records')

        # apply tile_item to each column-item tuple (created with python 'zip')
        any(tile_item(x[0], x[1]) for x in zip(columns, items))


def personalizedRecommendations(ratings, user):

    userRatings = ratings.pivot(
        index='content_id', columns='user', values='rating').fillna(np.nan)[user]
    userItemMatrix = ratings.pivot(index='content_id', columns='user', values='rating').fillna(
        np.nan).drop(user, axis='columns')

    # Calculating user similarities
    user_similarities = userItemMatrix.apply(
        userRatings.corr, axis=0)
    neighbourhood_similarities = user_similarities[user_similarities > 0.10]

    # Filtering userItemMatrix for similar users only
    similar_users = userItemMatrix.loc[:, user_similarities > 0.10]

    # Creating neighbourhood_unseen df
    # the shows unseen by the target user that appear in the neightbourhood of similar users
    neighbourhood_unseen = similar_users[~similar_users.index.isin(
        userRatings[userRatings.isna()].index)]

    # Applying weights (based on similarity) to ratings
    def apply_weights(x): return x * neighbourhood_similarities[x.name]
    weighted_scores = neighbourhood_unseen.apply(apply_weights)

    # Filtering out shows that have been rated by less than n_users**0.5 number of users
    n_users = weighted_scores.shape[1]
    unseen_min_neighbourhood = weighted_scores[weighted_scores.transpose(
    ).count() >= n_users**0.5]

    # Calculating similarity-weighted recommendations
    def weighted_rating(show): return show.sum() / \
        neighbourhood_similarities[show.notna()].sum()
    personalized_recommendations = unseen_min_neighbourhood.apply(
        weighted_rating, axis=1).sort_values(ascending=False).head(5)

    personalized_recommendations = personalized_recommendations.round(
        2)  # rounding the predicted rating

    return personalized_recommendations
