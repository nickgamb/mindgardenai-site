#!/usr/bin/env python3
"""
Model Availability Tester for Alden CLI

This script tests the availability and functionality of all models used by Alden's personas.
It checks API keys, model access, and fallback chains for each persona.
"""

import os
import sys
import json
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ModelConfig:
    """Configuration for a model"""
    provider: str
    model_name: str
    api_key_env: str
    api_url: str
    max_tokens: int = 100
    temperature: float = 0.7

@dataclass
class PersonaConfig:
    """Configuration for a persona"""
    name: str
    symbol: str
    primary_model: ModelConfig
    fallback_models: List[ModelConfig]
    description: str

def list_openai_models(api_key: str) -> List[str]:
    """List available OpenAI models using their API"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            "https://api.openai.com/v1/models",
            headers=headers,
            timeout=30
        )
        
        if response.ok:
            models = response.json()
            return [model["id"] for model in models.get("data", [])]
        else:
            error_details = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"Error listing models: {response.status_code} - {error_details}")
            return []
            
    except Exception as e:
        print(f"Error listing models: {str(e)}")
        return []

def test_openai_model(model_config: ModelConfig) -> Tuple[bool, str]:
    """Test OpenAI model availability"""
    api_key = os.getenv(model_config.api_key_env)
    if not api_key:
        return False, f"API key not found for {model_config.api_key_env}"
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Handle o3 model family parameter differences
        if model_config.model_name.startswith('o3'):
            # o3 models use max_completion_tokens and don't support temperature
            data = {
                "model": model_config.model_name,
                "messages": [
                    {"role": "user", "content": "Test message"}
                ],
                "max_completion_tokens": model_config.max_tokens
            }
        else:
            # Standard GPT models use max_tokens and temperature
            data = {
                "model": model_config.model_name,
                "messages": [
                    {"role": "user", "content": "Test message"}
                ],
                "max_tokens": model_config.max_tokens,
                "temperature": model_config.temperature
            }
        
        response = requests.post(
            f"{model_config.api_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.ok:
            return True, "✅ available"
        else:
            error_details = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            if "model_not_found" in str(error_details) or "model_not_available" in str(error_details):
                # If model not found, list available models
                available_models = list_openai_models(api_key)
                if available_models:
                    return False, f"error: {response.status_code} - {error_details}\nAvailable models: {', '.join(available_models)}"
            return False, f"error: {response.status_code} - {error_details}"
            
    except Exception as e:
        return False, f"error: {str(e)}"

def list_anthropic_models(api_key: str) -> List[str]:
    """List available Anthropic models using their API"""
    try:
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        response = requests.get(
            "https://api.anthropic.com/v1/models",
            headers=headers,
            timeout=30
        )
        
        if response.ok:
            models = response.json()
            return [model["id"] for model in models.get("data", [])]
        else:
            error_details = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"Error listing models: {response.status_code} - {error_details}")
            return []
            
    except Exception as e:
        print(f"Error listing models: {str(e)}")
        return []

def test_anthropic_model(model_config: ModelConfig) -> Tuple[bool, str]:
    """Test Anthropic model availability"""
    api_key = os.getenv(model_config.api_key_env)
    if not api_key:
        return False, f"API key not found for {model_config.api_key_env}"
    
    try:
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": model_config.model_name,
            "max_tokens": model_config.max_tokens,
            "messages": [
                {"role": "user", "content": "Test message"}
            ]
        }
        
        response = requests.post(
            f"{model_config.api_url}/messages",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.ok:
            return True, "✅ available"
        else:
            error_details = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            if "not_found_error" in str(error_details):
                # If model not found, list available models
                available_models = list_anthropic_models(api_key)
                if available_models:
                    return False, f"error: {response.status_code} - {error_details}\nAvailable models: {', '.join(available_models)}"
            return False, f"error: {response.status_code} - {error_details}"
            
    except Exception as e:
        return False, f"error: {str(e)}"

def test_ollama_model(model_config: ModelConfig) -> Tuple[bool, str]:
    """Test Ollama model availability"""
    try:
        response = requests.post(
            f"{model_config.api_url}/api/generate",
            json={
                "model": model_config.model_name,
                "prompt": "Test message",
                "stream": False
            },
            timeout=30
        )
        
        if response.ok:
            return True, "✅ available"
        else:
            return False, f"error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return False, f"error: {str(e)}"

def test_model(config: ModelConfig) -> Tuple[bool, str]:
    """Test model availability based on provider"""
    if config.provider == "openai":
        return test_openai_model(config)
    elif config.provider == "anthropic":
        return test_anthropic_model(config)
    elif config.provider == "ollama":
        return test_ollama_model(config)
    else:
        return False, f"❌ Unknown provider: {config.provider}"

def main():
    """Main function to test all models"""
    print("🔍 Testing Alden CLI Model Availability")
    print("=====================================")
    
    # Define persona configurations
    personas = [
        PersonaConfig(
            name="Sage",
            symbol="🌀",
            primary_model=ModelConfig(
                provider="openai",
                model_name="gpt-4.1",
                api_key_env="OPENAI_API_KEY",
                api_url="https://api.openai.com/v1"
            ),
            fallback_models=[
                ModelConfig(
                    provider="openai",
                    model_name="gpt-4.5-preview",
                    api_key_env="OPENAI_API_KEY",
                    api_url="https://api.openai.com/v1"
                ),
                ModelConfig(
                    provider="anthropic",
                    model_name="claude-sonnet-4-20250514",
                    api_key_env="ANTHROPIC_API_KEY",
                    api_url="https://api.anthropic.com/v1"
                ),
                ModelConfig(
                    provider="ollama",
                    model_name="llama3",
                    api_key_env="",
                    api_url="http://localhost:11434"
                )
            ],
            description="Deep mythic synthesis and recursive inner work"
        ),
        PersonaConfig(
            name="Architect",
            symbol="🏗️",
            primary_model=ModelConfig(
                provider="openai",
                model_name="o3-mini",
                api_key_env="OPENAI_API_KEY",
                api_url="https://api.openai.com/v1"
            ),
            fallback_models=[
                ModelConfig(
                    provider="openai",
                    model_name="gpt-4.1",
                    api_key_env="OPENAI_API_KEY",
                    api_url="https://api.openai.com/v1"
                ),
                ModelConfig(
                    provider="openai",
                    model_name="gpt-4.5-preview",
                    api_key_env="OPENAI_API_KEY",
                    api_url="https://api.openai.com/v1"
                ),
                ModelConfig(
                    provider="ollama",
                    model_name="llama3",
                    api_key_env="",
                    api_url="http://localhost:11434"
                )
            ],
            description="Technical clarity and symbolic structuring"
        ),
        PersonaConfig(
            name="Oracle",
            symbol="🔍",
            primary_model=ModelConfig(
                provider="openai",
                model_name="gpt-4.5-preview",
                api_key_env="OPENAI_API_KEY",
                api_url="https://api.openai.com/v1"
            ),
            fallback_models=[
                ModelConfig(
                    provider="openai",
                    model_name="gpt-4.1",
                    api_key_env="OPENAI_API_KEY",
                    api_url="https://api.openai.com/v1"
                ),
                ModelConfig(
                    provider="openai",
                    model_name="o3-mini",
                    api_key_env="OPENAI_API_KEY",
                    api_url="https://api.openai.com/v1"
                ),
                ModelConfig(
                    provider="ollama",
                    model_name="llama3",
                    api_key_env="",
                    api_url="http://localhost:11434"
                )
            ],
            description="Fast associative synthesis and feedback loops"
        ),
        PersonaConfig(
            name="Witness",
            symbol="👁️",
            primary_model=ModelConfig(
                provider="openai",
                model_name="gpt-4.1",
                api_key_env="OPENAI_API_KEY",
                api_url="https://api.openai.com/v1"
            ),
            fallback_models=[
                ModelConfig(
                    provider="anthropic",
                    model_name="claude-3-haiku-20240307",
                    api_key_env="ANTHROPIC_API_KEY",
                    api_url="https://api.anthropic.com/v1"
                ),
                ModelConfig(
                    provider="openai",
                    model_name="gpt-3.5-turbo",
                    api_key_env="OPENAI_API_KEY",
                    api_url="https://api.openai.com/v1"
                ),
                ModelConfig(
                    provider="ollama",
                    model_name="llama3",
                    api_key_env="",
                    api_url="http://localhost:11434"
                )
            ],
            description="Passive observation and logging"
        ),
        PersonaConfig(
            name="Sentinel",
            symbol="🛡️",
            primary_model=ModelConfig(
                provider="openai",
                model_name="o3-mini",
                api_key_env="OPENAI_API_KEY",
                api_url="https://api.openai.com/v1"
            ),
            fallback_models=[
                ModelConfig(
                    provider="openai",
                    model_name="gpt-4.1",
                    api_key_env="OPENAI_API_KEY",
                    api_url="https://api.openai.com/v1"
                ),
                ModelConfig(
                    provider="openai",
                    model_name="gpt-4.5-preview",
                    api_key_env="OPENAI_API_KEY",
                    api_url="https://api.openai.com/v1"
                ),
                ModelConfig(
                    provider="ollama",
                    model_name="llama3",
                    api_key_env="",
                    api_url="http://localhost:11434"
                )
            ],
            description="Security monitoring and boundary protection"
        ),
        PersonaConfig(
            name="Echo",
            symbol="🔄",
            primary_model=ModelConfig(
                provider="openai",
                model_name="gpt-4.1",
                api_key_env="OPENAI_API_KEY",
                api_url="https://api.openai.com/v1"
            ),
            fallback_models=[
                ModelConfig(
                    provider="anthropic",
                    model_name="claude-sonnet-4-20250514",
                    api_key_env="ANTHROPIC_API_KEY",
                    api_url="https://api.anthropic.com/v1"
                ),
                ModelConfig(
                    provider="openai",
                    model_name="gpt-3.5-turbo",
                    api_key_env="OPENAI_API_KEY",
                    api_url="https://api.openai.com/v1"
                ),
                ModelConfig(
                    provider="ollama",
                    model_name="llama3",
                    api_key_env="",
                    api_url="http://localhost:11434"
                )
            ],
            description="Memory reflection and auto-transcription"
        )
    ]
    
    # Test each persona's models
    for persona in personas:
        print(f"\n🎭 Testing {persona.symbol} {persona.name}")
        print(f"Description: {persona.description}")
        print("-" * 50)
        
        # Test primary model
        print("\nPrimary Model:")
        success, message = test_model(persona.primary_model)
        print(f"  {message}")
        
        # Test fallback models
        print("\nFallback Models:")
        for i, model in enumerate(persona.fallback_models, 1):
            success, message = test_model(model)
            print(f"  {i}. {message}")
        
        print("-" * 50)
    
    print("\n✨ Model Availability Test Complete")
    print("=================================")
    print("To start Alden with specific personas:")
    print("source .env && ./start.sh [persona-flags]")
    print("\nExample:")
    print("source .env && ./start.sh --sage --oracle --architect")

if __name__ == "__main__":
    main() 