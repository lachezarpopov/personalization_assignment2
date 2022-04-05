import streamlit as st
import pandas as pd
import template as t
import numpy as np
from PIL import Image
import authenticate as a
import json
from itertools import cycle
from random import random

# Internet balk layout
img = Image.open('NPO.jpg')
st.set_page_config(layout="wide", page_title='NPO prototype', page_icon=img)

# Hide made with streamlit:
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;} 
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# load the dataset with the shows
df_npo = pd.read_csv('./sample_npo2.csv')  # , sep=';', encoding='utf8'

# Load users
df_users = pd.read_json('users.json')

# Trying everything


# Sidebar layout
st.sidebar.image("./NPO.jpg", use_column_width=True)
st.sidebar.title('Welcome to the NPO')

# add_selectbox = st.sidebar.selectbox(
#    "How would you like to be contacted?",
#    (df_npo['Cluster'])
# )

# open the activities json file
with open('activities.json') as json_file:
    users_activities = json.load(json_file)


# Main page layout:
#st.image("./NPO.jpg", use_column_width=True)
st.header('Start watching on NPO' + '  ' + '     ▶️ ')

# Create session state:

if 'titles' not in st.session_state:
    st.session_state['titles'] = 'Vlaamse Meiden die Rijden '

if 'user' not in st.session_state:
    st.session_state['user'] = 0

if 'activities' not in st.session_state:
    st.session_state['activities'] = users_activities

if 'ratings' not in st.session_state:
    st.session_state['ratings'] = pd.read_csv('ratings.csv')

    # authenticate
a.authenticate()

# Select title
df_titles = df_npo[df_npo['titles'] == st.session_state['titles']]

#
df_npomroep = df_npo[df_npo['titles'] == st.session_state['titles']]

if st.session_state['authentication_status'] != True:
    st.write('Please log in to view the content on the platform.')


else:

    # create a cover and info column to display the selected show
    cover, info = st.columns([2, 3])

    with cover:
        # display the image
        st.image(df_npomroep['pictures'].iloc[0])

    with info:
        # display the book information

        st.title(df_npomroep['titles'].iloc[0])
        st.caption(df_npomroep['descriptions'].iloc[0])
        # st.caption(df_npomroep['k_means'].iloc[0])
    #     selectbox = st.selectbox(
    #         "Rate the show",
    #         ('1', '2', '3', '4', '5'))
    # # Outcome is in selectbox, maybe we can save the value with the current user? @Zaro
    #     st.write('Thanks', selectbox)

    # This works.. but I don't know how to implement something like this in selectbox
    # This saves to JSON
    # Explicit and implicit feedback:
        with st.expander('Rate the show'):
            st.button('⭐', key=random(), on_click=t.rating,
                      args=(df_titles['ID'].values[0], '1'))
            st.button('⭐⭐', key=random(), on_click=t.rating,
                      args=(df_titles['ID'].values[0], '2'))
            st.button('⭐⭐⭐', key=random(), on_click=t.rating,
                      args=(df_titles['ID'].values[0], '3'))
            st.button('⭐⭐⭐⭐', key=random(), on_click=t.rating,
                      args=(df_titles['ID'].values[0], '4'))
            st.button('⭐⭐⭐⭐⭐', key=random(), on_click=t.rating,
                      args=(df_titles['ID'].values[0], '5'))

    # recommendations based on youth,adult,senior column

    # Shows from youth group:
    if st.session_state['persona'] == 'ambitiousyouth':
        st.subheader('Youth might like: ')  # title should be changed later on
        df_recommendations2 = df_npo[df_npo['youth'] == 1]
        df_recommendations2 = df_recommendations2.sample(5)
        t.recommendations(df_recommendations2)

    if st.session_state['persona'] == 'adventurouscitydweller':
        st.subheader('Adults might like: ')  # title should be changed later on
        df_recommendations2 = df_npo[df_npo['adults'] == 1]
        df_recommendations2 = df_recommendations2.sample(5)
        t.recommendations(df_recommendations2)

    if st.session_state['persona'] == 'cautioussenior':
        # title should be changed later on
        st.subheader('Seniors might like: ')
        df_recommendations2 = df_npo[df_npo['seniors'] == 1]
        df_recommendations2 = df_recommendations2.sample(5)
        t.recommendations(df_recommendations2)


# based on current persona

    if st.session_state['persona'] in ['adventurouscitydweller', 'cautioussenior']:
        # Shows from nature genre:
        st.subheader('Nature: ')
        df_recommendations2 = df_npo[df_npo['nature'] == 1].sample(5)
        t.recommendations(df_recommendations2)

        # Shows from politics genre:
        st.subheader('Politics: ')
        df_recommendations10 = df_npo[df_npo['politics'] == 1].sample(5)
        t.recommendations(df_recommendations10)

        # Shows from history genre:
        st.subheader('History: ')
        df_recommendations3 = df_npo[df_npo['history'] == 1].sample(5)
        t.recommendations(df_recommendations3)

    if st.session_state['persona'] in ['adventurouscitydweller']:
        # Shows from travel genre:
        st.subheader('Travel: ')
        df_recommendations4 = df_npo[df_npo['travel'] == 1].sample(5)
        t.recommendations(df_recommendations4)

        # Shows from education genre:
        st.subheader('Educational: ')
        df_recommendations7 = df_npo[df_npo['educational'] == 1].sample(5)
        t.recommendations(df_recommendations7)

    if st.session_state['persona'] in ['ambitiousyouth', 'adventurouscitydweller', 'cautioussenior']:
        # Shows from romantic genre:
        st.subheader('Romantic: ')
        df_recommendations5 = df_npo[df_npo['romantic'] == 1].sample(5)
        t.recommendations(df_recommendations5)

        # Shows from crime genre:
        st.subheader('Crime: ')
        df_recommendations8 = df_npo[df_npo['crime'] == 1].sample(5)
        t.recommendations(df_recommendations8)

        # Shows from reality genre:
        st.subheader('Reality: ')  # ?
        df_recommendations12 = df_npo[df_npo['reality'] == 1].sample(5)
        t.recommendations(df_recommendations12)

    if st.session_state['persona'] in ['ambitiousyouth', 'adventurouscitydweller']:
        # Shows from diversity genre:
        st.subheader('Diversity: ')
        df_recommendations6 = df_npo[df_npo['diversity'] == 1].sample(5)
        t.recommendations(df_recommendations6)

    if st.session_state['persona'] in ['ambitiousyouth']:
        # Shows from action genre:
        st.subheader('Action: ')
        df_recommendations9 = df_npo[df_npo['action'] == 1].sample(5)
        t.recommendations(df_recommendations9)

        # Shows from teen genre:
        st.subheader('Teen: ')
        df_recommendations11 = df_npo[df_npo['teen'] == 1].sample(5)
        t.recommendations(df_recommendations11)

    # Shows from same k_means cluster
    st.subheader('Similar shows like ' + st.session_state['titles'])
    df_recommendations = df_npo[df_npo['k_means']
                                == df_npomroep['k_means'].iloc[0]].sample(5)
    t.recommendations(df_recommendations)

    #st.subheader('Start watching on NPO ')
    st.subheader('Select your favorite genre ')
    option2 = st.selectbox(
        ' ',
        ('nature', 'history', 'travel', 'romantic', 'diversity', 'educational', 'crime', 'action', 'politics', 'teen', 'reality'))
    st.subheader('Shows from ' + option2)
    df_recommendations = df_npo[df_npo[option2] == 1].sample(6)
    t.recommendations(df_recommendations)

    # Dropdown for own choice
    st.subheader('Choose the show you want to watch ')
    option = st.selectbox(
        'Select your favorite show and click play to start watching!',
        (df_npo['titles']))
    df = df_npo[df_npo['titles'] == option]
    t.recommendations(df)
