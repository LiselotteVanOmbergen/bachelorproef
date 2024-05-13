import streamlit as st
import os
import openai

from rag_motivation import generate_motivation
from rag_mealplan import generate_mealplan
st.set_page_config(layout="wide")
openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))


st.title("Vegan maaltijdplangenerator")


def generate_meal_plan(gender= 'vrouw', age = 34, height = 163, weight = 75, activity_level = 'gemiddeld', goal = '0.5 kilo per week afvallen'):
    try:
        user_template = f"Stel een plantaardig dagelijks maaltijdplan op dat voldoet aan de voedingsbehoeften van een {gender} van {age} jaar, {weight} kilo, {height} cm, met een {activity_level} activiteitsniveau en als doel {goal}. De totale voedingswaarden stemmen overeen met de voedingsbehoeften. Het plan is gedetailleerd en bevat minstens ontbijt, lunch, snacks en diner en eventueel dessert."

        completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "Je bent een voedingscoach die plantaardige maaltijdplannen opstelt."},
        {"role": "user", "content": user_template}
    ]
)
        

        

   

        return completion.choices[0].message.content.replace('\\n', '\n')

    except Exception as e:
        return f"Een fout is opgetreden: {str(e)}"


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
        st.json(generate_mealplan())
"""      # Knop om maaltijdplan te genereren
        if st.button('Genereer Maaltijdplan'):
            # Genereer maaltijdplan op basis van gebruikersinvoer
            st.header('Jouw Maaltijdplan')
            # st.write(generate_meal_plan(gender, age, height, weight, activity_level, goal))
 """
    # Motivatie genereren en weergeven in de tweede kolom
with col2:
        st.subheader('')
        st.write(generate_motivation())

   
