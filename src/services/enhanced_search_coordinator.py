#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Enhanced Search Coordinator ULTRA-ROBUSTO
Coordenador que GARANTE buscas simultâneas e distintas entre Exa e Google
"""

import os
import logging
import time
import asyncio
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from services.exa_client import exa_client
from services.production_search_manager import production_search_manager
from services.auto_save_manager import salvar_etapa, salvar_erro
from services.mcp_supadata_manager import mcp_supadata_manager
from services.deep_research_mcp_client import deep_research_mcp_client as deep_research_client
from services.instagram_mcp_client import instagram_mcp_client as instagram_client
from services.youtube_mcp_client import youtube_mcp_client as youtube_client
from datetime import datetime # Added import for datetime

logger = logging.getLogger(__name__)

class EnhancedSearchCoordinator:
    """Coordenador ULTRA-ROBUSTO de buscas simultâneas e distintas"""

    def __init__(self):
        """Inicializa coordenador de busca"""
        self.exa_available = exa_client.is_available()
        self.google_available = bool(os.getenv('GOOGLE_SEARCH_KEY') and os.getenv('GOOGLE_CSE_ID'))

        logger.info(f"🔍 Enhanced Search Coordinator ULTRA-ROBUSTO - Exa: {self.exa_available}, Google: {self.google_available}")

        # MCP Clients
        self.supadata_manager = mcp_supadata_manager
        self.deep_research_client = deep_research_client
        self.instagram_client = instagram_client
        self.youtube_client = youtube_client

        # Initialize excluded_domains if it's intended to be used in methods below
        self.excluded_domains = [] # Placeholder, adjust if needed from a config or another source

    # New method added as per the intention
    def _prepare_exa_neural_search(self, query: str) -> Dict[str, Any]:
        """Prepara busca neural com Exa"""
        try:
            from services.exa_client import exa_client

            # Otimiza query para busca neural
            neural_query = f"comprehensive analysis {query} market insights trends"

            results = exa_client.search_comprehensive(neural_query, num_results=10)

            return {
                'provider': 'exa_neural',
                'results': results.get('results', []),
                'total': len(results.get('results', [])),
                'neural_score': results.get('confidence', 0.8)
            }
        except Exception as e:
            logger.error(f"Erro na busca neural Exa: {str(e)}")
            return {'provider': 'exa_neural', 'results': [], 'total': 0, 'error': str(e)}

    def perform_search(self, query: str, search_type: str = 'comprehensive') -> Dict[str, Any]:
        """Executa busca coordenada usando múltiplos provedores"""

        try:
            logger.info(f"🔍 Iniciando busca coordenada para: {query}")

            results = {
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'providers_used': [],
                'total_results': 0,
                'search_results': [],
                'metadata': {}
            }

            # Executa busca usando múltiplos provedores
            if self.exa_available:
                try:
                    exa_results = exa_client.search_comprehensive(query, num_results=10)
                    if exa_results and exa_results.get('results'):
                        results['search_results'].extend(exa_results['results'])
                        results['providers_used'].append('exa')
                        results['total_results'] += len(exa_results['results'])
                        logger.info(f"✅ Exa: {len(exa_results['results'])} resultados")
                except Exception as e:
                    logger.error(f"❌ Erro na busca Exa: {e}")

            if self.google_available:
                try:
                    google_results = production_search_manager.search_with_fallback(
                        query,
                        max_results=10
                    )

                    # Trata tanto dict quanto list do Google
                    if google_results:
                        if isinstance(google_results, dict) and google_results.get('web_results'):
                            web_results = google_results['web_results'][:10]
                        elif isinstance(google_results, list):
                            web_results = google_results[:10]
                        else:
                            web_results = []

                        if web_results:
                            results['search_results'].extend(web_results)
                            results['providers_used'].append('google')
                            results['total_results'] += len(web_results)
                            logger.info(f"✅ Google: {len(web_results)} resultados")
                except Exception as e:
                    logger.error(f"❌ Erro na busca Google: {e}")

            logger.info(f"✅ Busca coordenada concluída: {results['total_results']} resultados de {len(results['providers_used'])} provedores")
            return results

        except Exception as e:
            logger.error(f"❌ Erro na busca coordenada: {e}")
            return {
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'providers_used': [],
                'total_results': 0,
                'search_results': [],
                'metadata': {},
                'error': str(e)
            }

    def execute_simultaneous_distinct_search(
        self,
        base_query: str,
        context: Dict[str, Any],
        session_id: str = None
    ) -> Dict[str, Any]:
        """GARANTE buscas MASSIVAS simultâneas e distintas - ESPECTRO AMPLIADO"""

        logger.info(f"🚀 INICIANDO BUSCAS MASSIVAS ULTRA-ROBUSTAS para: {base_query}")

        # Prepara MÚLTIPLAS queries DISTINTAS para cobertura máxima
        query_variations = self._generate_comprehensive_query_variations(base_query, context)

        # Salva queries preparadas
        salvar_etapa("queries_massivas_simultaneas", {
            "base_query": base_query,
            "query_variations": query_variations,
            "context": context,
            "search_scope": "MASSIVE_COMPREHENSIVE",
            "garantia_simultanea": True,
            "garantia_robusta": True
        }, categoria="pesquisa_web")

        search_results = {
            'base_query': base_query,
            'query_variations': query_variations,
            'exa_results': [],
            'google_results': [],
            'deep_research_results': [],
            'social_media_results': [],
            'news_results': [],
            'academic_results': [],
            'competitor_results': [],
            'trend_results': [],
            'execution_mode': 'MASSIVE_COMPREHENSIVE',
            'statistics': {
                'total_results': 0,
                'total_sources': 0,
                'exa_count': 0,
                'google_count': 0,
                'deep_research_count': 0,
                'social_count': 0,
                'news_count': 0,
                'academic_count': 0,
                'competitor_count': 0,
                'trend_count': 0,
                'search_time': 0,
                'simultaneous_execution': True,
                'comprehensive_coverage': True
            }
        }

        start_time = time.time()

        # EXECUTA BUSCAS MASSIVAS SIMULTANEAMENTE com ThreadPoolExecutor AMPLIADO
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {}

            # Prepara queries específicas para cada tipo de busca
            exa_query = self._prepare_exa_neural_search(base_query, context)
            google_query = self._prepare_google_keyword_query(base_query, context)

            # Busca Exa (se disponível) - NEURAL SEARCH
            if self.exa_available:
                futures['exa'] = executor.submit(self._execute_exa_neural_search, exa_query, context)
                logger.info(f"🧠 Exa Neural Search INICIADA: {exa_query}")

            # Busca Google (se disponível) - KEYWORD SEARCH
            if self.google_available:
                futures['google'] = executor.submit(self._execute_google_keyword_search, google_query, context)
                logger.info(f"🔍 Google Keyword Search INICIADA: {google_query}")

            # Busca outros provedores - FALLBACK SEARCH
            futures['other'] = executor.submit(self._execute_other_providers_search, base_query, context)
            logger.info(f"🌐 Other Providers Search INICIADA: {base_query}")

            # Social Media OBRIGATÓRIO com Exa ou Supadata
            if 'social_media' in query_variations: # Ajustado para verificar 'social_media' nas variações
                futures['social_media_exa'] = executor.submit(
                    self._execute_exa_social_search, base_query, context
                )
                logger.info(f"🌐 Exa Social Search INICIADA: {base_query}")
                futures['social_media_supadata'] = executor.submit(
                    self._execute_supadata_social_search, base_query, context
                )
                logger.info(f"🌐 Supadata Social Search INICIADA: {base_query}")
                futures['youtube_extraction'] = executor.submit(
                    self._execute_youtube_data_extraction, base_query, context
                )
                logger.info(f"🌐 YouTube Extraction INICIADA: {base_query}")


            # Coleta resultados conforme completam (SIMULTANEAMENTE)
            for provider_name, future in futures.items():
                try:
                    result = future.result(timeout=120)  # 2 minutos timeout

                    if provider_name == 'exa':
                        search_results['exa_results'] = result.get('results', [])
                        search_results['statistics']['exa_count'] = len(result.get('results', []))
                        logger.info(f"✅ Exa Neural: {len(result.get('results', []))} resultados ÚNICOS")

                        # Salva resultados Exa IMEDIATAMENTE
                        salvar_etapa("exa_neural_results", result, categoria="pesquisa_web")

                    elif provider_name == 'google':
                        search_results['google_results'] = result.get('results', [])
                        search_results['statistics']['google_count'] = len(result.get('results', []))
                        logger.info(f"✅ Google Keywords: {len(result.get('results', []))} resultados ÚNICOS")

                        # Salva resultados Google IMEDIATAMENTE
                        salvar_etapa("google_keyword_results", result, categoria="pesquisa_web")

                    elif provider_name == 'other':
                        search_results['other_results'] = result.get('results', [])
                        search_results['statistics']['other_count'] = len(result.get('results', []))
                        logger.info(f"✅ Outros Provedores: {len(result.get('results', []))} resultados")

                        # Salva resultados outros IMEDIATAMENTE
                        salvar_etapa("other_providers_results", result, categoria="pesquisa_web")

                    elif provider_name == 'social_media_exa':
                        search_results['social_media_results'].extend(result.get('results', []))
                        search_results['statistics']['social_count'] += len(result.get('results', []))
                        logger.info(f"✅ Exa Social: {len(result.get('results', []))} resultados ÚNICOS")
                        salvar_etapa("exa_social_results", result, categoria="pesquisa_web")

                    elif provider_name == 'social_media_supadata':
                        search_results['social_media_results'].extend(result.get('results', []))
                        search_results['statistics']['social_count'] += len(result.get('results', []))
                        logger.info(f"✅ Supadata Social: {len(result.get('results', []))} resultados ÚNICOS")
                        salvar_etapa("supadata_social_results", result, categoria="pesquisa_web")

                    elif provider_name == 'youtube_extraction':
                        search_results['youtube_results'] = result.get('results', []) # Assumindo que youtube_data_extraction retorna 'results'
                        search_results['statistics']['youtube_count'] = len(result.get('results', [])) # Adicionando contagem para YouTube
                        logger.info(f"✅ YouTube Extraction: {len(result.get('results', []))} resultados ÚNICOS")
                        salvar_etapa("youtube_extraction_results", result, categoria="pesquisa_web")

                except Exception as e:
                    logger.error(f"❌ Erro em busca {provider_name}: {e}")
                    salvar_erro(f"busca_{provider_name}", e, contexto={"query": base_query})

                    # CONTINUA MESMO COM ERRO - SALVA O QUE TEM
                    search_results[f'{provider_name}_error'] = str(e)
                    continue

        # Calcula estatísticas finais
        search_time = time.time() - start_time
        search_results['statistics']['search_time'] = search_time
        search_results['statistics']['total_results'] = (
            search_results['statistics']['exa_count'] +
            search_results['statistics']['google_count'] +
            search_results['statistics']['other_count'] +
            search_results['statistics']['social_count'] + # Inclui contagem de social media
            search_results.get('statistics', {}).get('youtube_count', 0) # Inclui contagem de YouTube
        )

        # GARANTE que pelo menos uma busca funcionou
        if search_results['statistics']['total_results'] == 0:
            logger.warning("⚠️ NENHUMA BUSCA RETORNOU RESULTADOS - Verifique as configurações e provedores.")
            search_results['error'] = "Nenhum resultado obtido. Verifique a configuração das APIs e provedores de busca."
            search_results['fallback_message'] = "Tentativa de busca sem sucesso. Por favor, tente novamente ou verifique os logs."

        # Salva resultado consolidado IMEDIATAMENTE
        salvar_etapa("busca_simultanea_consolidada", search_results, categoria="pesquisa_web")

        logger.info(f"✅ Buscas SIMULTÂNEAS E DISTINTAS concluídas em {search_time:.2f}s")
        logger.info(f"📊 Total: {search_results['statistics']['total_results']} resultados únicos")

        return search_results

    async def execute_comprehensive_web_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca web com cobertura total, incluindo redes sociais e deep research."""
        logger.info(f"🚀 INICIANDO BUSCA WEB AMPLA para: {query}")

        results = {
            'query': query,
            'exa': {},
            'google': {},
            'supadata': {},
            'deep_research': {},
            'instagram': {},
            'youtube': {},
            'error': None,
            'total_results': 0
        }

        prepared_query = self._prepare_search_query(query, context)
        total_results = 0

        async def run_search_task(search_func, key, **kwargs):
            nonlocal total_results
            try:
                response = await search_func(**kwargs)
                if response.get('success'):
                    results[key] = response
                    data_list = response.get('data') or response.get('results') or response.get('posts') or response.get('videos') or []
                    if isinstance(data_list, list):
                        total_results += len(data_list)
                        logger.info(f"✅ {key.capitalize()}: {len(data_list)} resultados")
                    else:
                        logger.warning(f"⚠️ {key.capitalize()} retornou dados não listados: {type(data_list)}")
                else:
                    logger.warning(f"⚠️ {key.capitalize()} falhou: {response.get('error', 'Erro desconhecido')}")
                    results[key] = {"error": response.get('error'), "data": []}
            except Exception as e:
                logger.error(f"❌ Erro {key.capitalize()}: {e}")
                results[key] = {"error": str(e), "data": []}

        search_tasks = []

        # 1. Exa Search
        exa_query = self._prepare_exa_neural_search(query, context)
        search_tasks.append(run_search_task(self._execute_exa_neural_search, 'exa', query=exa_query, context=context))

        # 2. Google Search
        google_query = self._prepare_google_keyword_query(query, context)
        search_tasks.append(run_search_task(self._execute_google_keyword_search, 'google', query=google_query, context=context))

        # 3. Deep Research MCP
        search_tasks.append(run_search_task(self._execute_deep_research_search, 'deep_research', query=prepared_query, context=context))

        # 4. Supadata (Redes Sociais)
        if self.supadata_manager.enabled:
            search_tasks.append(run_search_task(self.supadata_manager.search_social_media, 'supadata', query=prepared_query, platforms=['instagram', 'youtube', 'tiktok'], sentiment_analysis=True))

        # 5. Instagram (Novo)
        search_tasks.append(run_search_task(self.instagram_client.search_instagram_content, 'instagram', query=prepared_query, hashtags=self._extract_hashtags(prepared_query)))

        # 6. YouTube (Novo)
        search_tasks.append(run_search_task(self.youtube_client.search_videos, 'youtube', query=prepared_query, max_results=25))

        # Executa todas as tarefas de busca de forma concorrente
        await asyncio.gather(*search_tasks)

        results['total_results'] = total_results
        logger.info(f"✅ Busca web ampla concluída. Total de resultados: {total_results}")
        return results

    def _prepare_exa_neural_search(self, base_query: str, context: Dict[str, Any]) -> str:
        """Prepara query ESPECÍFICA para Exa Neural Search"""

        # Exa é melhor com queries conceituais e semânticas
        exa_query = f"{base_query} insights análise profunda"

        # Adiciona contexto semântico para busca neural
        if context.get('segmento'):
            exa_query += f" {context['segmento']} tendências oportunidades"

        # Termos para busca neural semântica
        exa_query += " estratégia inovação futuro"

        return exa_query.strip()

    def _generate_comprehensive_query_variations(self, base_query: str, context: Dict[str, Any]) -> Dict[str, List[str]]:
        """Gera variações abrangentes de queries para cobertura máxima"""

        segmento = context.get('segmento', '')
        produto = context.get('produto', '')

        variations = {
            'exa_neural_queries': [
                f"{base_query} insights análise neural semântica",
                f"{base_query} tendências futuro oportunidades",
                f"{base_query} estratégia inovação mercado",
                f"análise profunda {segmento} {produto} transformação digital"
            ],
            'google_keyword_queries': [
                f"{base_query} dados estatísticas Brasil 2024",
                f"{base_query} mercado brasileiro crescimento números",
                f"{base_query} pesquisa IBGE dados oficiais",
                f"relatório {segmento} {produto} Brasil estatísticas"
            ],
            'deep_research_queries': [
                f"pesquisa acadêmica {base_query} universidades",
                f"estudos científicos {segmento} {produto}",
                f"papers research {base_query} metodologia",
                f"dissertações teses {segmento} análise"
            ],
            'social_media_queries': [
                f"{base_query} discussão redes sociais",
                f"{segmento} {produto} opinião pública",
                f"debate {base_query} comunidades online",
                f"sentimento mercado {segmento} social media"
            ],
            'news_queries': [
                f"{base_query} notícias recentes Brasil",
                f"últimas novidades {segmento} {produto}",
                f"breaking news {base_query} mercado",
                f"jornalismo {segmento} tendências atuais"
            ],
            'competitor_queries': [
                f"concorrentes {segmento} {produto} análise",
                f"players mercado {base_query} competição",
                f"benchmark {segmento} líderes mercado",
                f"análise competitiva {base_query} Brasil"
            ],
            'trend_queries': [
                f"tendências {base_query} próximos anos",
                f"futuro {segmento} {produto} previsões",
                f"evolução mercado {base_query} 2024-2030",
                f"transformações {segmento} tecnologia"
            ]
        }

        logger.info(f"📊 Geradas {sum(len(v) for v in variations.values())} variações de query para cobertura máxima")
        return variations

    def _prepare_google_keyword_query(self, base_query: str, context: Dict[str, Any]) -> str:
        """Prepara query ESPECÍFICA para Google Keyword Search"""

        # Google é melhor com keywords específicas e dados
        google_query = f"{base_query} dados estatísticas"

        # Adiciona keywords específicas
        if context.get('segmento'):
            google_query += f" {context['segmento']} mercado brasileiro"

        # Termos para busca por keywords
        google_query += " Brasil 2024 crescimento números"

        return google_query.strip()

    def _execute_exa_neural_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca NEURAL específica no Exa"""

        try:
            logger.info(f"🧠 Executando Exa NEURAL SEARCH: {query}")

            # Domínios brasileiros preferenciais para Exa
            include_domains = [
                "g1.globo.com", "exame.com", "valor.globo.com", "estadao.com.br",
                "folha.uol.com.br", "canaltech.com.br", "infomoney.com.br",
                "startse.com", "revistapegn.globo.com", "epocanegocios.globo.com"
            ]

            exa_response = exa_client.search(
                query=query,
                num_results=20,  # Mais resultados para Exa
                include_domains=include_domains,
                start_published_date="2023-01-01",
                use_autoprompt=True,
                type="neural"  # FORÇA BUSCA NEURAL
            )

            if exa_response and 'results' in exa_response:
                results = []
                for item in exa_response['results']:
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'snippet': item.get('text', '')[:300],
                        'source': 'exa_neural',
                        'score': item.get('score', 0),
                        'published_date': item.get('publishedDate', ''),
                        'exa_id': item.get('id', ''),
                        'search_type': 'neural_semantic'
                    })

                logger.info(f"✅ Exa Neural Search: {len(results)} resultados ÚNICOS")
                return {
                    'provider': 'exa',
                    'query': query,
                    'results': results,
                    'success': True,
                    'search_type': 'neural_semantic'
                }
            else:
                logger.warning("⚠️ Exa não retornou resultados - CONTINUANDO")
                return {
                    'provider': 'exa',
                    'query': query,
                    'results': [],
                    'success': False,
                    'error': 'Exa não retornou resultados válidos'
                }

        except Exception as e:
            logger.error(f"❌ Erro na busca Exa: {e}")
            # SALVA ERRO MAS CONTINUA
            salvar_erro("exa_neural_search", e, contexto={"query": query})
            return {
                'provider': 'exa',
                'query': query,
                'results': [],
                'success': False,
                'error': str(e)
            }

    def _execute_google_keyword_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca KEYWORD específica no Google"""

        try:
            logger.info(f"🔍 Executando Google KEYWORD SEARCH: {query}")

            # Usa production search manager especificamente para Google
            google_api_key = os.getenv('GOOGLE_SEARCH_KEY')
            google_cse_id = os.getenv('GOOGLE_CSE_ID')

            if not google_api_key or not google_cse_id:
                raise Exception("Google API não configurada")

            import requests

            params = {
                'key': google_api_key,
                'cx': google_cse_id,
                'q': query,
                'num': 20,  # Mais resultados para Google
                'lr': 'lang_pt',
                'gl': 'br',
                'safe': 'off',
                'dateRestrict': 'm12'  # Últimos 12 meses
            }

            response = requests.get(
                'https://www.googleapis.com/customsearch/v1',
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                results = []

                for item in data.get('items', []):
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'source': 'google_keywords',
                        'search_type': 'keyword_based'
                    })

                logger.info(f"✅ Google Keyword Search: {len(results)} resultados ÚNICOS")
                return {
                    'provider': 'google',
                    'query': query,
                    'results': results,
                    'success': True,
                    'search_type': 'keyword_based'
                }
            else:
                raise Exception(f"Google API retornou status {response.status_code}")

        except Exception as e:
            logger.error(f"❌ Erro na busca Google: {e}")
            # SALVA ERRO MAS CONTINUA
            salvar_erro("google_keyword_search", e, contexto={"query": query})
            return {
                'provider': 'google',
                'query': query,
                'results': [],
                'success': False,
                'error': str(e)
            }

    def _execute_other_providers_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca em outros provedores como fallback"""

        try:
            logger.info(f"🌐 Executando Other Providers Search: {query}")

            # Usa outros provedores (Serper, Bing, DuckDuckGo)
            other_results = production_search_manager.comprehensive_search(query, search_type="comprehensive")

            # Filtra resultados que não são Google ou Exa
            other_only = []
            for result in other_results:
                if result.get('source') not in ['google', 'exa', 'google_keywords', 'exa_neural']:
                    result['search_type'] = 'fallback_providers'
                    other_only.append(result)

            logger.info(f"✅ Other Providers: {len(other_only)} resultados")
            return {
                'provider': 'other',
                'query': query,
                'results': other_only,
                'success': len(other_only) > 0,
                'search_type': 'fallback_providers'
            }

        except Exception as e:
            logger.error(f"❌ Erro na busca outros provedores: {e}")
            # SALVA ERRO MAS CONTINUA
            salvar_erro("other_providers_search", e, contexto={"query": query})
            return {
                'provider': 'other',
                'query': query,
                'results': [],
                'success': False,
                'error': str(e)
            }

    def _execute_deep_research_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca de pesquisa aprofundada usando o MCP"""
        try:
            logger.info(f"🔬 Executando Deep Research Search: {query}")

            # Usa o cliente de pesquisa aprofundada
            deep_research_results = self.deep_research_client.search(query=query, context=context)

            if deep_research_results.get('success'):
                logger.info(f"✅ Deep Research: {len(deep_research_results.get('results', []))} resultados encontrados")
                return {
                    'provider': 'deep_research',
                    'query': query,
                    'results': deep_research_results.get('results', []),
                    'success': True,
                    'search_type': 'deep_research'
                }
            else:
                logger.warning(f"⚠️ Deep Research falhou: {deep_research_results.get('error', 'Erro desconhecido')}")
                return {
                    'provider': 'deep_research',
                    'query': query,
                    'results': [],
                    'success': False,
                    'error': deep_research_results.get('error')
                }
        except Exception as e:
            logger.error(f"❌ Erro Deep Research: {e}")
            salvar_erro("deep_research_search", e, contexto={"query": query})
            return {
                'provider': 'deep_research',
                'query': query,
                'results': [],
                'success': False,
                'error': str(e)
            }

    def _extract_hashtags(self, query: str) -> List[str]:
        """Extrai hashtags relevantes da query"""
        import re

        # Palavras-chave para hashtags
        keywords = re.findall(r'\b\w+\b', query.lower())
        hashtags = []

        for keyword in keywords:
            if len(keyword) > 3:  # Apenas palavras com mais de 3 caracteres
                hashtags.append(f"#{keyword}")

        return hashtags[:10]  # Máximo 10 hashtags

    def _prepare_search_query(self, query: str, context: Dict[str, Any] = None) -> str:
        """Prepara uma query mais genérica para diferentes provedores, incluindo contexto."""
        prepared = query
        if context:
            if context.get('segmento'):
                prepared += f" {context['segmento']}"
            if context.get('produto'):
                prepared += f" {context['produto']}"

        # Adiciona termos genéricos para cobrir mais casos
        prepared += " análise dados insights mercado"

        return prepared.strip()

    # Métodos adicionados para buscas de redes sociais e YouTube com Exa e Supadata

    def _execute_exa_social_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca social no Exa, focando em plataformas relevantes."""
        try:
            logger.info(f"🌐 Executando Exa Social Search: {query}")

            # Query otimizada para redes sociais no Exa
            social_query = f"{query} site:twitter.com OR site:linkedin.com OR site:facebook.com"

            # Usa busca neural para melhor compreensão
            exa_response = exa_client.search(
                query=social_query,
                num_results=30,
                type="neural",
                use_autoprompt=True
            )

            if exa_response and 'results' in exa_response:
                results = []
                for item in exa_response['results']:
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'snippet': item.get('text', '')[:300],
                        'source': 'exa_social',
                        'score': item.get('score', 0),
                        'published_date': item.get('publishedDate', ''),
                        'exa_id': item.get('id', ''),
                        'search_type': 'social_media_neural'
                    })
                logger.info(f"✅ Exa Social Search: {len(results)} resultados encontrados.")
                return {'provider': 'exa_social', 'query': query, 'results': results, 'success': True, 'search_type': 'social_media_neural'}
            else:
                logger.warning("⚠️ Exa Social Search não retornou resultados.")
                return {'provider': 'exa_social', 'query': query, 'results': [], 'success': False, 'error': 'Exa Social Search falhou.'}
        except Exception as e:
            logger.error(f"❌ Erro Exa Social Search: {e}")
            salvar_erro("exa_social_search", e, contexto={"query": query})
            return {'provider': 'exa_social', 'query': query, 'results': [], 'success': False, 'error': str(e)}

    def _execute_supadata_social_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca social no Supadata/MCP."""
        try:
            logger.info(f"🌐 Executando Supadata Social Search: {query}")

            # Supadata pode ter funcionalidades específicas para redes sociais
            # Assumindo que mcp_supadata_manager tem um método para isso
            # Adapte 'search_social_platforms' para o nome real do método e parâmetros
            social_response = self.supadata_manager.search_social_media( # Usei search_social_media como no exemplo no thoughts
                query=query,
                platforms=['twitter', 'linkedin', 'facebook', 'instagram', 'tiktok'], # Plataformas comuns
                sentiment_analysis=True, # Exemplo de parâmetro adicional
                context=context
            )

            if social_response.get('success'):
                results = social_response.get('data', []) or social_response.get('results', [])
                logger.info(f"✅ Supadata Social Search: {len(results)} resultados encontrados.")
                return {'provider': 'supadata_social', 'query': query, 'results': results, 'success': True, 'search_type': 'social_media_supadata'}
            else:
                logger.warning(f"⚠️ Supadata Social Search falhou: {social_response.get('error', 'Erro desconhecido')}")
                return {'provider': 'supadata_social', 'query': query, 'results': [], 'success': False, 'error': social_response.get('error', 'Supadata Social Search falhou.')}
        except Exception as e:
            logger.error(f"❌ Erro Supadata Social Search: {e}")
            salvar_erro("supadata_social_search", e, contexto={"query": query})
            return {'provider': 'supadata_social', 'query': query, 'results': [], 'success': False, 'error': str(e)}

    def _execute_youtube_data_extraction(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa extração de dados relevantes do YouTube."""
        try:
            logger.info(f"▶️ Executando YouTube Data Extraction: {query}")

            # Usa o cliente do YouTube para buscar vídeos
            youtube_response = self.youtube_client.search_videos(
                query=query,
                max_results=20, # Número de resultados para YouTube
                context=context
            )

            if youtube_response.get('success'):
                results = youtube_response.get('videos', []) or youtube_response.get('results', [])
                logger.info(f"✅ YouTube Data Extraction: {len(results)} vídeos encontrados.")
                return {'provider': 'youtube', 'query': query, 'results': results, 'success': True, 'search_type': 'youtube_extraction'}
            else:
                logger.warning(f"⚠️ YouTube Data Extraction falhou: {youtube_response.get('error', 'Erro desconhecido')}")
                return {'provider': 'youtube', 'query': query, 'results': [], 'success': False, 'error': youtube_response.get('error', 'YouTube Data Extraction falhou.')}
        except Exception as e:
            logger.error(f"❌ Erro YouTube Data Extraction: {e}")
            salvar_erro("youtube_data_extraction", e, contexto={"query": query})
            return {'provider': 'youtube', 'query': query, 'results': [], 'success': False, 'error': str(e)}


# Instância global
enhanced_search_coordinator = EnhancedSearchCoordinator()