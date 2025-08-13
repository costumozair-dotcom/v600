
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Secure Key Manager
Gerenciador seguro de chaves API sem hardcoding
"""

import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class SecureKeyManager:
    """Gerenciador seguro de chaves API"""
    
    def __init__(self):
        """Inicializa o gerenciador de chaves"""
        self.required_keys = [
            'GEMINI_API_KEY',
            'JINA_API_KEY',
            'EXA_API_KEY',
            'SUPADATA_API_KEY',
            'YOUTUBE_API_KEY',
            'GOOGLE_SEARCH_KEY',
            'GOOGLE_CSE_ID',
            'SERPER_API_KEY'
        ]
        self.key_status = self._check_all_keys()
        logger.info(f"🔐 Secure Key Manager: {len(self.get_available_keys())}/{len(self.required_keys)} chaves disponíveis")
    
    def _check_all_keys(self) -> Dict[str, bool]:
        """Verifica disponibilidade de todas as chaves"""
        status = {}
        for key in self.required_keys:
            value = os.getenv(key)
            status[key] = bool(value and len(value.strip()) > 10)
        return status
    
    def get_key(self, key_name: str) -> Optional[str]:
        """Obtém chave de forma segura"""
        if key_name not in self.required_keys:
            logger.warning(f"⚠️ Chave não reconhecida: {key_name}")
            return None
        
        value = os.getenv(key_name)
        if not value or len(value.strip()) < 10:
            logger.warning(f"⚠️ Chave {key_name} não configurada ou inválida")
            return None
        
        return value.strip()
    
    def is_key_available(self, key_name: str) -> bool:
        """Verifica se chave está disponível"""
        return self.key_status.get(key_name, False)
    
    def get_available_keys(self) -> List[str]:
        """Retorna lista de chaves disponíveis"""
        return [key for key, available in self.key_status.items() if available]
    
    def get_missing_keys(self) -> List[str]:
        """Retorna lista de chaves em falta"""
        return [key for key, available in self.key_status.items() if not available]
    
    def refresh_key_status(self):
        """Atualiza status das chaves"""
        self.key_status = self._check_all_keys()
        logger.info(f"🔄 Status das chaves atualizado: {len(self.get_available_keys())}/{len(self.required_keys)} disponíveis")

# Instância global
secure_key_manager = SecureKeyManager()
