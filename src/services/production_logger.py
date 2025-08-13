
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Production Logger
Sistema de logging otimizado para produção
"""

import os
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

class ProductionLogger:
    """Sistema de logging otimizado para produção"""
    
    def __init__(self):
        """Inicializa o sistema de logging de produção"""
        self.setup_production_logging()
    
    def setup_production_logging(self):
        """Configura logging para produção"""
        
        # Remove handlers existentes
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Configura nível baseado no ambiente
        if os.getenv('FLASK_ENV') == 'production':
            log_level = logging.INFO
        else:
            log_level = logging.DEBUG
        
        # Formato de log otimizado
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para arquivo rotativo
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'arqv30_production.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        
        # Handler para console (apenas erros em produção)
        console_handler = logging.StreamHandler(sys.stdout)
        if os.getenv('FLASK_ENV') == 'production':
            console_handler.setLevel(logging.WARNING)
        else:
            console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Configura logger raiz
        root_logger.setLevel(log_level)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        # Desabilita logs verbosos de bibliotecas externas
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        
        logging.info("🔧 Sistema de logging de produção configurado")

# Inicializa automaticamente
production_logger = ProductionLogger()
