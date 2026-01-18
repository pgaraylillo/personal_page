import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple

try:
    from openai import OpenAI
except ImportError:
    print("❌ Error: 'openai' module not found. Please install dependencies:")
    print("   pip install -r backend/requirements.txt")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' module not found. Please install dependencies:")
    print("   pip install -r backend/requirements.txt")
    sys.exit(1)


class MedicalResearchService:
    """Service to research medical topics daily and create blog posts with images"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.blog_dir = self.data_dir / "blog"
        self.img_dir = Path(__file__).parent.parent.parent / "frontend" / "img"
        
        # Ensure directories exist
        self.blog_dir.mkdir(parents=True, exist_ok=True)
        self.img_dir.mkdir(parents=True, exist_ok=True)
    
    def research_medical_topic(self) -> Dict[str, str]:
        """
        Research a relevant medical topic using AI to suggest topics
        and then generate comprehensive content about it.
        """
        print("🔍 Investigating medical topics...")
        
        # Step 1: Get a relevant medical topic suggestion
        topic_prompt = """Sugiere un tema médico relevante, actual e interesante para hoy.
Responde SOLO con el título del tema en español, sin explicaciones adicionales.
Ejemplos: "Nuevos avances en telemedicina", "Inteligencia artificial en diagnóstico médico", 
"Actualizaciones en guías de tratamiento para hipertensión", etc.
El tema debe ser relevante para profesionales de la salud."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en medicina que sugiere temas relevantes y actuales."},
                    {"role": "user", "content": topic_prompt}
                ],
                temperature=0.9,
                max_tokens=100
            )
            topic = response.choices[0].message.content.strip()
            print(f"📋 Topic selected: {topic}")
        except Exception as e:
            print(f"❌ Error getting topic: {e}")
            # Fallback topic
            topic = "Avances recientes en medicina"
        
        # Step 2: Generate comprehensive content about the topic
        content_prompt = f"""Escribe un artículo completo en español sobre el tema médico: "{topic}"

El artículo debe:
- Ser profesional pero accesible
- Tener entre 500-800 palabras
- Incluir una introducción interesante
- Tener al menos 3 secciones principales con subtítulos (##)
- Incluir información relevante y actual
- Terminar con una reflexión o conclusión
- Usar formato Markdown correctamente

No incluyas el título principal (será agregado automáticamente).
Inicia directamente con el contenido después de una breve introducción."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un médico experto que escribe artículos médicos informativos y actualizados."},
                    {"role": "user", "content": content_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            content = response.choices[0].message.content.strip()
            print(f"✅ Content generated ({len(content)} characters)")
        except Exception as e:
            print(f"❌ Error generating content: {e}")
            content = f"## Introducción\n\nEl tema de {topic} es de gran relevancia en la medicina actual.\n\n## Desarrollo\n\nEste tema requiere investigación continua y actualización constante de conocimientos.\n\n## Conclusión\n\nEs importante mantenerse actualizado sobre este tema médico relevante."
        
        # Step 3: Generate excerpt
        excerpt_prompt = f"""Crea un resumen breve (máximo 150 caracteres) del artículo sobre "{topic}".
El resumen debe ser atractivo y descriptivo."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": excerpt_prompt}
                ],
                temperature=0.7,
                max_tokens=50
            )
            excerpt = response.choices[0].message.content.strip()
        except Exception as e:
            excerpt = f"Exploración sobre {topic} y su relevancia en la medicina actual."
        
        return {
            "topic": topic,
            "content": content,
            "excerpt": excerpt
        }
    
    def generate_image(self, topic: str) -> Optional[str]:
        """
        Generate an image related to the medical topic using DALL-E
        Returns the filename of the saved image
        """
        print(f"🎨 Generating image for topic: {topic}")
        
        # Create image prompt
        image_prompt = f"""Medical illustration, professional, modern, clean design, 
related to: {topic}. Style: medical infographic, professional healthcare illustration, 
modern medical art, clean and informative. Avoid text in the image. 
Professional medical illustration style."""
        
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            print(f"✅ Image generated: {image_url}")
            
            # Download and save the image
            filename = self._sanitize_filename(topic) + "_" + datetime.now().strftime("%Y%m%d") + ".png"
            filepath = self.img_dir / filename
            
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            print(f"💾 Image saved: {filepath}")
            return filename
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return None
    
    def create_markdown_file(self, topic: str, content: str, excerpt: str, image_filename: Optional[str]) -> str:
        """
        Create a markdown file in data/blog/ with proper frontmatter
        Returns the filename of the created file
        """
        print("📝 Creating markdown file...")
        
        # Sanitize topic for filename
        filename = self._sanitize_filename(topic) + "_" + datetime.now().strftime("%Y%m%d") + ".md"
        filepath = self.blog_dir / filename
        
        # Check if file already exists (if running multiple times per day)
        if filepath.exists():
            # Add timestamp to filename
            timestamp = datetime.now().strftime("%H%M%S")
            filename = self._sanitize_filename(topic) + "_" + datetime.now().strftime("%Y%m%d") + "_" + timestamp + ".md"
            filepath = self.blog_dir / filename
        
        # Prepare image reference if available
        image_ref = ""
        if image_filename:
            image_ref = f"\n![{topic}](/img/{image_filename})\n"
        
        # Create frontmatter
        frontmatter = f"""---
title: "{topic}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
author: "Pablo Garay"
excerpt: "{excerpt}"
tags: "Medicina, Investigación, Actualización Médica"
---
"""
        
        # Combine frontmatter, image, and content
        markdown_content = frontmatter + "\n# " + topic + "\n\n" + image_ref + "\n" + content
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Markdown file created: {filepath}")
        return filename
    
    def _sanitize_filename(self, text: str) -> str:
        """Convert text to a safe filename"""
        # Convert to lowercase
        text = text.lower()
        # Replace spaces with hyphens
        text = text.replace(' ', '-')
        # Remove special characters, keep only alphanumeric and hyphens
        text = re.sub(r'[^a-z0-9\-]', '', text)
        # Remove multiple consecutive hyphens
        text = re.sub(r'-+', '-', text)
        # Remove leading/trailing hyphens
        text = text.strip('-')
        # Limit length
        text = text[:50]
        return text
    
    def run_daily_research(self) -> Dict[str, str]:
        """
        Main function to run the daily medical research process
        Returns dict with results
        """
        print("🚀 Starting daily medical research...")
        print("=" * 60)
        
        try:
            # Step 1: Research topic and generate content
            research_result = self.research_medical_topic()
            
            # Step 2: Generate image
            image_filename = self.generate_image(research_result["topic"])
            
            # Step 3: Create markdown file
            md_filename = self.create_markdown_file(
                topic=research_result["topic"],
                content=research_result["content"],
                excerpt=research_result["excerpt"],
                image_filename=image_filename
            )
            
            print("=" * 60)
            print("✅ Daily research completed successfully!")
            print(f"📄 File created: {md_filename}")
            if image_filename:
                print(f"🖼️  Image created: {image_filename}")
            
            return {
                "status": "success",
                "markdown_file": md_filename,
                "image_file": image_filename,
                "topic": research_result["topic"]
            }
            
        except Exception as e:
            print("=" * 60)
            print(f"❌ Error during daily research: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e)
            }


# Singleton instance
medical_research_service = MedicalResearchService()
