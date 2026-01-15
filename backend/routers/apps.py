from fastapi import APIRouter, HTTPException
from typing import List
import os
import json

from backend.schemas import App

router = APIRouter(prefix="/api/apps", tags=["apps"])


@router.get("", response_model=List[App])
async def get_apps():
    """Get all portfolio applications"""
    apps_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "apps.json")
    
    try:
        with open(apps_path, "r", encoding="utf-8") as f:
            apps_data = json.load(f)
        return apps_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Apps data not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid apps data format")
