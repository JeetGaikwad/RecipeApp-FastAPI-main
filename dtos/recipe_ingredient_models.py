from pydantic import BaseModel
from enum import Enum
from decimal import Decimal


class WeightUnitEnum(str, Enum):
    gram = "gram"
    kilogram = "kilogram"
    liter = "liter"
    milliliter = "mililiter"
    teaspoon = "teaspoon"
    tablespoon = "tablespoon"
    cup = "cup"
    piece = "piece"


class IngredientBaseModel(BaseModel):
    ingredientName: str


class RecipeIngredientRequest(BaseModel):
    quantity: Decimal
    unit: WeightUnitEnum


class RecipeIngredientResponseModel(BaseModel):
    ingredientName: str
    quantity: Decimal
    unit: WeightUnitEnum
