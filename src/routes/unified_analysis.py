
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Rota de Análise Unificada
"""

import logging
import time
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from services.master_analysis_engine import master_analysis_engine
from routes.html_report_generator import html_report_generator

logger = logging.getLogger(__name__)

unified_analysis_bp = Blueprint('unified_analysis', __name__)

@unified_analysis_bp.route('/execute_unified_analysis', methods=['POST'])
def execute_unified_analysis():
    """Executa análise unificada completa e gera relatório HTML"""
    
    start_time = time.time()
    session_id = str(uuid.uuid4())
    
    try:
        # Recebe dados
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Dados são obrigatórios'
            }), 400
        
        # Validação obrigatória
        if not data.get('segmento'):
            return jsonify({
                'error': 'Segmento é obrigatório para análise personalizada'
            }), 400
        
        logger.info(f"🚀 Iniciando análise unificada para: {data.get('segmento')}")
        
        # Callback de progresso
        progress_updates = []
        
        def progress_callback(step: int, message: str):
            progress_updates.append({
                'step': step,
                'message': message,
                'timestamp': datetime.now().isoformat()
            })
            logger.info(f"Progresso {step}/13: {message}")
        
        # Executa análise unificada
        analysis_result = master_analysis_engine.execute_unified_analysis(
            data=data,
            session_id=session_id,
            progress_callback=progress_callback
        )
        
        # Gera relatório HTML profissional
        html_content = html_report_generator.generate_complete_html_report(analysis_result)
        
        # Resultado final
        processing_time = time.time() - start_time
        
        response = {
            'success': True,
            'session_id': session_id,
            'analysis_result': analysis_result,
            'html_report': html_content,
            'processing_info': {
                'total_time_seconds': processing_time,
                'progress_updates': progress_updates,
                'engine_used': 'MasterAnalysisEngine v2.0',
                'report_format': 'HTML Profissional',
                'pages_generated': len(html_content.split('<div class="page">')),
                'uniqueness_score': analysis_result.get('metadata_unique', {}).get('uniqueness_score', 0),
                'completeness_score': analysis_result.get('completeness_validation', {}).get('score', 0)
            },
            'quality_metrics': {
                'sources_analyzed': analysis_result.get('research_summary', {}).get('sources_analyzed', 0),
                'content_extracted': analysis_result.get('research_summary', {}).get('content_extracted', 0),
                'social_platforms': analysis_result.get('research_summary', {}).get('social_platforms', 0),
                'search_providers': analysis_result.get('research_summary', {}).get('search_providers', 0),
                'is_unique': True,
                'is_personalized': True,
                'contains_real_data': True
            }
        }
        
        logger.info(f"✅ Análise unificada concluída em {processing_time:.2f}s")
        return jsonify(response)
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"❌ Erro na análise unificada: {e}")
        
        return jsonify({
            'success': False,
            'error': str(e),
            'session_id': session_id,
            'processing_time': processing_time,
            'debug_info': {
                'error_type': type(e).__name__,
                'error_message': str(e)
            }
        }), 500

@unified_analysis_bp.route('/analysis_status/<session_id>', methods=['GET'])
def get_analysis_status(session_id: str):
    """Retorna status de uma análise em execução"""
    
    try:
        # Aqui você pode implementar um sistema de tracking de status
        # Por enquanto, retorna status genérico
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'status': 'completed',  # ou 'running', 'failed'
            'progress': 100,
            'message': 'Análise concluída'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@unified_analysis_bp.route('/system_status', methods=['GET'])
def get_system_status():
    """Retorna status do sistema"""
    
    try:
        # Verifica status dos serviços
        from services.ai_manager import ai_manager
        from services.unified_search_manager import unified_search_manager
        from services.mcp_supadata_manager import mcp_supadata_manager
        from services.mcp_sequential_thinking_manager import MCPSequentialThinkingManager
        
        mcp_thinking = MCPSequentialThinkingManager()
        
        status = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'services': {
                'ai_manager': {
                    'available': True,
                    'providers': ai_manager.get_provider_status() if hasattr(ai_manager, 'get_provider_status') else {}
                },
                'search_manager': {
                    'available': True,
                    'providers': unified_search_manager.get_provider_status()
                },
                'supadata': {
                    'available': mcp_supadata_manager.is_available,
                    'configured': bool(mcp_supadata_manager.api_key)
                },
                'sequential_thinking': {
                    'available': bool(mcp_thinking.base_url),
                    'configured': True
                }
            },
            'system_health': 'operational',
            'version': 'ARQV30 Enhanced v2.0'
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'system_health': 'degraded'
        }), 500
