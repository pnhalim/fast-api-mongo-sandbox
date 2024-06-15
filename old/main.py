from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/recipes")
async def get_recipes():
    """Returns a list of all recipes."""
    
    return {"getting recipe": "Hello World"}

@app.post("/recipes")
async def add_recipe():
    """Adds a recipe to the db and returns the new recipe."""
    return {"adding a recipe": "Hello World"}
