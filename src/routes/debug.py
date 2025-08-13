
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Debug Routes
Rotas para debug e verificação de saúde do sistema
"""

import logging
from flask import Blueprint, jsonify, request
from services.service_health_checker import service_health_checker
from services.super_orchestrator import super_orchestrator

logger = logging.getLogger(__name__)

debug_bp = Blueprint('debug', __name__, url_prefix='/debug')

@debug_bp.route('/health', methods=['GET'])
def health_check():
    """Verificação de saúde do sistema"""
    try:
        health_data = service_health_checker.check_all_services()
        
        return jsonify({
            'success': True,
            'health_status': health_data['overall_health'],
            'details': health_data,
            'report_text': service_health_checker.generate_health_report()
        })

    except Exception as e:
        logger.error(f"❌ Erro na verificação de saúde: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@debug_bp.route('/services', methods=['GET'])
def list_services():
    """Lista status de todos os serviços"""
    try:
        health_data = service_health_checker.check_all_services()
        
        all_services = {}
        all_services.update(health_data['critical_services'])
        all_services.update(health_data['optional_services'])
        
        return jsonify({
            'success': True,
            'total_services': len(all_services),
            'services': all_services,
            'overall_health': health_data['overall_health']
        })

    except Exception as e:
        logger.error(f"❌ Erro ao listar serviços: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@debug_bp.route('/orchestrator', methods=['GET'])
def orchestrator_status():
    """Status do Super Orchestrator"""
    try:
        if super_orchestrator:
            active_sessions = len(super_orchestrator.execution_state)
            available_services = len(super_orchestrator.services)
            
            return jsonify({
                'success': True,
                'orchestrator_available': True,
                'active_sessions': active_sessions,
                'available_services': available_services,
                'services_list': list(super_orchestrator.services.keys())
            })
        else:
            return jsonify({
                'success': False,
                'orchestrator_available': False,
                'error': 'Super Orchestrator not initialized'
            }), 500

    except Exception as e:
        logger.error(f"❌ Erro ao verificar orchestrator: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@debug_bp.route('/test-basic', methods=['POST'])
def test_basic_functionality():
    """Teste básico de funcionalidade"""
    try:
        data = request.get_json() or {}
        
        # Dados de teste básicos
        test_data = {
            'segmento': data.get('segmento', 'Teste'),
            'produto': data.get('produto', 'Produto Teste'),
            'publico': 'Público Teste',
            'query': 'teste mercado brasil'
        }
        
        # Testa apenas inicialização dos componentes, não execução completa
        test_results = {
            'data_validation': bool(test_data['segmento'] and test_data['produto']),
            'orchestrator_available': super_orchestrator is not None,
            'services_count': len(super_orchestrator.services) if super_orchestrator else 0
        }
        
        return jsonify({
            'success': True,
            'test_data': test_data,
            'test_results': test_results,
            'message': 'Teste básico concluído'
        })

    except Exception as e:
        logger.error(f"❌ Erro no teste básico: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@debug_bp.route('/clear-sessions', methods=['POST'])
def clear_debug_sessions():
    """Limpa sessões de debug (apenas para desenvolvimento)"""
    try:
        if super_orchestrator:
            cleared_sessions = len(super_orchestrator.execution_state)
            super_orchestrator.execution_state.clear()
            
            return jsonify({
                'success': True,
                'message': f'Limpas {cleared_sessions} sessões de debug',
                'cleared_count': cleared_sessions
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Super Orchestrator não disponível'
            }), 500

    except Exception as e:
        logger.error(f"❌ Erro ao limpar sessões: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
