import streamlit as st
from random import random
import json
import datetime


# save the activities as a file
def save_activities():
  with open('activities.json', 'w') as outfile:
    json.dump(st.session_state['activities'], outfile)

# function that processes an activity
def activity(id, activity): 
  data = {'content_id': id, 'activity': activity, 'user_id': st.session_state['user'], 'datetime': str(datetime.datetime.now())}
  # add to the session state
  st.session_state['activities'].append(data)
  # directly save the activities
  save_activities()

# set episode session state
def select_show(title):
  st.session_state['titles'] = title
  activity(title, 'Select title')

def tile_item(column, item):
  with column:
    st.button('▶️', key=random(), on_click=select_show, args=(item['titles'], ))
    st.image(item['pictures'], use_column_width='always')
    st.caption(item['titles'])
    
    
def recommendations(df):

  # check the number of items
  nbr_items = df.shape[0]
  cols=6

  if nbr_items != 0:    

    # create columns with the corresponding number of items
    columns = st.columns(nbr_items)

    # convert df rows to dict lists
    items = df.to_dict(orient='records')

    # apply tile_item to each column-item tuple (created with python 'zip')
    any(tile_item(x[0], x[1]) for x in zip(columns, items))