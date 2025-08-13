
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Fallback Manager - Sistema de Fallback Inteligente
Gerencia fallbacks robustos para AI e Search providers
"""

import os
import time
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime

logger = logging.getLogger(__name__)

class EnhancedFallbackManager:
    """Gerenciador de Fallbacks Inteligente e Robusto"""
    
    def __init__(self):
        self.providers_status = {}
        self.fallback_history = []
        self.retry_delays = [1, 2, 4, 8, 16]  # Exponential backoff
        
    def execute_with_fallback(
        self, 
        primary_function: Callable,
        fallback_functions: List[Callable],
        context: Dict[str, Any],
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """Executa função com fallbacks inteligentes"""
        
        all_functions = [primary_function] + fallback_functions
        
        for attempt, func in enumerate(all_functions):
            for retry in range(max_retries):
                try:
                    logger.info(f"🔄 Tentativa {retry + 1}/{max_retries} - Função: {func.__name__}")
                    
                    result = func(**context)
                    
                    if self._validate_result(result):
                        self._record_success(func.__name__, attempt, retry)
                        return {
                            "status": "success",
                            "result": result,
                            "provider_used": func.__name__,
                            "attempt": attempt + 1,
                            "retry": retry + 1
                        }
                    else:
                        logger.warning(f"⚠️ Resultado inválido de {func.__name__}")
                        
                except Exception as e:
                    logger.error(f"❌ Erro em {func.__name__}: {e}")
                    self._record_error(func.__name__, str(e))
                    
                    # Espera antes do retry
                    if retry < max_retries - 1:
                        delay = self.retry_delays[min(retry, len(self.retry_delays) - 1)]
                        time.sleep(delay)
        
        # Se chegou aqui, todos os fallbacks falharam
        return {
            "status": "total_failure",
            "error": "Todos os providers falharam",
            "fallback_history": self.fallback_history
        }
    
    def _validate_result(self, result: Any) -> bool:
        """Valida se o resultado é válido"""
        
        if not result:
            return False
            
        if isinstance(result, dict):
            if result.get("status") == "error":
                return False
            if "error" in result and not result.get("content"):
                return False
                
        if isinstance(result, str) and len(result) < 10:
            return False
            
        return True
    
    def _record_success(self, provider: str, attempt: int, retry: int):
        """Registra sucesso de provider"""
        
        self.providers_status[provider] = {
            "status": "success",
            "last_success": datetime.now().isoformat(),
            "attempt": attempt + 1,
            "retry": retry + 1
        }
        
        logger.info(f"✅ Sucesso: {provider} (tentativa {attempt + 1}, retry {retry + 1})")
    
    def _record_error(self, provider: str, error: str):
        """Registra erro de provider"""
        
        self.providers_status[provider] = {
            "status": "error",
            "last_error": datetime.now().isoformat(),
            "error": error
        }
        
        self.fallback_history.append({
            "provider": provider,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_provider_reliability(self) -> Dict[str, Any]:
        """Retorna confiabilidade dos providers"""
        
        reliability = {}
        
        for provider, status in self.providers_status.items():
            if status["status"] == "success":
                reliability[provider] = {
                    "reliable": True,
                    "last_success": status["last_success"]
                }
            else:
                reliability[provider] = {
                    "reliable": False,
                    "last_error": status.get("last_error"),
                    "error": status.get("error")
                }
        
        return reliability

# Instância global
enhanced_fallback_manager = EnhancedFallbackManager()
