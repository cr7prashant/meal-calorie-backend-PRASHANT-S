from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.calories import CaloriesRequest, CaloriesResponse
from services.usda_service import USDAService
from api.v1.deps import get_current_user

router = APIRouter()

@router.post("/get-calories", response_model=CaloriesResponse)
def get_calories(
    request: CaloriesRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        # Search for food in USDA database
        food_item = USDAService.search_food(request.dish_name)
        
        # Extract calories
        calories_per_serving = USDAService.extract_calories(food_item)
        
        if calories_per_serving == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Could not find calorie information for '{request.dish_name}'"
            )
        
        # Calculate total calories
        total_calories = calories_per_serving * request.servings
        
        return CaloriesResponse(
            dish_name=request.dish_name,
            servings=request.servings,
            calories_per_serving=round(calories_per_serving, 2),
            total_calories=round(total_calories, 2),
            source="USDA FoodData Central"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error processing your request"
        ) from e