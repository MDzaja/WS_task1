from django.shortcuts import render
from rdflib import Graph
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

from app.repositories.categoryrepo import getDistinctCategoryLabels
from app.repositories.foodrepo import getDistinctIngredientLabels
from app.repositories.reciperepo import getCompactRecipes, getCompactRecipes
from app.repositories.techniquerepo import getDistinctTechniqueLabels


def vehicle(request):
    # Load the RDF data
    g = Graph()
    g.parse("data_processed.rdf")

    # Define the SPARQL query
    query = """
        PREFIX ds: <https://data.wa.gov/resource/f6w7-q2d2/>
        SELECT ?make ?model ?ev_type ?electric_range
        WHERE {
            ?s ds:make ?make .
            ?s ds:model ?model .
            ?s ds:ev_type ?ev_type .
            ?s ds:electric_range ?electric_range .
        }
    """

    # Execute the SPARQL query
    results = g.query(query)

    # Render the results using a template
    context = {"results": results}
    return render(request, "vehicle_details.html", context)

def recipeTitle(request):
    # Create a connection to the GraphDB repository
    endpoint = "http://localhost:7200"
    repo_name = "WS-foodista"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)

    # SPARQL query to retrieve data from GraphDB
    query = """
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX lr: <http://linkedrecipes.org/schema/>
    
    SELECT ?title
    WHERE {
      ?recipe a lr:Recipe ;
              dcterms:title ?title .
    } LIMIT 20
    """

    # Execute the query and retrieve the results
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    titles = []
    for row in res['results']['bindings']:
        titles.append(row['title']['value'])

    # Render the results using a template
    context = {"titles": titles}
    return render(request, "recipe_titles.html", context)

def recipes(request):
    selectedCategoryList = request.GET.get('selected_categories', '').split(',')
    selectedTechniqueList = request.GET.get('selected_techniques', '').split(',')
    selectedIngredientList = request.GET.get('selected_ingredients', '').split(',')
    selectedCategoryList = list(filter(None, selectedCategoryList))
    selectedTechniqueList = list(filter(None, selectedTechniqueList))
    selectedIngredientList = list(filter(None, selectedIngredientList))
    searchTitle = request.GET.get('searchTitle', None)
    offset = request.GET.get('offset', 0)

    recipes = getCompactRecipes(offset=offset, limit=1000, searchTitle=searchTitle, categoryList=selectedCategoryList, techniqueList=selectedTechniqueList, ingredientList=selectedIngredientList)
    categoryList = getDistinctCategoryLabels()
    techniqueList = getDistinctTechniqueLabels()
    ingredientList = getDistinctIngredientLabels()

    context = {
        "recipe_list": recipes,
        "category_list": categoryList,
        "technique_list": techniqueList,
        "ingredient_list": ingredientList,
        "selected_categories": selectedCategoryList,
        "selected_techniques": selectedTechniqueList,
        "selected_ingredients": selectedIngredientList,
        "offset": offset
    }

    return render(request, "recipes.html", context)