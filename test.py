

from shopping_list import generate_shopping_list_dict
from shopping_list import print_shopping_list
from dict_to_text import dict_to_text

voorbeeld_maaltijdplan = {
    "maaltijdplan": {
        "ontbijt": {
            "gerecht": "Vegan avocado toast",
            "moeilijkheidsgraad": "Gemakkelijk",
            "kooktijd": "10 minuten",
            "benodigdheden": {
                "oven": 1,
                "broodrooster": 1
            },
            "ingrediënten": {
                "avocado": "1",
                "volkorenbrood": "2 sneetjes",
                "citroensap": "1 eetlepel",
                "chilivlokken": "naar smaak",
                "zout en peper": "naar smaak"
            },
            "bereidingswijze": "1. Rooster het volkorenbrood in de broodrooster.\n2. Prak de avocado en besprenkel met citroensap.\n3. Besmeer het geroosterde brood met de geprakte avocado.\n4. Breng op smaak met chilivlokken, zout en peper naar smaak."
        },
        "lunch": {
            "gerecht": "Quinoa bowl met geroosterde groenten",
            "moeilijkheidsgraad": "Gemiddeld",
            "kooktijd": "30 minuten",
            "benodigdheden": {
                "oven": 1,
                "kookpan": 1
            },
            "ingrediënten": {
                "quinoa": "1 kopje gekookt",
                "paprika": "1, in stukken",
                "courgette": "1, in plakjes",
                "cherrytomaten": "1 kopje, gehalveerd",
                "olijfolie": "2 eetlepels",
                "verse kruiden (bijv. basilicum en peterselie)": "naar smaak",
                "citroensap": "1 eetlepel",
                "zout en peper": "naar smaak"
            },
            "bereidingswijze": "1. Verwarm de oven voor op 200°C.\n2. Meng de gesneden paprika, courgette en cherrytomaten met olijfolie, zout en peper.\n3. Rooster de groenten in de voorverwarmde oven gedurende 20-25 minuten, tot ze gaar zijn.\n4. Kook de quinoa volgens de aanwijzingen op de verpakking.\n5. Meng de gekookte quinoa met de geroosterde groenten.\n6. Besprenkel met citroensap en garneer met verse kruiden."
        },
        "diner": {
            "gerecht": "Cauliflower 'steak' met romesco saus",
            "moeilijkheidsgraad": "Uitdagend",
            "kooktijd": "45 minuten",
            "benodigdheden": {
                "oven": 1,
                "grillpan": 1
            },
            "ingrediënten": {
                "bloemkool": "1 grote, in plakken",
                "olijfolie": "2 eetlepels",
                "amandelen": "½ kopje",
                "geroosterde rode paprika (uit pot)": "½ kopje",
                "knoflook": "2 teentjes",
                "citroensap": "1 eetlepel",
                "gerookt paprikapoeder": "1 theelepel",
                "zout en peper": "naar smaak"
            },
            "bereidingswijze": "1. Verwarm de oven voor op 200°C.\n2. Snijd de bloemkool in plakken van ongeveer 1 cm dik.\n3. Meng olijfolie, knoflook, gerookt paprikapoeder, zout en peper en bestrijk de bloemkoolplakken aan beide zijden met dit mengsel.\n4. Bak de bloemkoolplakken in een grillpan tot ze aan beide kanten goudbruin zijn.\n5. Plaats de gebakken bloemkoolplakken op een bakplaat en rooster ze gedurende 25-30 minuten in de voorverwarmde oven, tot ze zacht zijn.\n6. Maak ondertussen de romesco saus door amandelen, geroosterde rode paprika, knoflook, citroensap, zout en peper in een blender te mengen tot een gladde saus.\n7. Serveer de geroosterde bloemkoolplakken met de romesco saus."
        },
        "dessert": {
            "gerecht": "Chocolade avocado mousse",
            "moeilijkheidsgraad": "Gemakkelijk",
            "kooktijd": "10 minuten",
            "benodigdheden": {
                "blender": 1,
                "koelkast": 1
            },
            "ingrediënten": {
                "avocado": "1",
                "cacao poeder": "2 eetlepels",
                "agave siroop": "2 eetlepels",
                "vanille extract": "1 theelepel",
                "plantaardige melk": "¼ kopje",
                "zout": "een snufje"
            },
            "bereidingswijze": "1. Schep het vruchtvlees van de avocado in een blender.\n2. Voeg cacao poeder, agave siroop, vanille extract, plantaardige melk en een snufje zout toe.\n3. Blend tot een gladde mousse.\n4. Zet de mousse minstens een uur in de koelkast om op te stijven.\n5. Serveer gekoeld."
        },
        "snack": {
            "gerecht": "Geroosterde kikkererwten",
            "moeilijkheidsgraad": "Gemakkelijk",
            "kooktijd": "40 minuten",
            "benodigdheden": {
                "oven": 1,
                "bakplaat": 1
            },
            "ingrediënten": {
                "kikkererwten (uit blik, uitgelekt en afgespoeld)": "1 blikje",
                "olijfolie": "1 eetlepel",
                "paprikapoeder": "1 theelepel",
                "komijnpoeder": "1 theelepel",
                "knoflookpoeder": "½ theelepel",
                "zout en peper": "naar smaak"
            },
            "bereidingswijze": "1. Verwarm de oven voor op 200°C.\n2. Dep de kikkererwten droog met keukenpapier en verwijder eventuele losse velletjes.\n3. Meng de kikkererwten met olijfolie, paprikapoeder, komijnpoeder, knoflookpoeder, zout en peper.\n4. Verdeel de gekruide kikkererwten over een met bakpapier beklede bakplaat.\n5. Rooster de kikkererwten in de voorverwarmde oven gedurende 30-35 minuten, schud ze halverwege de baktijd om, tot ze knapperig en goudbruin zijn.\n6. Laat de geroosterde kikkererwten afkoelen voordat je ze serveert."
        }
    },
    "totaal_voedingswaarden": {
        "calorieën": "1510 kcal",
        "koolhydraten": "125g",
        "vetten": "79g",
        "eiwitten": "41g",
        "vezels": "36g",
        "ijzer": "10.3mg",
        "calcium": "150mg",
        "zink": "6.6mg"
    }
}

print("test2")
print(dict_to_text(voorbeeld_maaltijdplan))
print(print_shopping_list(generate_shopping_list_dict(voorbeeld_maaltijdplan)))


# JSON data
