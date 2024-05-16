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


cola, colb = st.columns(2)

if 'motivation_content' not in st.session_state:
    st.session_state.motivation_content = generate_motivation()

import streamlit as st

with cola.container(height=200):
    st.write(st.session_state.motivation_content)
    st.markdown('<span style="color:green">f"{st.session_state.motivation_content})"</span>', unsafe_allow_html=True)

with colb.container(height=200):
    st.write("Vergeet niet om dagelijks een vitamine B12-supplement in te nemen, aangezien deze vitamine van nature alleen voorkomt in dierlijke producten. Naast vitamine B12, kunnen ook andere supplementen worden overwogen om ervoor te zorgen dat je alle essentiële voedingsstoffen binnenkrijgt. Denk hierbij aan vitamine D, omega-3 vetzuren, calcium en ijzer.")

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {
        'gender': None,
        'age': 30,
        'height': 170,
        'weight': 70,
        'activity_level': 'Gemiddeld actief',
        'goal': 'Onderhouden',
        'ingredient_ontbijt': '',
        'ingredient_lunch': '',
        'ingredient_diner': '',
        'ingredient_snack':'',
        'ingredient_dessert':''
    }

if not st.session_state.form_submitted:
    with st.form(key='user_input_form'):
        col1, col2 = st.columns(2)    

        with col1:
            st.write("Vul hieronder je persoonlijke gegevens in.")
            st.session_state.user_inputs['gender'] = st.selectbox('Geslacht', ['Vrouw', 'Man', 'Non-binair persoon'], index=['Vrouw', 'Man', 'Non-binair persoon'].index(st.session_state.user_inputs['gender']) if st.session_state.user_inputs['gender'] else None)
            st.session_state.user_inputs['age'] = st.number_input('Leeftijd', min_value=1, max_value=100, value=st.session_state.user_inputs['age'], step=1)
            st.session_state.user_inputs['height'] = st.number_input('Lengte (cm)', min_value=1, max_value=220, value=st.session_state.user_inputs['height'], step=1)
            st.session_state.user_inputs['weight'] = st.number_input('Gewicht (kg)', min_value=1, max_value=500, value=st.session_state.user_inputs['weight'], step=1)
            st.session_state.user_inputs['activity_level'] = st.selectbox('Activiteitsniveau', ['Sedentair', 'Licht actief', 'Gemiddeld actief', 'Zeer actief'], index=['Sedentair', 'Licht actief', 'Gemiddeld actief', 'Zeer actief'].index(st.session_state.user_inputs['activity_level']))
            st.session_state.user_inputs['goal'] = st.selectbox('Doel', ['0.5 kilo per week aankomen', '1 kilo per week aankomen', '0.5 kilo per week afvallen', '1 kilo per week afvallen', 'Onderhouden'], index=['0.5 kilo per week aankomen', '1 kilo per week aankomen', '0.5 kilo per week afvallen', '1 kilo per week afvallen', 'Onderhouden'].index(st.session_state.user_inputs['goal']))

        
        with col2:
            st.write("Hieronder kan je specifieke ingrediënten of gerechten invullen voor een bepaalde maaltijd. Dit is optioneel: je kan dit ook leeglaten of slechts gedeeltelijk invullen.")
            st.subheader(":pancakes: Ontbijt")
            st.session_state.user_inputs['ingredient_ontbijt'] = st.text_input("Ingrediënt of gerecht voor ontbijt", value=st.session_state.user_inputs['ingredient_ontbijt'])
            
            st.subheader(":sandwich: Lunch")
            st.session_state.user_inputs['ingredient_lunch'] = st.text_input("Ingrediënt of gerecht voor lunch", value=st.session_state.user_inputs['ingredient_lunch'])
            

            st.subheader(":spaghetti: Diner")
            st.session_state.user_inputs['ingredient_diner'] = st.text_input("Ingrediënt of gerecht voor diner", value=st.session_state.user_inputs['ingredient_diner'])

            st.subheader(":cookie: Snack")
            st.session_state.user_inputs['ingredient_snack'] = st.text_input("Ingrediënt of gerecht voor snack", value=st.session_state.user_inputs['ingredient_snack'])

            st.subheader(":ice_cream: Dessert")
            st.session_state.user_inputs['ingredient_dessert'] = st.text_input("Ingrediënt of gerecht voor dessert", value=st.session_state.user_inputs['ingredient_dessert'])
        
            submitted = st.form_submit_button('Genereer maaltijdplan')

    if submitted:
        st.session_state.form_submitted = True

if st.session_state.form_submitted:
    user_requirements = f"{st.session_state.user_inputs['ingredient_ontbijt']} voor ontbijt, {st.session_state.user_inputs['ingredient_lunch']} voor lunch, {st.session_state.user_inputs['ingredient_diner']} voor diner, {st.session_state.user_inputs['ingredient_snack']} voor snack en {st.session_state.user_inputs['ingredient_dessert']} voor dessert"
    col1, col2 = st.columns([0.7, 0.3])
    
    with col1:
        st.header(' :carrot: Jouw maaltijdplan')
        mealplan = generate_mealplan(generate_dietary_requirements(st.session_state.user_inputs['gender'], st.session_state.user_inputs['age'], st.session_state.user_inputs[
                                    'height'], st.session_state.user_inputs['weight'],  st.session_state.user_inputs['activity_level'], st.session_state.user_inputs['goal']), user_requirements)
        st.text(dict_to_text(json.loads(mealplan)))
        st.download_button("Download maaltijdplan", mealplan)
    with col2:
        st.header(' :shopping_trolley: Boodschappenlijst')
        boodschappenlijst = dict_to_text(
            generate_shopping_list_dict(json.loads(mealplan)))
        st.text(boodschappenlijst)
        st.download_button("Download boodschappenlijst", boodschappenlijst)

