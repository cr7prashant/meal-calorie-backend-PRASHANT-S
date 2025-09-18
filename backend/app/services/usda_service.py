import requests
from fastapi import HTTPException, status
from core.config import settings
from utils.fuzzy_match import find_closest_match
from functools import lru_cache

class USDAService:
    BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
    
    @staticmethod
    @lru_cache(maxsize=100) 
    def search_food(query: str):
        """Search for food in USDA database with fuzzy matching"""
        try:
            params = {
                "api_key": settings.USDA_API_KEY,
                "query": query,
                "pageSize": 10,
                "dataType": ["Survey (FNDDS)"]
            }
            
            response = requests.get(USDAService.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('foods'):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No results found for '{query}'"
                )
            
            # Use fuzzy matching to find the best result
            food_descriptions = [food['description'] for food in data['foods']]
            best_match = find_closest_match(query, food_descriptions)
            
            # Get the matching food item
            matched_food = next(food for food in data['foods'] 
                              if food['description'] == best_match)
            
            return matched_food
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="USDA API service unavailable"
            ) from e

    @staticmethod
    def extract_calories(food_item: dict):
        """Extract calories from USDA food item"""
        for nutrient in food_item.get('foodNutrients', []):
            if nutrient.get('nutrientName') == 'Energy' and nutrient.get('unitName') == 'KCAL':
                return nutrient.get('value', 0)
        return 0