import streamlit as st
#import os
#import openai
from langchain_community.llms import GPT4All


st.title("Vegan maaltijplangenerator")


def generate_meal_plan(gender= 'vrouw', age = 34, height = 163, weight = 75, activity_level = 'gemiddeld', goal = '0.5 kilo per week afvallen'):
    try:
        # Initialiseer het GPT-4-model
        model = GPT4All(
            model="mistral-7b-instruct-v0.1.Q4_0.gguf",
            max_tokens=300,
            n_threads=4,
            temp=0.3,
            top_p=0.2,
            top_k=40,
            n_batch=8,
            seed=100,
            allow_download=False,
            verbose=True
        )

        # Definieer de vraag voor het maaltijdplan
        question = f"Stel een plantaardig dagelijks maaltijdplan op dat voldoet aan de voedingsbehoeften van een {gender} van {age} jaar, {weight} kilo, {height} cm, met een activiteitsniveau van {activity_level} en als doel {goal}. De totale voedingswaarden stemmen overeen met de voedingsbehoeften. Het plan is gedetailleerd en bevat minstens ontbijt, lunch, snacks en diner en eventueel dessert."
        

        return (model.generate([question]))

    except Exception as e:
        return f"Een fout is opgetreden: {str(e)}"

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

# Knop om maaltijdplan te genereren
if st.button('Genereer Maaltijdplan'):
    # Genereer maaltijdplan op basis van gebruikersinvoer
    st.header('Jouw Maaltijdplan')
    st.write(generate_meal_plan(
        gender, age, height, weight, activity_level, goal))

   




