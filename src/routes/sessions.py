
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rotas para gerenciamento de sessões e resultados
"""

from flask import Blueprint, jsonify, request
import os
import json
import logging
from services.auto_save_manager import salvar_etapa

logger = logging.getLogger(__name__)

sessions_bp = Blueprint('sessions', __name__)

@sessions_bp.route('/sessions', methods=['GET'])
def list_sessions():
    """Lista todas as sessões disponíveis"""
    try:
        sessions_dir = "relatorios_intermediarios/logs"
        sessions = []
        
        if os.path.exists(sessions_dir):
            for session_folder in os.listdir(sessions_dir):
                if session_folder.startswith('session_'):
                    session_path = os.path.join(sessions_dir, session_folder)
                    if os.path.isdir(session_path):
                        # Pega informações básicas da sessão
                        metadata_files = [f for f in os.listdir(session_path) if f.startswith('session_metadata')]
                        if metadata_files:
                            sessions.append({
                                'id': session_folder,
                                'created_at': metadata_files[0].split('_')[-1].replace('.txt', ''),
                                'status': 'completed' if any(f.startswith('progresso') for f in os.listdir(session_path)) else 'active'
                            })
        
        return jsonify({
            'success': True,
            'sessions': sessions
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar sessões: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sessions_bp.route('/sessions/<session_id>/status', methods=['GET'])
def get_session_status(session_id):
    """Obtém o status de uma sessão específica"""
    try:
        session_path = f"relatorios_intermediarios/logs/{session_id}"
        
        if not os.path.exists(session_path):
            return jsonify({
                'success': False,
                'error': 'Sessão não encontrada'
            }), 404
        
        # Busca arquivos de progresso
        progress_files = []
        for file in os.listdir(session_path):
            if file.startswith('progresso_'):
                progress_files.append(file)
        
        progress_files.sort()  # Ordena por timestamp
        
        status = 'completed' if progress_files else 'active'
        last_update = progress_files[-1] if progress_files else None
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'status': status,
            'last_update': last_update,
            'progress_count': len(progress_files)
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter status da sessão {session_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sessions_bp.route('/sessions/<session_id>/results', methods=['GET'])
def get_session_results(session_id):
    """Obtém os resultados finais de uma sessão"""
    try:
        # Busca pelo arquivo de análise final
        analysis_path = f"relatorios_intermediarios/analise_completa/{session_id}"
        
        # Se não existir, tenta buscar qualquer arquivo JSON na pasta da sessão
        if not os.path.exists(analysis_path):
            # Tenta buscar arquivos na pasta de logs da sessão
            logs_path = f"relatorios_intermediarios/logs/{session_id}"
            if os.path.exists(logs_path):
                # Busca por arquivos de progresso ou análise
                for file in os.listdir(logs_path):
                    if 'analise' in file.lower() and file.endswith('.json'):
                        # Lê o arquivo JSON mais recente
                        file_path = os.path.join(logs_path, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            results = json.load(f)
                        
                        return jsonify({
                            'success': True,
                            'session_id': session_id,
                            'results': results,
                            'file': file,
                            'source': 'logs'
                        })
            
            return jsonify({
                'success': False,
                'error': 'Resultados não encontrados'
            }), 404
        
        # Procura pelo arquivo final
        final_files = []
        for file in os.listdir(analysis_path):
            if ('final' in file.lower() or 'analise' in file.lower()) and file.endswith('.json'):
                final_files.append(file)
        
        if not final_files:
            return jsonify({
                'success': False,
                'error': 'Análise ainda não finalizada'
            }), 404
        
        # Pega o arquivo mais recente
        final_files.sort()
        final_file = final_files[-1]
        
        with open(os.path.join(analysis_path, final_file), 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'results': results,
            'file': final_file
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter resultados da sessão {session_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sessions_bp.route('/sessions/<session_id>/progress', methods=['GET'])
def get_session_progress(session_id):
    """Obtém o progresso detalhado de uma sessão"""
    try:
        session_path = f"relatorios_intermediarios/logs/{session_id}"
        
        if not os.path.exists(session_path):
            return jsonify({
                'success': False,
                'error': 'Sessão não encontrada'
            }), 404
        
        # Coleta todos os arquivos de progresso
        progress_files = []
        for file in os.listdir(session_path):
            if file.startswith('progresso_'):
                file_path = os.path.join(session_path, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    progress_files.append({
                        'timestamp': file.replace('progresso_', '').replace('.txt', ''),
                        'content': content,
                        'step': len(progress_files) + 1
                    })
        
        progress_files.sort(key=lambda x: x['timestamp'])
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'progress': progress_files,
            'total_steps': len(progress_files)
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter progresso da sessão {session_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
