import streamlit as st
import pandas as pd
import random
import SessionState
from PIL import Image

lion_image = Image.open('lion.jpg')
monkey_image = Image.open('home.jpg')
N_PLAYERS = 6

df = pd.read_csv('words.csv')

categories = df.columns.to_list()
words = []

for category in categories:
    cat_words = df[category]
    card_word_tuples = [(category,w) for w in cat_words]
    words.extend(card_word_tuples)

def title(text, color='maroon'):
    return st.markdown(f"<h2 style='text-align: center; color: {color};'>{text}</h2>", unsafe_allow_html=True)

def sub_title(text, color='maroon'):
    return st.markdown(f"<h3 style='text-align: center; color: {color};'>{text}</h3>", unsafe_allow_html=True)

def card(category, word, color='maroon'):
    return st.markdown(f'<h3 style="text-align: center; border:4px; color: {color}; border-style:solid; border-color:#800000; padding: 1em;"> {category} <br /> <br /> {word} </h3>', unsafe_allow_html=True)
    

def show_word(category, word, player):
    sub_title(f'Player {player}')
    card(category, word, 'red')

col1, col2 = st.beta_columns([3,1])
with col1:
    title('FAKE ARTIST')
with col2:
    st.image(monkey_image,width = None, use_column_width=False)

index = random.randint(0, len(words)-1)
display_tuple = words[index]
display_category = display_tuple[0]
display_word = display_tuple[1]
fake_index = random.randint(0, N_PLAYERS-1)

ss = SessionState.get(counter=0, display_category=display_category, display_word=display_word, fake_index=fake_index, show_card = True)

next_title  = title('Hand over the device to the first Player..') 
next_player_button = st.button('Next')   
 
if next_player_button:
    next_title.empty()
    if ss.show_card:
        if ss.counter == ss.fake_index:
            show_word(ss.display_category, 'Fake', ss.counter+1)
        else:    
            show_word(ss.display_category, ss.display_word, ss.counter+1)

        ss.counter +=1

        if ss.counter >= N_PLAYERS:
            st.header('Now Draw...')
            st.image(lion_image, use_column_width=True)
            st.subheader('Refresh page for new round')

    # else:
    #     next_title  = title('Hand over the device to next Player..')

    ss.show_card = not ss.show_card 
