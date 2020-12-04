import streamlit as st
import pandas as pd
import random
import SessionState
from PIL import Image

image = Image.open('lion.jpg')

N_PLAYERS = 6

st.header('FAKE ARTIST')

df = pd.read_excel('words.xlsx')

categories = df.columns.to_list()
words = []

for category in categories:
    cat_words = df[category]
    card_word_tuples = [(category,w) for w in cat_words]
    words.extend(card_word_tuples)


def show_word(category, word, player):
    st.subheader(f'Player No. {player}')
    st.subheader((category, word))


index = random.randint(0, len(words)-1)
display_tuple = words[index]
display_category = display_tuple[0]
display_word = display_tuple[1]
fake_index = random.randint(0, N_PLAYERS-1)

ss = SessionState.get(counter=0, display_category=display_category, display_word=display_word, fake_index=fake_index)

next_word_button_enabled = True
next_word_button = st.button('Next Word')
player_1 = st.header('Hand over to Player 1 in this round..')
 
if next_word_button and next_word_button_enabled:
    player_1.empty()

    if ss.counter == ss.fake_index:
        show_word(ss.display_category, 'fake', ss.counter+1)
    else:    
        show_word(ss.display_category, ss.display_word, ss.counter+1)

    ss.counter +=1

    if ss.counter >= N_PLAYERS:
        next_word_button_enabled = False
        st.header('Now Draw...')
        st.image(image, use_column_width=True)
        st.subheader('Refresh page for new round')
