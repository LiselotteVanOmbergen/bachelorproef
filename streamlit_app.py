import streamlit as st
import os
import openai
import json
from rag_motivation import generate_motivation
from rag_dietary_requirements import generate_dietary_requirements
from rag_mealplan import generate_mealplan
from dict_to_text import dict_to_text
from shopping_list import generate_shopping_list_dict

st.set_page_config(layout="wide")
openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

st.title(":seedling: Vegan maaltijdplangenerator :seedling:")

col1, col2 = st.columns(2)


  

with col1:
    st.write(generate_motivation())

    gender = st.selectbox('Geslacht', ['Vrouw', 'Man', 'Non-binair persoon'])
    age = st.number_input('Leeftijd', min_value=1,
                        max_value=100, value=30, step=1)
    height = st.number_input('Lengte (cm)', min_value=1,
                            max_value=220, value=170, step=1)
    weight = st.number_input('Gewicht (kg)', min_value=1,
                            max_value=500, value=70, step=1)
    activity_level = st.selectbox('Activiteitsniveau', [
        'Sedentair', 'Licht actief', 'Gemiddeld actief', 'Zeer actief'])
    goal = st.selectbox('Doel', ['0.5 kilo per week aankomen', '1 kilo per week aankomen',
                                '0.5 kilo per week afvallen', '1 kilo per week afvallen', 'Onderhouden'])

# Invoervelden voor ontbijt
with col2:
    st.subheader("Ontbijt")
    ingredient_ontbijt = st.text_input("Ingrediënt of gerecht voor ontbijt")
    # Voeg meer ingrediëntenvelden toe zoals hierboven indien nodig voor ontbijt

    # Invoervelden voor lunch
    st.subheader("Lunch")
    ingredient_lunch = st.text_input("Ingrediënt of gerecht voor lunch")
    # Voeg meer ingrediëntenvelden toe zoals hierboven indien nodig voor lunch

    # Invoervelden voor diner
    st.subheader("Diner")
    ingredient_diner = st.text_input("Ingrediënt of gerecht voor diner")
    user_requirements = f"{ingredient_ontbijt} voor ontbijt, {ingredient_lunch} voor lunch en {ingredient_diner} voor diner"


if st.button('Genereer maaltijdplan'):
            st.header('	:carrot: Jouw maaltijdplan')
            mealplan = generate_mealplan(generate_dietary_requirements(gender, age, height, weight,  activity_level, goal), user_requirements)
            st.text(dict_to_text(json.loads(mealplan)))
            st.download_button("Download maaltijdplan", mealplan)
            

            st.header('	:shopping_trolley: Boodschappenlijst')
            boodschappenlijst = dict_to_text(generate_shopping_list_dict(json.loads(mealplan)))
            st.text(boodschappenlijst)
            st.download_button("Download boodschappenlijst", boodschappenlijst)
            