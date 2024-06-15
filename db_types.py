from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class RecipeModel(BaseModel):
    """
    Container for a single recipe.
    """

    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    author: str = Field(...)
    img_url: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Costco chicken bake",
                "author": "jdoe@example.com",
                "img_url": "https://www.allrecipes.com/thmb/mZ-qW89GfZwMViVPR3HhtOzHS1A=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/7970726-Copycat-Costco-Chicken-Bake-DDMFS-3x4-3606652c5ca040afab6cf77860350020.jpg",
            }
        },
    )


class UpdateRecipeModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """
    
    name: Optional[str] = None
    author: Optional[str] = None
    img_url: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Costco chicken bake",
                "author": "jdoe@example.com",
                "img_url": "https://www.allrecipes.com/thmb/mZ-qW89GfZwMViVPR3HhtOzHS1A=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/7970726-Copycat-Costco-Chicken-Bake-DDMFS-3x4-3606652c5ca040afab6cf77860350020.jpg",
            }
        },
    )


class RecipeCollection(BaseModel):
    """
    A container holding a list of `Recipes` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    recipes: List[RecipeModel]

