import os
from typing import Optional
from openai import OpenAI
from anthropic import Anthropic


class AIService:
    """AI service for chatbot functionality with RAG-light context"""
    
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "openai").lower()
        self.context = self._load_context()
        
        if self.provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        elif self.provider == "anthropic":
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    def _load_context(self) -> str:
        """Load context from context.md file"""
        context_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "context.md")
        try:
            with open(context_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "No context available. Please create a context.md file."
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with context"""
        return f"""You are 'Dr. Pablo Garay's Assistant'.

INSTRUCTIONS:
1. **MAXIMUM 40 WORDS PER RESPONSE.** NO EXCEPTIONS.
2. Answer the user's question directly and briefly.
3. ALWAYS end with a short question engaging the user to ask more.
4. Speak in the user's language (Spanish preferred).
5. Do NOT list items. Do NOT summarize everything.

Bio Context:
{self.context}

REMEMBER: BE BRIEF. MAX 40 WORDS."""
    
    async def get_response(self, user_message: str) -> str:
        """Get AI response based on user message"""
        try:
            if self.provider == "openai":
                return await self._get_openai_response(user_message)
            elif self.provider == "anthropic":
                return await self._get_anthropic_response(user_message)
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}"
    
    async def _get_openai_response(self, user_message: str) -> str:
        """Get response from OpenAI"""
        print(f"DEBUG SYSTEM PROMPT: {self._build_system_prompt()}")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    async def _get_anthropic_response(self, user_message: str) -> str:
        """Get response from Anthropic"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            system=self._build_system_prompt(),
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return response.content[0].text


# Singleton instance
ai_service = AIService()
