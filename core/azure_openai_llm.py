import os
from typing import List, Optional, Dict, Any
from llama_index.llms.azure_openai import AzureOpenAI 
from .llm_base import BaseLLM


class AzureOpenAILLM(BaseLLM):
    """Azure OpenAI implementation of the LLM interface"""
    llm: AzureOpenAI
    
    def __init__(self, model_config: Dict[str, Any]):
        super().__init__(model_config)

        if not self.validate_config():
            raise ValueError("Invalid Azure OpenAI configuration")

        self.llm = AzureOpenAI(
                    deployment_name=self.model_config["deployment_name"],
                    api_key=self.model_config["api_key"],
                    azure_endpoint=self.model_config["api_base"],
                    api_version=self.model_config["api_version"],
                    model=self.model_config["model"],
                    temperature=self.model_config.get("temperature", .25)
                )
            
        self.is_initialized = True
    
    async def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        **kwargs
    ) -> str:
        """Generate completion using Azure OpenAI"""
        try:
            response = await self.llm.Completion.acreate(
                engine=self.deployment_name,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop_sequences,
                **kwargs
            )
            return response.choices[0].text.strip()
        except Exception as e:
            raise Exception(f"Azure OpenAI generation failed: {str(e)}")
    
    async def generate_chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        **kwargs
    ) -> str:
        """Generate chat completion using Azure OpenAI"""
        try:
            response = await self.llm.ChatCompletion.acreate(
                engine=self.deployment_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop_sequences,
                **kwargs
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            raise Exception(f"Azure OpenAI chat generation failed: {str(e)}")
    
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings using Azure OpenAI"""
        try:
            response = await self.llm.Embedding.acreate(
                engine=self.embedding_deployment,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Azure OpenAI embedding generation failed: {str(e)}")
    
    @property
    def token_limit(self) -> int:
        """Return token limit based on model configuration"""
        # Token limits for different Azure OpenAI models
        model_limits = {
            "gpt-4": 8192,
            "gpt-4-32k": 32768,
            "gpt-35-turbo": 4096,
            "gpt-35-turbo-16k": 16384
        }
        return model_limits.get(self.model_config.get("model_name", "gpt-35-turbo"), 4096)
    
    def validate_config(self) -> bool:
        """Validate Azure OpenAI configuration"""
        required_fields = ["deployment_name", "api_base", "api_key", "model", "api_version"]
        
        # Check required config fields
        for field in required_fields:
            if not self.model_config.get(field):
                raise Exception(f"Missing Azure OpenAI configuration: {field}")
                return False
                
        return True 