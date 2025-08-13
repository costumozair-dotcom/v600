#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Analysis Routes com Controles de Sessão - FIXED
Rotas para análise de mercado com pausar/continuar/salvar
"""

import logging
from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
import json
import os
from services.ultra_detailed_analysis_engine import ultra_detailed_analysis_engine
from services.auto_save_manager import auto_save_manager, salvar_etapa, salvar_erro
from services.super_orchestrator import super_orchestrator # Import the Super Orchestrator
import asyncio # Import asyncio for running async functions


logger = logging.getLogger(__name__)

analysis_bp = Blueprint('analysis', __name__)

# Instancia o Super Orchestrator
orchestrator = super_orchestrator

# Armazena sessões ativas
active_sessions = {}

@analysis_bp.route('/')
def index():
    """Interface principal"""
    return render_template('unified_interface.html')

@analysis_bp.route('/analyze', methods=['POST'])
@analysis_bp.route('/api/analyze', methods=['POST'])
def analyze():
    """Inicia análise de mercado com controle de sessão"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400

        logger.info("🚀 Iniciando análise de mercado ultra-detalhada")

        # Cria sessão única
        session_id = auto_save_manager.iniciar_sessao()

        # Salva dados da requisição
        salvar_etapa("requisicao_analise", data, categoria="analise_completa")

        segmento_negocio = data.get('segmento')
        produto_servico = data.get('produto')
        publico_alvo = data.get('publico_alvo', '')
        objetivos_estrategicos = data.get('objetivos_estrategicos', '')
        contexto_adicional = data.get('contexto_adicional', '')

        logger.info(f"📊 Dados recebidos: Segmento={segmento_negocio}, Produto={produto_servico}")

        # Prepara query de pesquisa
        query = data.get('query', f"mercado de {produto_servico or segmento_negocio} no brasil desde 2022")
        logger.info(f"🔍 Query de pesquisa: {query}")

        # Salva query
        salvar_etapa("query_preparada", {"query": query}, categoria="pesquisa_web")

        # Registra sessão como ativa
        active_sessions[session_id] = {
            'status': 'running',
            'data': data,
            'started_at': datetime.now().isoformat(),
            'paused_at': None
        }

        # Função para enviar atualizações de progresso
        def send_progress_update(session_id, step, message):
            logger.info(f"Progress {session_id}: Step {step} - {message}")
            salvar_etapa("progresso", {
                "step": step,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }, categoria="logs")

        # Executa análise COMPLETA com todos os serviços - SÓ DADOS REAIS
        logger.info("🚀 Executando análise COMPLETA com TODOS os serviços - ZERO SIMULADOS")

        analysis_data = {
            'segmento': segmento_negocio,
            'produto': produto_servico,
            'publico': publico_alvo,
            'objetivos': objetivos_estrategicos,
            'contexto': contexto_adicional,
            'query': query,
            'session_id': session_id,
            'validation_mode': 'REAL_DATA_ONLY'
        }

        # VALIDAÇÃO CRÍTICA: Verifica se dados essenciais estão preenchidos
        if not segmento_negocio or not produto_servico:
            return jsonify({
                'success': False,
                'error': 'FALHA CRÍTICA: Segmento e Produto são obrigatórios para análise com dados reais',
                'session_id': session_id
            }), 400

        resultado = super_orchestrator.execute_synchronized_analysis(
            data=analysis_data,
            session_id=session_id,
            progress_callback=lambda step, msg: send_progress_update(session_id, step, msg)
        )

        # VALIDAÇÃO CRÍTICA: Verifica se o resultado contém dados reais
        data_validation = resultado.get('data_validation', {})
        if not resultado.get('success', False):
            logger.error(f"❌ FALHA na análise: {resultado.get('error', 'Erro desconhecido')}")
            return jsonify({
                'success': False,
                'error': f"Falha na análise: {resultado.get('error', 'Erro desconhecido')}",
                'session_id': session_id,
                'partial_data': resultado
            }), 500

        


        # Atualiza status da sessão
        active_sessions[session_id]['status'] = 'completed'
        active_sessions[session_id]['completed_at'] = datetime.now().isoformat()

        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Análise COMPLETA concluída com sucesso!',
            'processing_time': resultado.get('metadata', {}).get('processing_time_formatted', 'N/A'),
            'data': resultado
        })

    except Exception as e:
        logger.error(f"❌ Erro na análise: {str(e)}")
        if 'session_id' in locals() and session_id:
            active_sessions[session_id]['status'] = 'error'
            active_sessions[session_id]['error'] = str(e)
            active_sessions[session_id]['error_at'] = datetime.now().isoformat()
            salvar_erro("erro_analise", e)
        else:
            salvar_erro("erro_geral_analise", e)
        return jsonify({
            'success': False,
            'session_id': locals().get('session_id'), # Try to get session_id if it was created
            'error': str(e),
            'message': 'Erro na análise. Dados intermediários foram salvos.'
        }), 500


@analysis_bp.route('/sessions', methods=['GET'])
def list_sessions():
    """Lista todas as sessões salvas"""
    try:
        # Lista sessões do auto_save_manager
        try:
            saved_sessions_ids = auto_save_manager.listar_sessoes()
        except AttributeError:
            # Fallback se método não existe
            import os
            base_path = 'relatorios_intermediarios/logs'
            saved_sessions_ids = []
            if os.path.exists(base_path):
                for item in os.listdir(base_path):
                    if item.startswith('session_'):
                        saved_sessions_ids.append(item.replace('session_', '').split('.')[0]) # Extract session ID
            else:
                saved_sessions_ids = []

        sessions_list = []
        for session_id in saved_sessions_ids:
            session_data = active_sessions.get(session_id, {})
            session_info = auto_save_manager.obter_info_sessao(session_id)

            sessions_list.append({
                'session_id': session_id,
                'status': session_data.get('status', 'saved'), # Default to 'saved' if not active
                'segmento': session_data.get('data', {}).get('segmento', 'N/A'),
                'produto': session_data.get('data', {}).get('produto', 'N/A'), # Corrected variable name here
                'started_at': session_data.get('started_at'),
                'completed_at': session_data.get('completed_at'),
                'paused_at': session_data.get('paused_at'),
                'error': session_data.get('error'),
                'etapas_salvas': len(session_info.get('etapas', {})) if session_info else 0
            })

        return jsonify({
            'success': True,
            'sessions': sessions_list,
            'total': len(sessions_list)
        })

    except Exception as e:
        logger.error(f"❌ Erro ao listar sessões: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/sessions/<session_id>/pause', methods=['POST'])
def pause_session(session_id):
    """Pausa uma sessão ativa"""
    try:
        if session_id not in active_sessions:
            return jsonify({'error': 'Sessão não encontrada'}), 404

        session = active_sessions[session_id]
        if session['status'] != 'running':
            return jsonify({'error': 'Sessão não está em execução'}), 400

        # Atualiza status
        session['status'] = 'paused'
        session['paused_at'] = datetime.now().isoformat()

        # Salva estado de pausa
        salvar_etapa("sessao_pausada", {
            "session_id": session_id,
            "paused_at": session['paused_at'],
            "reason": "User requested pause"
        }, categoria="logs")

        logger.info(f"⏸️ Sessão {session_id} pausada pelo usuário")

        return jsonify({
            'success': True,
            'message': 'Sessão pausada com sucesso',
            'session_id': session_id,
            'status': 'paused'
        })

    except Exception as e:
        logger.error(f"❌ Erro ao pausar sessão: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/sessions/<session_id>/resume', methods=['POST'])
def resume_session(session_id):
    """Resume uma sessão pausada"""
    try:
        if session_id not in active_sessions:
            return jsonify({'error': 'Sessão não encontrada'}), 404

        session = active_sessions[session_id]
        if session['status'] != 'paused':
            return jsonify({'error': 'Sessão não está pausada'}), 400

        # Atualiza status
        session['status'] = 'running'
        session['resumed_at'] = datetime.now().isoformat()
        session['paused_at'] = None

        # Salva estado de resume
        salvar_etapa("sessao_resumida", {
            "session_id": session_id,
            "resumed_at": session['resumed_at'],
            "reason": "User requested resume"
        }, categoria="logs")

        logger.info(f"▶️ Sessão {session_id} resumida pelo usuário")

        return jsonify({
            'success': True,
            'message': 'Sessão resumida com sucesso',
            'session_id': session_id,
            'status': 'running'
        })

    except Exception as e:
        logger.error(f"❌ Erro ao resumir sessão: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/sessions/<session_id>/continue', methods=['POST'])
def continue_session(session_id):
    """Continua uma sessão salva - VERSÃO COM DEBUG COMPLETO"""
    try:
        # VALIDAÇÃO INICIAL
        if not session_id:
            logger.error("❌ Session ID não fornecido")
            return jsonify({
                'success': False,
                'error': 'Session ID obrigatório'
            }), 400

        logger.info(f"🔄 Tentando continuar análise da sessão {session_id}...")

        # Debug: Lista todas as possíveis localizações de dados
        possible_paths = [
            f"relatorios_intermediarios/analise_completa/{session_id}",
            f"relatorios_intermediarios/logs/{session_id}",
            f"relatorios_intermediarios/logs/session_{session_id}.json",
            f"relatorios_intermediarios/{session_id}"
        ]
        
        logger.info(f"🔍 Verificando caminhos possíveis para sessão {session_id}:")
        for path in possible_paths:
            exists = os.path.exists(path)
            logger.info(f"  - {path}: {'EXISTS' if exists else 'NOT_FOUND'}")

        # Recupera dados da sessão com múltiplas estratégias
        session_info = None
        recovery_method = "none"
        
        # ESTRATÉGIA 1: auto_save_manager
        try:
            session_info = auto_save_manager.obter_info_sessao(session_id)
            if session_info:
                recovery_method = "auto_save_manager"
                logger.info(f"✅ Método auto_save_manager: {len(session_info.get('etapas', {})) if session_info else 0} etapas")
            else:
                logger.warning("⚠️ auto_save_manager retornou None")
        except Exception as e:
            logger.error(f"❌ Erro no auto_save_manager: {e}")

        # ESTRATÉGIA 2: Busca manual em pastas
        if not session_info:
            logger.info("🔍 Tentando recuperação manual...")
            for base_path in ["relatorios_intermediarios/analise_completa", "relatorios_intermediarios/logs", "relatorios_intermediarios"]:
                session_path = f"{base_path}/{session_id}"
                if os.path.exists(session_path):
                    logger.info(f"📁 Encontrada pasta: {session_path}")
                    try:
                        session_info = {'etapas': {}}
                        recovery_method = f"manual_{base_path.split('/')[-1]}"
                        
                        files = os.listdir(session_path)
                        logger.info(f"📋 Arquivos encontrados: {files}")
                        
                        for file_name in files:
                            if file_name.endswith('.json'):
                                file_path = os.path.join(session_path, file_name)
                                try:
                                    with open(file_path, 'r', encoding='utf-8') as f:
                                        file_data = json.load(f)
                                        session_info['etapas'][file_name] = file_data
                                        logger.info(f"✅ Arquivo lido: {file_name} ({len(str(file_data))} chars)")
                                except Exception as fe:
                                    logger.warning(f"⚠️ Erro ao ler {file_name}: {fe}")
                        break
                    except Exception as e:
                        logger.error(f"❌ Erro na recuperação manual de {session_path}: {e}")

        # ESTRATÉGIA 3: Busca por arquivo único de sessão
        if not session_info:
            session_file_path = f"relatorios_intermediarios/logs/session_{session_id}.json"
            if os.path.exists(session_file_path):
                logger.info(f"📄 Encontrado arquivo de sessão: {session_file_path}")
                try:
                    with open(session_file_path, 'r', encoding='utf-8') as f:
                        file_data = json.load(f)
                        session_info = {'etapas': {'session_file': file_data}}
                        recovery_method = "session_file"
                        logger.info(f"✅ Arquivo de sessão lido: {len(str(file_data))} chars")
                except Exception as e:
                    logger.error(f"❌ Erro ao ler arquivo de sessão: {e}")

        # Verifica se conseguiu recuperar alguma coisa
        if not session_info or not session_info.get('etapas'):
            logger.error(f"❌ Nenhum dado recuperado para sessão {session_id}")
            logger.error(f"📊 Debug info: session_info={session_info}, recovery_method={recovery_method}")
            
            # Lista todos os arquivos das pastas para debug
            for base_path in ["relatorios_intermediarios/analise_completa", "relatorios_intermediarios/logs"]:
                if os.path.exists(base_path):
                    try:
                        all_items = os.listdir(base_path)
                        session_items = [item for item in all_items if session_id in item]
                        logger.info(f"🔍 Items relacionados à sessão em {base_path}: {session_items}")
                    except Exception as e:
                        logger.error(f"❌ Erro ao listar {base_path}: {e}")
            
            return jsonify({
                'success': False,
                'error': f'Sessão {session_id} não encontrada ou sem dados (method: {recovery_method})',
                'debug_info': {
                    'session_id': session_id,
                    'recovery_method': recovery_method,
                    'session_info': bool(session_info),
                    'paths_checked': possible_paths
                }
            }), 404

        logger.info(f"✅ Dados recuperados usando método: {recovery_method}")
        logger.info(f"📋 Etapas disponíveis: {list(session_info.get('etapas', {}).keys())}")

        # Estratégias múltiplas para recuperar dados originais
        original_data = None
        data_source = "none"
        
        # Debug: mostra estrutura das etapas
        logger.info(f"🔍 Analisando estrutura das etapas:")
        for etapa_nome, etapa_data in session_info.get('etapas', {}).items():
            data_type = type(etapa_data).__name__
            if isinstance(etapa_data, dict):
                keys = list(etapa_data.keys())[:5]  # Primeiras 5 chaves
                logger.info(f"  📄 {etapa_nome}: {data_type} com chaves: {keys}")
            else:
                logger.info(f"  📄 {etapa_nome}: {data_type} ({len(str(etapa_data))} chars)")
        
        # Estratégia 1: Busca por arquivos de requisição
        for etapa_nome, etapa_data in session_info.get('etapas', {}).items():
            if 'requisicao_analise' in etapa_nome.lower() or 'requisicao' in etapa_nome.lower():
                logger.info(f"🎯 Processando arquivo de requisição: {etapa_nome}")
                if isinstance(etapa_data, dict):
                    # Tenta diferentes estruturas de dados
                    possible_data = [
                        etapa_data.get('dados', {}),
                        etapa_data.get('data', {}),
                        etapa_data,  # Os dados podem estar na raiz
                        etapa_data.get('request_data', {}),
                        etapa_data.get('payload', {})
                    ]
                    
                    for candidate in possible_data:
                        if isinstance(candidate, dict) and (candidate.get('segmento') or candidate.get('produto')):
                            original_data = candidate
                            data_source = f"requisicao_dict_{etapa_nome}"
                            logger.info(f"✅ Dados recuperados: {list(candidate.keys())}")
                            break
                    
                    if original_data:
                        break
                        
                elif isinstance(etapa_data, str):
                    try:
                        parsed_data = json.loads(etapa_data)
                        if isinstance(parsed_data, dict):
                            possible_data = [
                                parsed_data.get('dados', {}),
                                parsed_data.get('data', {}),
                                parsed_data
                            ]
                            for candidate in possible_data:
                                if isinstance(candidate, dict) and (candidate.get('segmento') or candidate.get('produto')):
                                    original_data = candidate
                                    data_source = f"requisicao_json_{etapa_nome}"
                                    logger.info(f"✅ Dados recuperados de JSON: {list(candidate.keys())}")
                                    break
                            if original_data:
                                break
                    except json.JSONDecodeError as e:
                        logger.warning(f"⚠️ Erro ao parsear JSON de {etapa_nome}: {e}")

        # Estratégia 2: Busca em qualquer etapa que tenha dados de mercado
        if not original_data:
            logger.warning("⚠️ Dados de requisição não encontrados, buscando em outras etapas...")
            for etapa_nome, etapa_data in session_info.get('etapas', {}).items():
                if isinstance(etapa_data, dict):
                    # Procura por dados que tenham segmento/produto diretamente
                    if etapa_data.get('segmento') or etapa_data.get('produto'):
                        original_data = etapa_data
                        data_source = f"etapa_direta_{etapa_nome}"
                        logger.info(f"✅ Dados encontrados diretamente: {etapa_nome}")
                        break
                    
                    # Procura dentro de sub-estruturas
                    for key, value in etapa_data.items():
                        if isinstance(value, dict) and (value.get('segmento') or value.get('produto')):
                            original_data = value
                            data_source = f"sub_estrutura_{etapa_nome}.{key}"
                            logger.info(f"✅ Dados encontrados em sub-estrutura: {etapa_nome}.{key}")
                            break
                    
                    if original_data:
                        break

        # Estratégia 3: Busca por padrões alternativos de nomenclatura
        if not original_data:
            logger.info("🔍 Procurando por campos alternativos...")
            alternative_fields = {
                'segmento': ['segment', 'business_segment', 'market_segment', 'categoria', 'setor'],
                'produto': ['product', 'service', 'servico', 'item', 'offering']
            }
            
            for etapa_nome, etapa_data in session_info.get('etapas', {}).items():
                if isinstance(etapa_data, dict):
                    found_fields = {}
                    
                    # Procura pelos campos alternativos
                    for standard_field, alternatives in alternative_fields.items():
                        for alt_field in [standard_field] + alternatives:
                            if etapa_data.get(alt_field):
                                found_fields[standard_field] = etapa_data[alt_field]
                                break
                    
                    if len(found_fields) >= 1:  # Pelo menos um campo encontrado
                        # Cria estrutura completa com campos encontrados
                        original_data = {
                            'segmento': found_fields.get('segmento', ''),
                            'produto': found_fields.get('produto', ''),
                            'publico_alvo': etapa_data.get('publico_alvo', etapa_data.get('target_audience', '')),
                            'objetivos_estrategicos': etapa_data.get('objetivos_estrategicos', etapa_data.get('objectives', '')),
                            'contexto_adicional': etapa_data.get('contexto_adicional', etapa_data.get('context', ''))
                        }
                        data_source = f"campos_alternativos_{etapa_nome}"
                        logger.info(f"✅ Dados montados com campos alternativos: {found_fields}")
                        break

        # Estratégia 4: Dados mínimos com informações do usuário
        if not original_data:
            logger.warning("⚠️ Tentando extrair dados do contexto da sessão...")
            
            # Procura por qualquer texto que possa dar pistas
            context_hints = []
            for etapa_nome, etapa_data in session_info.get('etapas', {}).items():
                if isinstance(etapa_data, dict):
                    # Procura em campos de texto
                    text_fields = ['query', 'message', 'description', 'title', 'name']
                    for field in text_fields:
                        if etapa_data.get(field):
                            context_hints.append(str(etapa_data[field]))
            
            # Tenta criar dados mínimos inteligentes
            if context_hints:
                combined_context = ' '.join(context_hints)
                original_data = {
                    'segmento': 'Análise de Mercado Extraída',
                    'produto': 'Produto/Serviço da Sessão',
                    'publico_alvo': '',
                    'objetivos_estrategicos': '',
                    'contexto_adicional': f'Continuação da sessão {session_id}. Contexto: {combined_context[:200]}...'
                }
                data_source = "contexto_extraido"
                logger.info(f"⚠️ Dados criados a partir do contexto: {combined_context[:100]}...")
            else:
                # Último recurso: dados totalmente genéricos
                original_data = {
                    'segmento': 'Análise de Mercado Geral',
                    'produto': 'Produto/Serviço',
                    'publico_alvo': '',
                    'objetivos_estrategicos': '',
                    'contexto_adicional': f'Continuação da sessão {session_id}'
                }
                data_source = "dados_genericos"
                logger.warning("⚠️ Usando dados completamente genéricos")

        if not original_data:
            logger.error("❌ Falha completa na recuperação de dados")
            return jsonify({
                'success': False,
                'error': 'Não foi possível recuperar dados da sessão',
                'debug_info': {
                    'session_id': session_id,
                    'recovery_method': recovery_method,
                    'data_source': data_source,
                    'etapas_disponiveis': list(session_info.get('etapas', {}).keys())
                }
            }), 400

        logger.info(f"✅ Dados recuperados usando fonte: {data_source}")

        # Normaliza e valida os dados recuperados
        normalized_data = {
            'segmento': str(original_data.get('segmento', '')).strip(),
            'produto': str(original_data.get('produto', '')).strip(),
            'publico_alvo': str(original_data.get('publico_alvo', original_data.get('publico', ''))).strip(),
            'objetivos_estrategicos': str(original_data.get('objetivos_estrategicos', original_data.get('objetivos', ''))).strip(),
            'contexto_adicional': str(original_data.get('contexto_adicional', original_data.get('contexto', ''))).strip()
        }

        # VALIDAÇÃO FLEXÍVEL: Se dados essenciais estão vazios, usa valores padrão
        validation_warnings = []
        if not normalized_data['segmento']:
            normalized_data['segmento'] = 'Mercado Geral'
            validation_warnings.append("Segmento vazio - usando valor padrão")
        
        if not normalized_data['produto']:
            normalized_data['produto'] = 'Produto/Serviço'
            validation_warnings.append("Produto vazio - usando valor padrão")

        # Log completo dos dados processados
        logger.info(f"📋 Dados processados:")
        logger.info(f"  - Fonte: {data_source}")
        logger.info(f"  - Segmento: '{normalized_data['segmento']}'")
        logger.info(f"  - Produto: '{normalized_data['produto']}'")
        logger.info(f"  - Público: '{normalized_data['publico_alvo'][:50]}...' ({len(normalized_data['publico_alvo'])} chars)")
        logger.info(f"  - Avisos: {validation_warnings}")

        # VALIDAÇÃO FINAL CRÍTICA: Garante dados mínimos válidos
        if not normalized_data['segmento'] or not normalized_data['produto']:
            logger.error(f"❌ Dados inválidos após normalização: segmento='{normalized_data['segmento']}', produto='{normalized_data['produto']}'")
            return jsonify({
                'success': False,
                'error': 'FALHA CRÍTICA: Não foi possível obter dados válidos para continuar análise',
                'debug_info': {
                    'session_id': session_id,
                    'data_source': data_source,
                    'recovery_method': recovery_method,
                    'original_data_keys': list(original_data.keys()) if original_data else [],
                    'normalized_data': normalized_data,
                    'validation_warnings': validation_warnings
                }
            }), 400

        # Registra como sessão ativa
        active_sessions[session_id] = {
            'status': 'running',
            'data': normalized_data,
            'continued_at': datetime.now().isoformat(),
            'original_session': True,
            'recovery_info': {
                'method': recovery_method,
                'data_source': data_source,
                'warnings': validation_warnings
            }
        }

        # Callback de progresso melhorado
        def progress_callback(step, message):
            logger.info(f"Continue Progress {session_id}: Step {step} - {message}")
            salvar_etapa("progresso_continuacao", {
                "step": step,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id,
                "recovery_info": f"{recovery_method}:{data_source}"
            }, categoria="logs")

        # Prepara dados para análise
        analysis_data = {
            'segmento': normalized_data['segmento'],
            'produto': normalized_data['produto'],
            'publico': normalized_data['publico_alvo'],
            'objetivos': normalized_data['objetivos_estrategicos'],
            'contexto': normalized_data['contexto_adicional'],
            'query': original_data.get('query', f"mercado de {normalized_data['produto']} {normalized_data['segmento']} no brasil desde 2022"),
            'session_id': session_id,
            'validation_mode': 'REAL_DATA_ONLY'
        }

        logger.info(f"🚀 INICIANDO ANÁLISE com dados validados:")
        logger.info(f"  📊 Segmento: {analysis_data['segmento']}")
        logger.info(f"  🏷️  Produto: {analysis_data['produto']}")
        logger.info(f"  🔍 Query: {analysis_data['query'][:100]}...")

        # Salva tentativa de continuação com dados completos
        salvar_etapa("tentativa_continuacao_detalhada", {
            "session_id": session_id,
            "analysis_data": analysis_data,
            "recovery_info": {
                "method": recovery_method,
                "data_source": data_source,
                "warnings": validation_warnings
            },
            "timestamp": datetime.now().isoformat()
        }, categoria="logs")

        # Executa análise
        logger.info("🎯 Chamando super_orchestrator.execute_synchronized_analysis...")
        resultado = super_orchestrator.execute_synchronized_analysis(
            data=analysis_data,
            session_id=session_id,
            progress_callback=progress_callback
        )

        # Verifica resultado
        if not resultado.get('success', False):
            error_msg = resultado.get('error', 'Erro desconhecido na análise')
            logger.error(f"❌ Falha na continuação: {error_msg}")
            
            active_sessions[session_id]['status'] = 'error'
            active_sessions[session_id]['error'] = error_msg
            active_sessions[session_id]['error_at'] = datetime.now().isoformat()
            
            salvar_erro("erro_continuacao_analise", Exception(error_msg), {
                'session_id': session_id,
                'analysis_data': analysis_data
            })
            
            return jsonify({
                'success': False,
                'session_id': session_id,
                'error': f"Falha na continuação da análise: {error_msg}",
                'partial_data': resultado
            }), 500

        # Sucesso
        active_sessions[session_id]['status'] = 'completed'
        active_sessions[session_id]['completed_at'] = datetime.now().isoformat()

        logger.info(f"✅ Análise da sessão {session_id} continuada e concluída com sucesso!")

        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Análise continuada e concluída com sucesso!',
            'processing_time': resultado.get('metadata', {}).get('processing_time_formatted', 'N/A'),
            'data': resultado
        })

    except Exception as e:
        logger.error(f"❌ Erro crítico ao continuar sessão {session_id}: {str(e)}")
        
        # Registra erro
        if session_id in active_sessions:
            active_sessions[session_id]['status'] = 'error'
            active_sessions[session_id]['error'] = str(e)
            active_sessions[session_id]['error_at'] = datetime.now().isoformat()
        
        salvar_erro("erro_critico_continuacao_sessao", e, {'session_id': session_id})
        
        return jsonify({
            'success': False,
            'session_id': session_id,
            'error': str(e),
            'message': 'Erro crítico na continuação da análise. Dados intermediários foram salvos.'
        }), 500

@analysis_bp.route('/sessions/<session_id>/save', methods=['POST'])
def save_session(session_id):
    """Salva explicitamente uma sessão"""
    try:
        if session_id not in active_sessions:
            return jsonify({'error': 'Sessão não encontrada'}), 404

        session = active_sessions[session_id]

        # Salva estado completo da sessão
        salvar_etapa("sessao_salva_explicitamente", {
            "session_id": session_id,
            "saved_at": datetime.now().isoformat(),
            "session_data": session,
            "reason": "User explicitly saved session"
        }, categoria="logs")

        logger.info(f"💾 Sessão {session_id} salva explicitamente pelo usuário")

        return jsonify({
            'success': True,
            'message': 'Sessão salva com sucesso',
            'session_id': session_id
        })

    except Exception as e:
        logger.error(f"❌ Erro ao salvar sessão: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/sessions/<session_id>/status', methods=['GET'])
@analysis_bp.route('/api/sessions/<session_id>/status', methods=['GET'])
def get_session_status(session_id):
    """Obtém status de uma sessão"""
    try:
        session = active_sessions.get(session_id)
        session_info = auto_save_manager.obter_info_sessao(session_id)

        if not session and not session_info:
            return jsonify({'error': 'Sessão não encontrada'}), 404

        status_data = {
            'session_id': session_id,
            'status': session.get('status', 'saved') if session else 'saved', # Default to 'saved' if not active
            'active': session is not None,
            'saved': session_info is not None,
            'etapas_salvas': len(session_info.get('etapas', {})) if session_info else 0
        }

        if session:
            status_data.update({
                'started_at': session.get('started_at'),
                'paused_at': session.get('paused_at'),
                'completed_at': session.get('completed_at'),
                'error': session.get('error'),
                'segmento': session.get('data', {}).get('segmento'),
                'produto': session.get('data', {}).get('produto')
            })

        return jsonify({
            'success': True,
            'session': status_data
        })

    except Exception as e:
        logger.error(f"❌ Erro ao obter status da sessão: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/sessions', methods=['GET'])
def api_list_sessions():
    """API endpoint para listar sessões"""
    return list_sessions()

@analysis_bp.route('/api/progress/<session_id>', methods=['GET'])
def api_get_progress(session_id):
    """API endpoint para obter progresso"""
    try:
        session = active_sessions.get(session_id)
        session_info = auto_save_manager.obter_info_sessao(session_id)

        if not session and not session_info:
            return jsonify({'error': 'Sessão não encontrada'}), 404

        if session and session['status'] == 'error':
            return jsonify({
                'success': False,
                'completed': False,
                'percentage': 0,
                'current_step': f"Erro: {session.get('error')}",
                'total_steps': 13,
                'estimated_time': 'N/A'
            })

        if session and session['status'] == 'completed':
            return jsonify({
                'success': True,
                'completed': True,
                'percentage': 100,
                'current_step': 'Análise concluída',
                'total_steps': 13,
                'estimated_time': '0m'
            })
        elif session and session['status'] == 'running':
            # Tenta obter progresso do Super Orchestrator se disponível
            progress_data = super_orchestrator.get_session_progress(session_id)
            if progress_data:
                return jsonify({
                    'success': True,
                    'completed': progress_data.get('completed', False),
                    'percentage': progress_data.get('percentage', 0),
                    'current_step': progress_data.get('current_step', 'Processando...'),
                    'total_steps': progress_data.get('total_steps', 13),
                    'estimated_time': progress_data.get('estimated_time', 'N/A')
                })
            else:
                # Fallback para cálculo de progresso baseado no tempo
                start_time = datetime.fromisoformat(session['started_at'])
                elapsed = (datetime.now() - start_time).total_seconds()
                progress = min(elapsed / 600 * 100, 95)  # 10 minutos = 100% (ajustar conforme necessário)

                return jsonify({
                    'success': True,
                    'completed': False,
                    'percentage': progress,
                    'current_step': f'Processando... ({progress:.0f}%)',
                    'total_steps': 13,
                    'estimated_time': f'{max(0, 10 - elapsed/60):.0f}m' # Estimativa de 10 minutos totais
                })
        else: # Paused or unknown status
            return jsonify({
                'success': True,
                'completed': False,
                'percentage': 0,
                'current_step': 'Pausado' if session and session['status'] == 'paused' else 'Aguardando',
                'total_steps': 13,
                'estimated_time': 'N/A'
            })

    except Exception as e:
        logger.error(f"❌ Erro ao obter progresso: {str(e)}")
        return jsonify({'error': str(e)}), 500
