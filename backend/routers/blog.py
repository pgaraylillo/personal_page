from fastapi import APIRouter, HTTPException
from typing import List
import os
import markdown
import re
from pathlib import Path

from backend.schemas import BlogPost

router = APIRouter(prefix="/api/blog", tags=["blog"])


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content"""
    frontmatter = {}
    body = content
    
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            # Parse frontmatter
            frontmatter_text = parts[1].strip()
            for line in frontmatter_text.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    
                    # Handle tags as list
                    if key == "tags" and value:
                        frontmatter[key] = [tag.strip() for tag in value.split(",")]
                    else:
                        frontmatter[key] = value
            
            body = parts[2].strip()
    
    return frontmatter, body


@router.get("", response_model=List[BlogPost])
async def get_blog_posts():
    """Get all blog posts (metadata only)"""
    blog_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "blog")
    posts = []
    
    try:
        for filename in os.listdir(blog_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(blog_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                frontmatter, body = parse_frontmatter(content)
                
                # Extract excerpt (first paragraph or from frontmatter)
                excerpt = frontmatter.get("excerpt", "")
                if not excerpt:
                    # Get first paragraph as excerpt
                    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
                    excerpt = paragraphs[0][:200] + "..." if paragraphs else ""
                
                posts.append(BlogPost(
                    slug=filename.replace(".md", ""),
                    title=frontmatter.get("title", filename.replace(".md", "").replace("-", " ").title()),
                    date=frontmatter.get("date", ""),
                    author=frontmatter.get("author", "Pablo Garay"),
                    excerpt=excerpt,
                    tags=frontmatter.get("tags", [])
                ))
        
        # Sort by date (newest first)
        posts.sort(key=lambda x: x.date, reverse=True)
        return posts
    
    except FileNotFoundError:
        return []


@router.get("/{slug}", response_model=BlogPost)
async def get_blog_post(slug: str):
    """Get a specific blog post with full content"""
    blog_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "blog")
    filepath = os.path.join(blog_dir, f"{slug}.md")
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        frontmatter, body = parse_frontmatter(content)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(body, extensions=['fenced_code', 'tables'])
        
        return BlogPost(
            slug=slug,
            title=frontmatter.get("title", slug.replace("-", " ").title()),
            date=frontmatter.get("date", ""),
            author=frontmatter.get("author", "Pablo Garay"),
            excerpt=frontmatter.get("excerpt", ""),
            content=html_content,
            tags=frontmatter.get("tags", [])
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading blog post: {str(e)}")
