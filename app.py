import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
import motor.motor_asyncio
from pymongo import ReturnDocument

# import relevant db types
from db_types import *

# set up fast api
app = FastAPI(
    title="sandbox recipe api",
    summary="a sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)
# set up mongo db
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.sandbox_db
recipe_collection = db.get_collection("recipes")



@app.post(
    "/recipes/",
    response_description="Add new recipe",
    response_model=RecipeModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def __POST_EXAMPLE__(recipe: RecipeModel = Body(...)): # this unpacks the json body into RecipeModel object
    """
    Insert a new recipe.
    A unique `id` will be created and provided in the response.
    """

    new_recipe = await recipe_collection.insert_one(
        recipe.model_dump(by_alias=True, exclude=["id"]) # let the id be automatically generated and set in new_recipe
    )
    created_recipe = await recipe_collection.find_one( # get the new data (confirm that it's stored in db)
        {"_id": new_recipe.inserted_id}
    )
    return created_recipe


@app.get(
    "/recipes/",
    response_description="List all recipes",
    response_model=RecipeCollection,
    response_model_by_alias=False,
)
async def __GET_ALL_EXAMPLE__():
    """
    List all of the recipes in the database.
    The response is unpaginated and limited to 1000 results.
    """

    return RecipeCollection(recipes=await recipe_collection.find().to_list(1000))


@app.get(
    "/recipes/{id}",
    response_description="Get a single recipe",
    response_model=RecipeModel,
    response_model_by_alias=False,
)
async def __GET_BY_ID_EXAMPLE__(id: str):
    """
    Get the record for a specific recipe, looked up by `id`.
    """
    if (
        recipe := await recipe_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return recipe

    raise HTTPException(status_code=404, detail=f"Recipe {id} not found")


@app.put(
    "/recipes/{id}",
    response_description="Update a recipe",
    response_model=RecipeModel,
    response_model_by_alias=False,
)
async def __PUT_EXAMPLE__(id: str, recipe: UpdateRecipeModel = Body(...)): # we use type UpdateRecipeModel which can have missing fields
    """
    Update individual fields of an existing student record.
    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """

    recipe = {
        k: v for k, v in recipe.model_dump(by_alias=True).items() if v is not None
    }

    if len(recipe) >= 1:
        update_result = await recipe_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": recipe},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Recipe {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_recipe := await recipe_collection.find_one({"_id": id})) is not None:
        return existing_recipe

    raise HTTPException(status_code=404, detail=f"Recipe {id} not found")


@app.delete("/recipes/{id}", response_description="Delete a recipe")
async def __DELETE_EXAMPLE__(id: str):
    """
    Remove a single recipe from the database.
    """
    delete_result = await recipe_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Recipe {id} not found")
