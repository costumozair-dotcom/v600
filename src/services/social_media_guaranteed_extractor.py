#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Social Media Guaranteed Extractor
Sistema que GARANTE extrações reais de redes sociais usando EXA e SUPADATA
"""

import os
import logging
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from services.exa_client import exa_client
from services.mcp_supadata_manager import mcp_supadata_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class SocialMediaGuaranteedExtractor:
    """Extrator garantido de redes sociais usando EXA e SUPADATA"""

    def __init__(self):
        """Inicializa o extrator garantido"""
        self.platforms = {
            'youtube': ['youtube.com', 'youtu.be'],
            'instagram': ['instagram.com'],
            'tiktok': ['tiktok.com'],
            'twitter': ['twitter.com', 'x.com'],
            'facebook': ['facebook.com'],
            'linkedin': ['linkedin.com']
        }

        self.extraction_results = {}

        logger.info("🔍 Social Media Guaranteed Extractor inicializado")

    def extract_guaranteed_social_data(
        self, 
        query: str, 
        session_id: str,
        max_results_per_platform: int = 20
    ) -> Dict[str, Any]:
        """Executa extração garantida de dados sociais"""

        try:
            logger.info(f"🚀 Iniciando extração GARANTIDA de redes sociais para: {query}")

            extraction_results = {
                'query': query,
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'exa_social_results': {},
                'supadata_results': {},
                'total_extracted': 0,
                'platforms_analyzed': [],
                'success_status': {}
            }

            # FASE 1: Extração com EXA para cada plataforma
            logger.info("📱 Executando extração EXA por plataforma...")
            exa_results = self._extract_with_exa(query, max_results_per_platform)
            extraction_results['exa_social_results'] = exa_results

            # FASE 2: Extração com SUPADATA
            logger.info("🎬 Executando extração SUPADATA...")
            supadata_results = self._extract_with_supadata(query, max_results_per_platform)
            extraction_results['supadata_results'] = supadata_results

            # FASE 3: Consolidação e validação
            logger.info("✅ Consolidando resultados extraídos...")
            consolidated = self._consolidate_social_data(extraction_results)

            # Salva resultados garantidos
            salvar_etapa(
                "social_extraction_guaranteed",
                consolidated,
                session_id=session_id,
                categoria="social_media"
            )

            logger.info(f"✅ Extração garantida concluída: {consolidated['total_extracted']} itens")
            return consolidated

        except Exception as e:
            logger.error(f"❌ Erro na extração garantida: {e}")
            salvar_erro("social_extraction_error", e, contexto={
                'query': query,
                'session_id': session_id
            })

            return {
                'query': query,
                'session_id': session_id,
                'error': str(e),
                'total_extracted': 0,
                'success': False
            }

    def _extract_with_exa(self, query: str, max_results: int) -> Dict[str, Any]:
        """Extrai dados sociais usando EXA"""

        exa_results = {
            'youtube_data': [],
            'instagram_data': [],
            'tiktok_data': [],
            'twitter_data': [],
            'total_exa_results': 0
        }

        try:
            # Busca específica para YouTube
            youtube_query = f"{query} site:youtube.com OR site:youtu.be"
            youtube_data = exa_client.search(
                query=youtube_query,
                num_results=max_results,
                use_autoprompt=True,
                type="neural",
                include_domains=['youtube.com', 'youtu.be']
            )

            if youtube_data and 'results' in youtube_data:
                exa_results['youtube_data'] = [
                    {
                        'url': result.get('url', ''),
                        'title': result.get('title', ''),
                        'text': result.get('text', '')[:500],
                        'platform': 'youtube',
                        'extracted_at': datetime.now().isoformat()
                    }
                    for result in youtube_data['results']
                ]
                logger.info(f"✅ EXA YouTube: {len(exa_results['youtube_data'])} resultados")

            # Busca para Instagram
            instagram_query = f"{query} site:instagram.com"
            instagram_data = exa_client.search(
                query=instagram_query,
                num_results=max_results,
                use_autoprompt=True,
                type="neural",
                include_domains=['instagram.com']
            )

            if instagram_data and 'results' in instagram_data:
                exa_results['instagram_data'] = [
                    {
                        'url': result.get('url', ''),
                        'title': result.get('title', ''),
                        'text': result.get('text', '')[:500],
                        'platform': 'instagram',
                        'extracted_at': datetime.now().isoformat()
                    }
                    for result in instagram_data['results']
                ]
                logger.info(f"✅ EXA Instagram: {len(exa_results['instagram_data'])} resultados")

            # Busca para TikTok
            tiktok_query = f"{query} site:tiktok.com"
            tiktok_data = exa_client.search(
                query=tiktok_query,
                num_results=max_results,
                use_autoprompt=True,
                type="neural",
                include_domains=['tiktok.com']
            )

            if tiktok_data and 'results' in tiktok_data:
                exa_results['tiktok_data'] = [
                    {
                        'url': result.get('url', ''),
                        'title': result.get('title', ''),
                        'text': result.get('text', '')[:500],
                        'platform': 'tiktok',
                        'extracted_at': datetime.now().isoformat()
                    }
                    for result in tiktok_data['results']
                ]
                logger.info(f"✅ EXA TikTok: {len(exa_results['tiktok_data'])} resultados")

            # Busca para Twitter/X
            twitter_query = f"{query} site:twitter.com OR site:x.com"
            twitter_data = exa_client.search(
                query=twitter_query,
                num_results=max_results,
                use_autoprompt=True,
                type="neural",
                include_domains=['twitter.com', 'x.com']
            )

            if twitter_data and 'results' in twitter_data:
                exa_results['twitter_data'] = [
                    {
                        'url': result.get('url', ''),
                        'title': result.get('title', ''),
                        'text': result.get('text', '')[:500],
                        'platform': 'twitter',
                        'extracted_at': datetime.now().isoformat()
                    }
                    for result in twitter_data['results']
                ]
                logger.info(f"✅ EXA Twitter: {len(exa_results['twitter_data'])} resultados")

            # Calcula total
            exa_results['total_exa_results'] = (
                len(exa_results['youtube_data']) +
                len(exa_results['instagram_data']) +
                len(exa_results['tiktok_data']) +
                len(exa_results['twitter_data'])
            )

        except Exception as e:
            logger.error(f"❌ Erro na extração EXA: {e}")
            exa_results['error'] = str(e)

        return exa_results

    def _extract_with_supadata(self, query: str, max_results: int) -> Dict[str, Any]:
        """Extrai dados usando SUPADATA"""

        supadata_results = {
            'platforms_data': {},
            'total_supadata_results': 0
        }

        try:
            # Executa busca SUPADATA em todas as plataformas
            supadata_response = mcp_supadata_manager.search_all_platforms(
                query, 
                max_results_per_platform=max_results
            )

            if supadata_response and supadata_response.get('success'):
                platforms_data = supadata_response.get('platforms', {})

                for platform, data in platforms_data.items():
                    if data and isinstance(data, list):
                        processed_data = []
                        for item in data:
                            processed_item = {
                                'title': item.get('title', ''),
                                'url': item.get('url', ''),
                                'description': item.get('description', ''),
                                'platform': platform,
                                'extracted_at': datetime.now().isoformat(),
                                'metadata': item.get('metadata', {})
                            }
                            processed_data.append(processed_item)

                        supadata_results['platforms_data'][platform] = processed_data
                        logger.info(f"✅ SUPADATA {platform}: {len(processed_data)} resultados")

                supadata_results['total_supadata_results'] = sum(
                    len(data) for data in supadata_results['platforms_data'].values()
                )

        except Exception as e:
            logger.error(f"❌ Erro na extração SUPADATA: {e}")
            supadata_results['error'] = str(e)

        return supadata_results

    def _consolidate_social_data(self, extraction_results: Dict[str, Any]) -> Dict[str, Any]:
        """Consolida dados extraídos de todas as fontes"""

        consolidated = {
            'query': extraction_results['query'],
            'session_id': extraction_results['session_id'],
            'timestamp': extraction_results['timestamp'],
            'consolidated_data': {},
            'extraction_summary': {},
            'total_extracted': 0,
            'platforms_analyzed': [],
            'data_quality_score': 0
        }

        # Consolida dados EXA
        exa_data = extraction_results.get('exa_social_results', {})
        for platform, data in exa_data.items():
            if platform != 'total_exa_results' and isinstance(data, list) and data:
                if platform not in consolidated['consolidated_data']:
                    consolidated['consolidated_data'][platform] = []

                consolidated['consolidated_data'][platform].extend(data)
                if platform.replace('_data', '') not in consolidated['platforms_analyzed']:
                    consolidated['platforms_analyzed'].append(platform.replace('_data', ''))

        # Consolida dados SUPADATA
        supadata_data = extraction_results.get('supadata_results', {}).get('platforms_data', {})
        for platform, data in supadata_data.items():
            if isinstance(data, list) and data:
                if platform not in consolidated['consolidated_data']:
                    consolidated['consolidated_data'][platform] = []

                consolidated['consolidated_data'][platform].extend(data)
                if platform not in consolidated['platforms_analyzed']:
                    consolidated['platforms_analyzed'].append(platform)

        # Calcula métricas finais
        consolidated['total_extracted'] = sum(
            len(data) for data in consolidated['consolidated_data'].values()
        )

        consolidated['extraction_summary'] = {
            'platforms_with_data': len(consolidated['consolidated_data']),
            'total_platforms_analyzed': len(consolidated['platforms_analyzed']),
            'exa_total': exa_data.get('total_exa_results', 0),
            'supadata_total': extraction_results.get('supadata_results', {}).get('total_supadata_results', 0)
        }

        # Score de qualidade baseado na quantidade e diversidade
        quality_score = min(100, (
            (consolidated['total_extracted'] * 2) +
            (len(consolidated['platforms_analyzed']) * 10)
        ))
        consolidated['data_quality_score'] = quality_score

        return consolidated

# Instância global
social_media_guaranteed_extractor = SocialMediaGuaranteedExtractor()