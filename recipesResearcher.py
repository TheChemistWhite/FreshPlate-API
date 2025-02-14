import re
import spoonacular
from spoonacular.models.search_recipes_by_ingredients200_response_inner import SearchRecipesByIngredients200ResponseInner
from spoonacular.rest import ApiException
from pprint import pprint
import os
import json

# Defining the host is optional and defaults to https://api.spoonacular.com
# See configuration.py for a list of all supported configuration parameters.
configuration = spoonacular.Configuration(
    host = "https://api.spoonacular.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKeyScheme
configuration.api_key['apiKeyScheme'] = "YOUR_API_KEY"

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKeyScheme'] = 'Bearer'

def recipes_researcher(my_ingredients):
# Enter a context with an instance of the API client
    with spoonacular.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = spoonacular.RecipesApi(api_client)
        ingredients = str(my_ingredients) # str | A comma-separated list of ingredients that the recipes should contain.
        number = 1 # int | The maximum number of items to return (between 1 and 100). Defaults to 10. (optional) (default to 10)
        ranking = 1 # int | Whether to maximize used ingredients (1) or minimize missing ingredients (2) first. (optional)
        ignore_pantry = False # bool | Whether to ignore typical pantry items, such as water, salt, flour, etc. (optional) (default to False)
        include_nutrition = True # bool | Include nutrition data in the recipe information. Nutrition data is per serving. If you want the nutrition data for the entire recipe, just multiply by the number of servings. (optional) (default to False)
        add_wine_pairing = False # bool | Add a wine pairing to the recipe. (optional)
        add_taste_data = False # bool | Add taste data to the recipe. (optional)

        try:
            # Search Recipes by Ingredients
            print("The ingredients are: ", ingredients)
            api_response = api_instance.search_recipes_by_ingredients(ingredients, number=number, ranking=ranking, ignore_pantry=ignore_pantry)
            recipe_id = int(getattr(api_response[0], 'id'))
            print(api_response)
            recipe_information = api_instance.get_recipe_information(recipe_id, include_nutrition=include_nutrition, add_wine_pairing=add_wine_pairing, add_taste_data=add_taste_data)
            print("The response of RecipesApi->search_recipes_by_ingredients:\n")
            pprint(recipe_information)
            recipe_data = [{
                'title': recipe_information.title,
                'image': recipe.image,
                'missed_ingredients': [{'name': ing.name, 'amount': ing.amount, 'unit': ing.unit} 
                                    for ing in recipe.missed_ingredients],
                'used_ingredients': [{'name': ing.name, 'amount': ing.amount, 'unit': ing.unit} 
                                    for ing in recipe.used_ingredients]
            } for recipe in api_response]
            return recipe_data
        except Exception as e:
            print("Exception when calling RecipesApi->search_recipes_by_ingredients: %s\n" % e)