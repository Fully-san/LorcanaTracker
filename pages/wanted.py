import streamlit as st

#region Settings

st.set_page_config(
    page_title = 'Lorcana Tracker',
    page_icon = '📖',
    layout = 'centered',
    initial_sidebar_state = 'expanded')

#endregion

from helper import *

init()

drawSidebard()

drawMainContent(st.session_state.currentCards.loc[st.session_state.currentCards.ownedNumber == 0])