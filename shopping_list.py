from dict_to_text import dict_to_text


def generate_shopping_list_dict(meal_plan):
    shopping_list = {}

    for meal, data in meal_plan["maaltijdplan"].items():
        ingredients = data["ingrediënten"]

        for ingredient, quantity in ingredients.items():
            if ingredient in shopping_list:
                shopping_list[ingredient] = f"{shopping_list[ingredient]} + {quantity}"
            else:
                shopping_list[ingredient] = quantity

    return dict(sorted(shopping_list.items()))


def print_shopping_list(shopping_list):
    return dict_to_text(shopping_list)
