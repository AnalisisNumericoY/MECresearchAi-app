import streamlit as st
from PIL import Image
img = Image.open('logioto77.jpg')
#st.beta_set_page_config(page_title='MEC ia', page_icon=img) #page_icon=':smiley:'

import streamlit as st

st.set_page_config(
    page_title="medicina computacional llm",
    page_icon=img,
    layout="wide")


#st.title("🎈 large language model ")
st.write(
    "inspirado por Medicina Computacional [https://www.medicinacomputacional.com/](https://www.medicinacomputacional.com/)."
)
