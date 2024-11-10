from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class BaseLLM(ABC):
    """Abstract base class for LLM implementations"""
    
    @abstractmethod
    def __init__(self, model_config: Dict[str, Any]):
        """Initialize the LLM with configuration"""
        self.model_config = model_config
        self.is_initialized = False
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        **kwargs
    ) -> str:
        """Generate a completion for the given prompt"""
        pass
    
    @abstractmethod
    async def generate_chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        **kwargs
    ) -> str:
        """Generate a chat completion for the given messages"""
        pass
    
    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings for the given text"""
        pass
    
    @property
    @abstractmethod
    def token_limit(self) -> int:
        """Return the maximum token limit for the model"""
        pass
    
    def validate_config(self) -> bool:
        """Validate the model configuration"""
        return True 