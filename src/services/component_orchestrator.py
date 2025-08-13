#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Component Orchestrator com tratamento robusto de erros
"""

import logging
import threading
from datetime import datetime
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)
"""
ARQV30 Enhanced v2.0 - Component Orchestrator
Orquestrador seguro de componentes com validação rigorosa
"""

import logging
import time
import json
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class ComponentValidationError(Exception):
    """Exceção para erros de validação de componentes"""
    pass

class ComponentOrchestrator:
    """Component Orchestrator com tratamento robusto de erros"""
    
    def __init__(self):
        self.components_status = {}
        self.execution_lock = threading.Lock() if 'threading' in globals() else None
        logger.info("🔧 Component Orchestrator inicializado")
    
    def execute_component_safely(self, component_name: str, component_func, *args, **kwargs):
        """Executa componente com tratamento seguro de erros"""
        try:
            logger.info(f"🚀 Executando componente: {component_name}")
            result = component_func(*args, **kwargs)
            
            self.components_status[component_name] = {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'result_available': bool(result)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro no componente {component_name}: {e}")
            
            self.components_status[component_name] = {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'result_available': False
            }
            
            # Retorna resultado de fallback em vez de propagar erro
            return self._create_component_fallback(component_name, str(e))
    
    def _create_component_fallback(self, component_name: str, error_msg: str) -> Dict[str, Any]:
        """Cria resultado de fallback para componente com falha"""
        return {
            'status': 'fallback',
            'component': component_name,
            'error': error_msg,
            'fallback_used': True,
            'timestamp': datetime.now().isoformat(),
            'message': f'Componente {component_name} executado com fallback devido a erro'
        }
    
    def get_components_status(self) -> Dict[str, Any]:
        """Retorna status de todos os componentes"""
        return {
            'total_components': len(self.components_status),
            'successful_components': len([c for c in self.components_status.values() if c['status'] == 'success']),
            'failed_components': len([c for c in self.components_status.values() if c['status'] == 'error']),
            'components_detail': self.components_status
        }
    """Orquestrador seguro de componentes da análise"""

    def __init__(self):
        """Inicializa o orquestrador"""
        self.component_registry = {}
        self.execution_order = []
        self.validation_rules = {}
        self.component_results = {}
        self.execution_stats = {}

        logger.info("Component Orchestrator inicializado")

    def register_component(
        self, 
        name: str, 
        executor: Callable,
        dependencies: List[str] = None,
        validation_rules: Dict[str, Any] = None,
        required: bool = True
    ):
        """Registra um componente no orquestrador"""

        self.component_registry[name] = {
            'executor': executor,
            'dependencies': dependencies or [],
            'validation_rules': validation_rules or {},
            'required': required,
            'status': 'pending'
        }

        if name not in self.execution_order:
            self.execution_order.append(name)

        logger.info(f"📝 Componente registrado: {name}")

    def execute_components(
        self, 
        input_data: Dict[str, Any],
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Executa todos os componentes registrados em ordem"""

        logger.info(f"🚀 Iniciando execução de {len(self.component_registry)} componentes")
        start_time = time.time()

        successful_components = {}
        failed_components = {}

        # Reset status
        for component_name in self.component_registry:
            self.component_registry[component_name]['status'] = 'pending'

        logger.info("🔄 Orquestração iniciada - executando componentes...")

        # Executa cada componente
        for i, component_name in enumerate(self.execution_order):
            if component_name not in self.component_registry:
                continue

            try:
                if progress_callback:
                    progress_callback(i + 1, f"Executando {component_name}...")

                logger.info(f"🔄 Executando componente: {component_name}")

                # Prepara dados com resultados anteriores
                component_data = input_data.copy()
                component_data['previous_results'] = successful_components

                # Executa componente
                executor = self.component_registry[component_name]['executor']
                result = executor(component_data)

                # Valida resultado
                if result and self._validate_component_result(component_name, result):
                    successful_components[component_name] = result
                    self._mark_component_success(component_name)
                    logger.info(f"✅ {component_name}: Sucesso")

                    # Salva resultado imediatamente
                    salvar_etapa(f"componente_{component_name}", result, categoria="analise_completa")

                else:
                    error_msg = f"Componente {component_name} falhou na validação"
                    logger.error(f"❌ {error_msg}")
                    failed_components[component_name] = error_msg
                    self._mark_component_failed(component_name, error_msg)

            except Exception as e:
                error_msg = f"Erro na execução de {component_name}: {str(e)}"
                logger.error(f"❌ {error_msg}")
                failed_components[component_name] = error_msg
                self._mark_component_failed(component_name, error_msg)

                # Se é componente obrigatório, pode interromper
                if self.component_registry[component_name]['required']:
                    logger.error(f"🚨 Componente obrigatório {component_name} falhou - análise comprometida")

        execution_time = time.time() - start_time

        # Gera relatório final
        execution_report = {
            'successful_components': successful_components,
            'failed_components': failed_components,
            'execution_stats': {
                'total_components': len(self.component_registry),
                'successful_count': len(successful_components),
                'failed_count': len(failed_components),
                'success_rate': (len(successful_components) / len(self.component_registry)) * 100,
                'execution_time': execution_time
            }
        }

        logger.info(f"✅ Orquestração concluída: {len(successful_components)}/{len(self.component_registry)} componentes")

        # Salva relatório de execução
        salvar_etapa("component_orchestrator_report", execution_report, categoria="analise_completa")

        return execution_report

    def _validate_component_result(self, component_name: str, result: Any) -> bool:
        """Valida resultado de componente"""

        if not result:
            logger.warning(f"⚠️ {component_name}: Resultado vazio")
            return False

        rules = self.component_registry[component_name]['validation_rules']

        # Validação de tipo
        if 'type' in rules:
            expected_type = rules['type']
            if not isinstance(result, expected_type):
                logger.warning(f"⚠️ {component_name}: Tipo inválido - esperado {expected_type}, recebido {type(result)}")
                return False

        # Validação de tamanho mínimo
        if 'min_size' in rules:
            min_size = rules['min_size']
            if isinstance(result, dict) and len(result) < min_size:
                logger.warning(f"⚠️ {component_name}: Tamanho insuficiente - {len(result)} < {min_size}")
                return False
            elif isinstance(result, list) and len(result) < min_size:
                logger.warning(f"⚠️ {component_name}: Lista muito pequena - {len(result)} < {min_size}")
                return False

        # Validação de campos obrigatórios
        if 'required_fields' in rules and isinstance(result, dict):
            required_fields = rules['required_fields']
            missing_fields = [field for field in required_fields if field not in result]
            if missing_fields:
                logger.warning(f"⚠️ {component_name}: Campos obrigatórios ausentes - {missing_fields}")
                return False

        # Validação de erro
        if isinstance(result, dict) and 'error' in result:
            logger.warning(f"⚠️ {component_name}: Contém erro - {result.get('error')}")
            return False

        return True

    def _mark_component_success(self, component_name: str):
        """Marca componente como bem-sucedido"""
        self.component_registry[component_name]['status'] = 'success'

    def _mark_component_failed(self, component_name: str, error: str):
        """Marca componente como falhado"""
        self.component_registry[component_name]['status'] = 'failed'
        self.component_registry[component_name]['error'] = error

    def get_component_status(self, component_name: str) -> str:
        """Retorna status de um componente"""
        return self.component_registry.get(component_name, {}).get('status', 'not_found')

    def get_execution_summary(self) -> Dict[str, Any]:
        """Retorna resumo da execução"""

        status_counts = {}
        for component_name, component_info in self.component_registry.items():
            status = component_info.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            'total_components': len(self.component_registry),
            'status_breakdown': status_counts,
            'success_rate': status_counts.get('success', 0) / len(self.component_registry) * 100 if self.component_registry else 0
        }

# Instância global
component_orchestrator = ComponentOrchestrator()