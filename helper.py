import streamlit as st
import pandas as pd

#region Variables & Session State

pageTitle = 'Lorcana Tracker'
pageIcon = '📖'
pageLayout = 'centered'
sidebarState = 'expanded'

url = 'Data/cards.csv'

def init():
    if 'allCards' not in st.session_state:
        st.session_state.allCards = pd.read_csv(url)

    if 'currentCards' not in st.session_state:
        st.session_state.currentCards = st.session_state.allCards

    if 'name' not in st.session_state:
        st.session_state.name = ''

    if 'sets' not in st.session_state:
        st.session_state.sets = []

    if 'colors' not in st.session_state:
        st.session_state.colors = []

    if 'types' not in st.session_state:
        st.session_state.types = []

    if 'costMin' not in st.session_state:
        st.session_state.costMin = st.session_state.allCards.Cost.min()

    if 'costMax' not in st.session_state:
        st.session_state.costMax = st.session_state.allCards.Cost.max()

    if 'willpowerMin' not in st.session_state:
        st.session_state.willpowerMin = st.session_state.allCards.Willpower.min()

    if 'willpowerMax' not in st.session_state:
        st.session_state.willpowerMax = st.session_state.allCards.Willpower.max()

    if 'strengthMin' not in st.session_state:
        st.session_state.strengthMin = st.session_state.allCards.Strength.min()

    if 'strengthMax' not in st.session_state:
        st.session_state.strengthMax = st.session_state.allCards.Strength.max()

    if 'loreMin' not in st.session_state:
        st.session_state.loreMin = st.session_state.allCards.LoreValue.min()

    if 'loreMax' not in st.session_state:
        st.session_state.loreMax = st.session_state.allCards.LoreValue.max()

    if 'wanted' not in st.session_state:
        st.session_state.wanted = False

#endregion


#region Fonctions


# Fonction qui sauvegarde la collection
def saveCollection(cardId):
    st.session_state.allCards.loc[st.session_state.allCards.Id == cardId, 'OwnedNumber'] = st.session_state[cardId]
    st.session_state.currentCards.loc[st.session_state.currentCards.Id == cardId, 'OwnedNumber'] = st.session_state[cardId]

    st.session_state.allCards.to_csv(url, index=False)

    st.toast('Saving performed', icon='💾')

# Fonction de recherche
def search():
    st.session_state.currentCards = st.session_state.allCards.copy()

    if st.session_state.wanted:
        st.session_state.currentCards = st.session_state.currentCards.loc[st.session_state.currentCards.OwnedNumber == 0]

    if st.session_state.name:
        st.session_state.currentCards = st.session_state.currentCards.loc[st.session_state.currentCards.Name.str.lower().str.contains(st.session_state.name.lower(), regex=False)]

    if st.session_state.sets:
        st.session_state.currentCards = st.session_state.currentCards.loc[st.session_state.currentCards.SetName.isin(st.session_state.sets)]

    if st.session_state.colors:
        # st.session_state.currentCards = st.session_state.currentCards.loc[st.session_state.currentCards.Color.isin(st.session_state.colors)]
        st.session_state.currentCards = st.session_state.currentCards.loc[st.session_state.currentCards.Color.str.contains('|'.join(st.session_state.colors))]

    if st.session_state.types:
        st.session_state.currentCards = st.session_state.currentCards.loc[st.session_state.currentCards.Type.isin(st.session_state.types)]

    st.session_state.costMin = st.session_state.cost[0]
    st.session_state.costMax = st.session_state.cost[1]
    st.session_state.willpowerMin = st.session_state.willpower[0]
    st.session_state.willpowerMax = st.session_state.willpower[1]
    st.session_state.strengthMin = st.session_state.strength[0]
    st.session_state.strengthMax = st.session_state.strength[1]
    st.session_state.loreMin = st.session_state.lore[0]
    st.session_state.loreMax = st.session_state.lore[1]

    st.session_state.currentCards = st.session_state.currentCards.loc[(st.session_state.currentCards.Cost >= st.session_state.costMin) & (st.session_state.currentCards.Cost <= st.session_state.costMax)]
    st.session_state.currentCards = st.session_state.currentCards.loc[(st.session_state.currentCards.Willpower.isnull()) | (st.session_state.currentCards.Willpower >= st.session_state.willpowerMin) & (st.session_state.currentCards.Willpower <= st.session_state.willpowerMax)]
    st.session_state.currentCards = st.session_state.currentCards.loc[(st.session_state.currentCards.Strength.isnull()) | (st.session_state.currentCards.Strength >= st.session_state.strengthMin) & (st.session_state.currentCards.Strength <= st.session_state.strengthMax)]
    st.session_state.currentCards = st.session_state.currentCards.loc[(st.session_state.currentCards.LoreValue.isnull()) | (st.session_state.currentCards.LoreValue >= st.session_state.loreMin) & (st.session_state.currentCards.LoreValue <= st.session_state.loreMax)]

# Fonction pour afficher la sidebard
def drawSidebard():
    with st.sidebar:
        # Système de recherche
        with st.form('search', border = True):
            col1, col2, col3 = st.columns(3)
            with col2:
                st.subheader('Filters')

            st.text_input('Name : ', key='name')
            st.multiselect('Sets :', options = st.session_state.allCards.SetName.unique(), key='sets')
            st.multiselect('Colors :', options = st.session_state.allCards.Color.unique(), key='colors')
            st.multiselect('Types :', options = st.session_state.allCards.Type.unique(), key='types')
            st.select_slider('Cost :', options = sorted(st.session_state.allCards.Cost.unique()), value=[st.session_state.costMin, st.session_state.costMax], key='cost')
            st.select_slider('Willpower :', options = sorted(st.session_state.allCards.Willpower.dropna().unique()), value=[st.session_state.willpowerMin, st.session_state.willpowerMax], key='willpower')
            st.select_slider('Strength :', options = sorted(st.session_state.allCards.Strength.dropna().unique()), value=[st.session_state.strengthMin, st.session_state.strengthMax], key='strength')
            st.select_slider('Lore value :', options = sorted(st.session_state.allCards.LoreValue.dropna().unique()), value=[st.session_state.loreMin, st.session_state.loreMax], key='lore')
            st.toggle('All/Only wanted', key='wanted')
            st.form_submit_button('Search', use_container_width = True, on_click=search)

# def switchPage(key):
#     selection = st.session_state[key]
#     if selection == 'All cards':
#         st.switch_page('home.py')
#     if selection == 'My collection':
#         st.write(selection)
#         st.switch_page('pages/collection.py')
#     if selection == 'Wanted':
#         st.switch_page('pages/wanted.py')

# Fonction pour afficher le menu
def drawMenu():
    with st.container(border = True):
        col1, col2, col3 = st.columns(3)

        if col1.button('All cards', use_container_width = True, key='home'):
            st.switch_page('home.py')
        if col2.button('My collection', use_container_width = True, key='collection'):
            st.switch_page('pages/collection.py')
        if col3.button('Wanted', use_container_width = True, key='wantedCards'):
            st.switch_page('pages/wanted.py')
    # option_menu(None, ['All cards', 'My collection', 'Wanted'],
    #                     icons=['house', "list-task", 'gear'],
    #                     on_change=st.switch_page('pages/wanted.py'), key='menu', orientation="horizontal")    

#Fonction pour afficher le contenu principal
def drawMainContent(cards, allPage = False):
    st.image('Data/logo.png', use_container_width=True)

    drawMenu()

    col1, col2, col3 = st.columns(3)

    for id, card in cards.reset_index(drop=True).iterrows():
        if id % 3 == 0:
            drawComponent(col1, card, allPage)

        if id % 3 == 1:
            drawComponent(col2, card, allPage)

        if id % 3 == 2:
            drawComponent(col3, card, allPage)

# Fonction pour afficher nos cartes
def drawComponent(col, card, allPage = False):
    with col:
        st.image(card.Image, use_container_width = True)

        if allPage:
            st.number_input(label=card.Name, value=card.OwnedNumber, label_visibility='collapsed', step=1, min_value=0, key=card.Id, on_change=saveCollection, args=(card.Id,))
            st.divider()


#endregion