import streamlit as st
import pandas as pd
import random
from SessionState import SessionState
from PIL import Image
from bokeh.plotting import figure
from bokeh.models import FreehandDrawTool

lion_image = Image.open('lion.jpg')
monkey_image = Image.open('home.jpg')
df = pd.read_csv('words.csv')
categories = df.columns.to_list()
words = []

with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
 

for category in categories:
    cat_words = df[category]
    card_word_tuples = [(category,w) for w in cat_words]
    words.extend(card_word_tuples)

def html_markdown(header, **kwargs):
    text = kwargs['text'] 
    if 'color' in kwargs:
        color= kwargs['color']
    else:
        color= 'maroon'

    if 'sidebar' in kwargs:
        sidebar = kwargs['sidebar']
    else:
        sidebar = False

    if 'center' in kwargs:
        center = kwargs['center']
    else:
        center = False

    if center:
        markdown_html = f"<{header} style='text-align: center; color: {color}'>{text}</{header}>"
    else:
        markdown_html = f"<{header} style='color: {color}'>{text}</{header}>"

    if sidebar:
        return st.sidebar.markdown(markdown_html, unsafe_allow_html=True)
    else:    
        return st.markdown(markdown_html, unsafe_allow_html=True)

def title(**kwargs):
    return html_markdown('h1', **kwargs)

def sub_title(**kwargs):
    return html_markdown('h2', **kwargs)

def card(category, word, color='maroon'):
    return st.markdown(f'<h3 style="text-align: center; border:4px; color: {color}; border-style:solid; border-color:#800000; padding: 1em;"> {category} <br /> <br /> {word} </h3>', unsafe_allow_html=True)
    
def show_word(category, word, player):
    sub_title(text=f'Player {player}')
    card(category, word, 'red')
 
title(text='Fake Artist', sidebar=True, center=True)
st.sidebar.image(monkey_image, width = 150, use_column_width=False)
 
N_PLAYERS = st.sidebar.number_input('No. of players : ', min_value=3, max_value=12)    
 
index = random.randint(0, len(words)-1)
display_tuple = words[index]
display_category = display_tuple[0]
display_word = display_tuple[1]
fake_index = random.randint(0, N_PLAYERS-1)

# placeholder.empty()

ss = SessionState.get(game=0, counter=0, display_category=display_category, display_word=display_word, fake_index=fake_index, show_card = True, round_over= False, end_game=False)

if st.sidebar.button("New Game"):
    ss.game += 1
    ss.counter = 0
    ss.display_category = display_category
    ss.display_word = display_word
    ss.fake_index = fake_index
    ss.show_card = True
    ss.round_over = False
    ss.end_game = False

message  = sub_title(text=f"It's your turn player No. {ss.counter + 1}\n\n") 
next_player_button = st.button('Next')   

if next_player_button:
    if not ss.round_over:
        if ss.show_card:
            if ss.counter == ss.fake_index:
                show_word(ss.display_category, 'Fake', ss.counter+1)
            else:    
                show_word(ss.display_category, ss.display_word, ss.counter+1)

            ss.counter +=1
    else:
        message.empty()
        if ss.end_game:
            sub_title(text=f'Player {ss.fake_index + 1} is Fake Artist')
        else:    
            message = sub_title(text='Now Draw...')
            # stop_image = st.image(lion_image, use_column_width=True)
            p = figure(x_range=(0, 10), y_range=(0, 10), width=600, height=700)

            renderer = p.multi_line([[1, 1]], [[1, 1]], line_width=4, alpha=0.4, color='red')

            draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=99999)
            p.add_tools(draw_tool)
            p.toolbar.active_drag = draw_tool

            st.bokeh_chart(p)

        ss.end_game=True
        

    ss.show_card = not ss.show_card 

    if ss.counter >= N_PLAYERS:
        ss.round_over = True
