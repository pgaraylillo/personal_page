from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class BlogPost(BaseModel):
    """Blog post model"""
    slug: str
    title: str
    date: str
    author: str = "Pablo Garay"
    excerpt: str
    content: Optional[str] = None
    tags: List[str] = []


class App(BaseModel):
    """Portfolio app model"""
    id: str
    name: str
    description: str
    tech_stack: List[str]
    demo_url: Optional[str] = None
    github_url: Optional[str] = None
    image_url: Optional[str] = None
    featured: bool = False


class ChatMessage(BaseModel):
    """Chat message model"""
    message: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    timestamp: datetime = Field(default_factory=datetime.now)
