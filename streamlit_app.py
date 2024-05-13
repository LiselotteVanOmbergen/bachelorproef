import streamlit as st
import os
import openai
import json
from rag_motivation import generate_motivation
from rag_mealplan import generate_mealplan
from dict_to_text import dict_to_text
from shopping_list import generate_shopping_list_dict
from shopping_list import print_shopping_list

st.set_page_config(layout="wide")
openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))


st.title(":seedling: Vegan maaltijdplangenerator :seedling:")



col1, col2 = st.columns(2)
    # Maaltijdplan genereren en weergeven in de eerste kolom
with col2:
    #st.subheader(':earth_africa:')
    st.write(generate_motivation())

with col1:
         # Motivatie genereren en weergeven in de tweede kolom
        st.subheader(':earth_africa:')
        st.write(generate_motivation())
        if st.button("Genereer maaltijdplan"):
            gender = st.selectbox('Geslacht', ['Vrouw', 'Man', 'Non-binair persoon'])
            age = st.number_input('Leeftijd', min_value=1, max_value=100, value=30, step=1)
            height = st.number_input('Lengte (cm)', min_value=1,
                         max_value=220, value=170, step=1)
            weight = st.number_input('Gewicht (kg)', min_value=1,
                         max_value=500, value=70, step=1)
            activity_level = st.selectbox('Activiteitsniveau', [
                              'Sedentair', 'Licht actief', 'Gemiddeld actief', 'Zeer actief'])
            goal = st.selectbox('Doel', ['0.5 kilo per week aankomen', '1 kilo per week aankomen',
                    '0.5 kilo per week afvallen', '1 kilo per week afvallen', 'Onderhouden'])
        
    # Knop om maaltijdplan te genereren
            if st.button('Genereer maaltijdplan'):
                st.header('Jouw maaltijdplan')
                mealplan =(generate_mealplan(gender, age, height , weight, activity_level, goal))
                st.text(dict_to_text(json.loads(mealplan)))
                st.download_button("Download maaltijdplan", mealplan)
            # Genereer maaltijdplan op basis van gebruikersinvoer
                with col2:
                    st.header('Boodschappenlijst')
                    boodschappenlijst = dict_to_text(generate_shopping_list_dict(json.loads(mealplan)))
                    st.text(boodschappenlijst)
                    st.download_button("Download boodschappenlijst", boodschappenlijst)
   

        
   
