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

def setup_user_inputs():
    return {
        'gender': None,
        'age': 30,
        'height': 170,
        'weight': 70,
        'activity_level': 'Gemiddeld actief',
        'goal': 'Onderhouden',
        'ingredient_ontbijt': '',
        'ingredient_lunch': '',
        'ingredient_diner': '',
        'ingredient_snack': '',
        'ingredient_dessert': ''
    }

def setup_user_form():
    st.write("Vul hieronder je persoonlijke gegevens in.")
    user_inputs = st.session_state.user_inputs
    user_inputs['gender'] = st.selectbox('Geslacht', ['Vrouw', 'Man', 'Non-binair persoon'], index=['Vrouw', 'Man', 'Non-binair persoon'].index(user_inputs['gender']) if user_inputs['gender'] else None)
    user_inputs['age'] = st.number_input('Leeftijd', min_value=1, max_value=100, value=user_inputs['age'], step=1)
    user_inputs['height'] = st.number_input('Lengte (cm)', min_value=1, max_value=220, value=user_inputs['height'], step=1)
    user_inputs['weight'] = st.number_input('Gewicht (kg)', min_value=1, max_value=500, value=user_inputs['weight'], step=1)
    user_inputs['activity_level'] = st.selectbox('Activiteitsniveau', ['Sedentair', 'Licht actief', 'Gemiddeld actief', 'Zeer actief'], index=['Sedentair', 'Licht actief', 'Gemiddeld actief', 'Zeer actief'].index(user_inputs['activity_level']))
    user_inputs['goal'] = st.selectbox('Doel', ['0.5 kilo per week aankomen', '1 kilo per week aankomen', '0.5 kilo per week afvallen', '1 kilo per week afvallen', 'Onderhouden'], index=['0.5 kilo per week aankomen', '1 kilo per week aankomen', '0.5 kilo per week afvallen', '1 kilo per week afvallen', 'Onderhouden'].index(user_inputs['goal']))

    st.write("Vul hieronder specifiek gewenste ingrediënten of gerechten in voor een bepaalde maaltijd. Dit is optioneel: je kan dit ook oningevuld laten of slechts gedeeltelijk invullen.")
    st.subheader(":pancakes: Ontbijt")
    user_inputs['ingredient_ontbijt'] = st.text_input("Ingrediënt of gerecht voor ontbijt", value=user_inputs['ingredient_ontbijt'])

    st.subheader(":sandwich: Lunch")
    user_inputs['ingredient_lunch'] = st.text_input("Ingrediënt of gerecht voor lunch", value=user_inputs['ingredient_lunch'])

    st.subheader(":spaghetti: Diner")
    user_inputs['ingredient_diner'] = st.text_input("Ingrediënt of gerecht voor diner", value=user_inputs['ingredient_diner'])

    st.subheader(":cookie: Snack")
    user_inputs['ingredient_snack'] = st.text_input("Ingrediënt of gerecht voor snack", value=user_inputs['ingredient_snack'])

    st.subheader(":ice_cream: Dessert")
    user_inputs['ingredient_dessert'] = st.text_input("Ingrediënt of gerecht voor dessert", value=user_inputs['ingredient_dessert'])

    return user_inputs

def generate_meal_plan(user_inputs):
    user_requirements = f"{user_inputs['ingredient_ontbijt']} voor ontbijt, {user_inputs['ingredient_lunch']} voor lunch, {user_inputs['ingredient_diner']} voor diner, {user_inputs['ingredient_snack']} voor snack en {user_inputs['ingredient_dessert']} voor dessert"
    dietary_requirements = generate_dietary_requirements(user_inputs['gender'], user_inputs['age'], user_inputs['height'], user_inputs['weight'], user_inputs['activity_level'], user_inputs['goal'])
    mealplan = generate_mealplan(dietary_requirements, user_requirements)
    return json.loads(mealplan)

def main():
    st.title(":seedling: Veg:green[AI]n maaltijdplangenerator :seedling:")
    motivation_content = generate_motivation()
    st.write(motivation_content)

    if 'user_inputs' not in st.session_state:
        st.session_state.user_inputs = setup_user_inputs()

    if not st.session_state.form_submitted:
        st.session_state.user_inputs = setup_user_form()

    if st.form_submit_button('Genereer maaltijdplan'):
        st.session_state.form_submitted = True

    if st.session_state.form_submitted:
        user_inputs = st.session_state.user_inputs
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.header(' :carrot: Jouw maaltijdplan')
            mealplan = generate_meal_plan(user_inputs)
            st.text(dict_to_text(mealplan))
            st.download_button("Download maaltijdplan", dict_to_text(mealplan), file_name="maaltijdplan.txt")
        with col2:
            st.header(' :shopping_trolley: Boodschappenlijst')
            shopping_list = generate_shopping_list_dict(mealplan)
            st.text(dict_to_text(shopping_list))
            st.download_button("Download boodschappenlijst", dict_to_text(shopping_list), file_name="boodschappenlijst.txt")
        st.button("Nieuw maaltijdplan", on_click=main)

if __name__ == "__main__":
    main()
