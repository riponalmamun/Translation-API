import openai
from config.settings import settings
from typing import Dict, Optional
import uuid

class ChatService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.conversations = {}  # In-memory storage (use database in production)
        self.agent_types = {
            "general": "You are a helpful AI assistant.",
            "translator": "You are a professional translator assistant.",
            "teacher": "You are a language learning teacher.",
            "business": "You are a business communication assistant.",
            "technical": "You are a technical support assistant."
        }
    
    async def chat(
        self, 
        message: str, 
        language: str, 
        conversation_id: Optional[str] = None,
        agent_type: str = "general"
    ) -> Dict:
        """Chat with AI agent in any language"""
        try:
            # Generate or retrieve conversation ID
            if not conversation_id:
                conversation_id = str(uuid.uuid4())
                self.conversations[conversation_id] = []
            
            # Get agent system message
            system_message = self.agent_types.get(agent_type, self.agent_types["general"])
            
            # Add language instruction
            system_message += f" Respond in {language} language. Maintain natural conversation flow."
            
            # Get conversation history
            history = self.conversations.get(conversation_id, [])
            
            # Build messages for API
            messages = [
                {"role": "system", "content": system_message}
            ]
            
            # Add conversation history
            for msg in history[-10:]:  # Last 10 messages for context
                messages.append(msg)
            
            # Add current user message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=settings.GPT_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Save to conversation history
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []
            
            self.conversations[conversation_id].append({
                "role": "user",
                "content": message
            })
            self.conversations[conversation_id].append({
                "role": "assistant",
                "content": ai_response
            })
            
            return {
                "message": ai_response,
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            raise Exception(f"Chat error: {str(e)}")
    
    async def get_conversation_history(self, conversation_id: str) -> list:
        """Get conversation history"""
        return self.conversations.get(conversation_id, [])
    
    async def clear_conversation(self, conversation_id: str) -> bool:
        """Clear conversation history"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False