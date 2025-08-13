#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Exa Client
Cliente para integração com Exa API para pesquisa avançada
"""

import os
import logging
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from exa_py import Exa

logger = logging.getLogger(__name__)

class ExaClient:
    """Cliente para integração com Exa API"""

    def __init__(self):
        """Inicializa cliente Exa"""
        self.api_key = os.getenv("EXA_API_KEY", "a0dd63a6-0bd1-488f-a63e-2c4f4cfe969f")
        self.base_url = "https://api.exa.ai"

        if self.api_key:
            try:
                self.client = Exa(self.api_key)
                logger.info("✅ Exa client inicializado com sucesso")
                self.available = True
            except Exception as e:
                logger.error(f"⚠️ Erro ao inicializar Exa client: {e}")
                self.available = False
                self.client = None
        else:
            logger.warning("⚠️ Exa API key não encontrada")
            self.available = False
            self.client = None


    def is_available(self) -> bool:
        """Verifica se o cliente está disponível"""
        return self.available

    def search(
        self,
        query: str,
        num_results: int = 10,
        include_domains: List[str] = None,
        exclude_domains: List[str] = None,
        start_crawl_date: str = None,
        end_crawl_date: str = None,
        start_published_date: str = None,
        end_published_date: str = None,
        use_autoprompt: bool = True,
        type: str = "neural"
    ) -> Optional[Dict[str, Any]]:
        """Realiza busca usando Exa API"""

        if not self.available:
            logger.warning("Exa não está disponível")
            return None

        try:
            # Parâmetros corretos para a API Exa
            search_params = {
                "query": query,
                "num_results": num_results,
                "use_autoprompt": use_autoprompt,  # Corrigido de useAutoprompt
                "type": type
            }

            if include_domains:
                search_params["include_domains"] = include_domains

            if exclude_domains:
                search_params["exclude_domains"] = exclude_domains

            if start_crawl_date:
                search_params["start_crawl_date"] = start_crawl_date

            if end_crawl_date:
                search_params["end_crawl_date"] = end_crawl_date

            if start_published_date:
                search_params["start_published_date"] = start_published_date

            if end_published_date:
                search_params["end_published_date"] = end_published_date

            response = self.client.search(**search_params)

            # A resposta do Exa é um objeto, não HTTP response
            if hasattr(response, 'results'):
                results = []
                for result in response.results:
                    result_dict = {
                        'id': getattr(result, 'id', ''),
                        'title': getattr(result, 'title', ''),
                        'url': getattr(result, 'url', ''),
                        'text': getattr(result, 'text', ''),
                        'score': getattr(result, 'score', 0),
                        'published_date': result.published_date if isinstance(result.published_date, str) else (result.published_date.isoformat() if hasattr(result, 'published_date') and result.published_date and hasattr(result.published_date, 'isoformat') else None),
                    }
                    results.append(result_dict)

                logger.info(f"✅ Exa search: {len(results)} resultados")
                return {'results': results}
            else:
                logger.warning("⚠️ Resposta Exa sem resultados")
                return {'results': []}

        except Exception as e:
            logger.error(f"❌ Erro na requisição Exa: {str(e)}")
            return None

    def get_contents(
        self,
        ids: List[str],
        text: bool = True,
        highlights: bool = False,
        summary: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Obtém conteúdo detalhado dos resultados"""

        if not self.available:
            return None

        try:
            payload = {
                "ids": ids,
                "text": text,
                "highlights": highlights,
                "summary": summary
            }

            response = self.client.get_contents(**payload)

            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Exa contents: {len(data.get('results', []))} conteúdos")
                return data
            else:
                logger.error(f"❌ Erro Exa contents: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"❌ Erro ao obter conteúdos Exa: {str(e)}")
            return None

    def find_similar(
        self,
        url: str,
        num_results: int = 10,
        exclude_source_domain: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Encontra páginas similares"""

        if not self.available:
            return None

        try:
            payload = {
                "url": url,
                "numResults": num_results,
                "excludeSourceDomain": exclude_source_domain
            }

            response = self.client.find_similar(**payload)

            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Exa similar: {len(data.get('results', []))} similares")
                return data
            else:
                logger.error(f"❌ Erro Exa similar: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"❌ Erro ao buscar similares: {str(e)}")
            return None

    def search_comprehensive(self, query: str, num_results: int = 10, **kwargs) -> Dict[str, Any]:
        """Busca abrangente com múltiplas estratégias e filtros avançados"""
        try:
            if not self.api_key:
                logger.warning("Exa API key não configurada")
                return {
                    'success': False,
                    'error': 'API key não configurada',
                    'query': query,
                    'results': []
                }

            # Extrai parâmetros de kwargs com valores padrão seguros
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')
            include_domains = kwargs.get('include_domains')
            exclude_domains = kwargs.get('exclude_domains')
            min_length = kwargs.get('min_length', 200) # Valor padrão para min_length
            max_length = kwargs.get('max_length', 2000) # Valor padrão para max_length

            try:
                # Configuração da busca com parâmetros otimizados
                search_params = {
                    'query': query,
                    'num_results': min(num_results or 10, 50),  # Limite máximo da API
                    'type': 'auto',  # Deixa a API decidir o melhor tipo
                    'use_autoprompt': True,  # Melhora a query automaticamente
                }

                # Adiciona datas se fornecidas
                if start_date:
                    search_params['start_published_date'] = start_date
                if end_date:
                    search_params['end_published_date'] = end_date
                if include_domains:
                    search_params['include_domains'] = include_domains
                if exclude_domains:
                    search_params['exclude_domains'] = exclude_domains

                logger.info(f"🔍 Executando busca Exa com parâmetros: {search_params}")

                # Executa a busca
                response = self.client.search(**search_params)

                if not response or not hasattr(response, 'results'):
                    logger.warning("⚠️ Resposta Exa vazia ou inválida")
                    return []

                results = self._process_exa_results(response.results, search_params)

                logger.info(f"✅ Exa retornou {len(results)} resultados válidos")

                return {
                    'success': True,
                    'query': query,
                    'total_results': len(results),
                    'results': results,
                    'search_strategy': 'comprehensive_neural',
                    'timestamp': datetime.now().isoformat(),
                    'search_params': search_params
                }

            except Exception as api_error:
                logger.error(f"Erro na API Exa: {api_error}")

                # Fallback para busca básica
                return self._fallback_basic_search(query, num_results)

        except Exception as e:
            logger.error(f"❌ Erro na busca comprehensive Exa: {e}")
            return {
                'success': False,
                'error': str(e),
                'query': query,
                'results': []
            }

    def _process_exa_results(self, results, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Processa resultados do Exa para formato padronizado"""
        processed_results = []

        for item in results:
            try:
                # CORREÇÃO CRÍTICA: Normaliza published_date independente do tipo
                published_date = self._normalize_published_date(item.published_date)

                processed_item = {
                    'title': item.title or 'Sem título',
                    'url': item.url,
                    'snippet': (item.text or '')[:300],
                    'content': item.text or '',
                    'source': 'exa',
                    'score': getattr(item, 'score', 0),
                    'published_date': published_date,
                    'highlights': getattr(item, 'highlights', []),
                    'author': getattr(item, 'author', None),
                    'search_query': search_params.get('query', ''),
                    'extracted_at': datetime.now().isoformat()
                }

                processed_results.append(processed_item)

            except Exception as e:
                logger.warning(f"⚠️ Erro ao processar item Exa: {e} - Tipo do item: {type(item)} - Atributos: {[attr for attr in dir(item) if not attr.startswith('_')]}")
                continue

        logger.info(f"✅ Exa retornou {len(processed_results)} resultados válidos")
        return processed_results

    def _normalize_published_date(self, date_field) -> Optional[str]:
        """Normaliza campo published_date para ISO format independente do tipo"""
        try:
            if date_field is None:
                return None

            # Se já é string, retorna diretamente
            if isinstance(date_field, str):
                # Tenta parsear diferentes formatos de string para validar
                try:
                    from dateutil.parser import parse
                    parsed_date = parse(date_field)
                    return parsed_date.isoformat()
                except:
                    # Se não conseguir parsear, retorna a string original
                    return date_field

            # Se é datetime, chama isoformat
            if hasattr(date_field, 'isoformat'):
                return date_field.isoformat()

            # Se é timestamp, converte
            if isinstance(date_field, (int, float)):
                return datetime.fromtimestamp(date_field).isoformat()

            # Fallback: converte para string
            return str(date_field)

        except Exception as e:
            logger.warning(f"⚠️ Erro ao normalizar data: {e} - Tipo: {type(date_field)} - Valor: {date_field}")
            return None


    def _fallback_basic_search(self, query: str, num_results: int) -> Dict[str, Any]:
        """Busca básica como fallback"""
        try:
            basic_params = {
                'query': query,
                'num_results': min(num_results, 10),
                'use_autoprompt': True
            }

            response = self.client.search(**basic_params)

            results = []
            if hasattr(response, 'results') and response.results:
                for result in response.results:
                    results.append({
                        'title': getattr(result, 'title', 'Sem título'),
                        'url': getattr(result, 'url', ''),
                        'text': '',  # Busca básica não retorna texto
                        'score': getattr(result, 'score', 0),
                        'source': 'exa_basic'
                    })

            return {
                'success': True,
                'query': query,
                'total_results': len(results),
                'results': results,
                'search_strategy': 'basic_fallback',
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Falha no fallback básico Exa: {e}")
            return {
                'success': False,
                'error': f"Busca básica falhou: {str(e)}",
                'query': query,
                'results': []
            }

# Instância global
exa_client = ExaClient()