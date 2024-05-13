import streamlit as st
import os
import openai

from rag_motivation import generate_motivation
from rag_mealplan import generate_mealplan
from dict_to_text import dict_to_text
from shopping_list import generate_shopping_list_dict
from shopping_list import print_shopping_list

st.set_page_config(layout="wide")
openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))


st.title("Vegan maaltijdplangenerator")

col1, col2 = st.columns(2)

    # Maaltijdplan genereren en weergeven in de eerste kolom
with col1:
        
        gender = st.selectbox('Geslacht', ['Man', 'Vrouw', 'Non-binair persoon'])
        age = st.number_input('Leeftijd', min_value=1, max_value=100, value=30, step=1)
        height = st.number_input('Lengte (cm)', min_value=1,
                         max_value=220, value=170, step=1)
        weight = st.number_input('Gewicht (kg)', min_value=1,
                         max_value=500, value=70, step=1)
        activity_level = st.selectbox('Activiteitsniveau', [
                              'Sedentair', 'Licht actief', 'Gemiddeld actief', 'Zeer actief'])
        goal = st.selectbox('Doel', ['0.5 kilo per week aankomen', '1 kilo per week aankomen',
                    '0.5 kilo per week afvallen', '1 kilo per week afvallen', 'Onderhouden'])

        st.subheader('Jouw Maaltijdplan')
        
    # Knop om maaltijdplan te genereren
        if st.button('Genereer Maaltijdplan'):
            st.header('Jouw Maaltijdplan')
            mealplan =(generate_mealplan(gender= 'vrouw', age = 34, height = 163, weight = 75, activity_level = 'gemiddeld', goal = '0.5 kilo per week afvallen'))
            st.write(dict_to_text(mealplan))
            # Genereer maaltijdplan op basis van gebruikersinvoer
            st.header('Boodschappenlijst')
            st.write(print_shopping_list(generate_shopping_list_dict(mealplan)))
    # Motivatie genereren en weergeven in de tweede kolom
with col2:
        st.subheader('')
        st.write(generate_motivation())
        
   
