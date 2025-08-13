#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Master Analysis Engine UNIFICADO
Engine principal que centraliza TODAS as análises sem duplicação
"""

import os
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

# Importações de todos os engines específicos
from services.enhanced_analysis_engine import enhanced_analysis_engine
from services.ultra_detailed_analysis_engine import ultra_detailed_analysis_engine
from services.unified_analysis_engine import unified_analysis_engine

# Importações de serviços essenciais
from services.ai_manager import ai_manager
from services.exa_client import exa_client
from services.mcp_supadata_manager import mcp_supadata_manager
from services.alibaba_websailor import AlibabaWebSailorAgent
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class MasterAnalysisEngine:
    """Engine principal que unifica TODAS as análises sem duplicação"""

    def __init__(self):
        """Inicializa o Master Analysis Engine"""
        self.engines = {
            'enhanced': enhanced_analysis_engine,
            'ultra_detailed': ultra_detailed_analysis_engine,
            'unified': unified_analysis_engine
        }

        self.search_providers = {
            'exa': exa_client,
            'supadata': mcp_supadata_manager,
            'websailor': AlibabaWebSailorAgent()
        }

        self.analysis_cache = {}
        self.execution_metrics = {}

        logger.info("🚀 Master Analysis Engine inicializado - UNIFICAÇÃO COMPLETA")

    def execute_complete_analysis(
        self,
        data: Dict[str, Any],
        session_id: str,
        analysis_type: str = "complete",
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """Executa análise completa e unificada"""

        try:
            logger.info(f"🎯 Iniciando análise MASTER COMPLETA - Sessão: {session_id}")
            start_time = time.time()

            # Salva início da análise
            salvar_etapa("master_analysis_iniciada", {
                'session_id': session_id,
                'data': data,
                'analysis_type': analysis_type,
                'engines_available': list(self.engines.keys()),
                'search_providers': list(self.search_providers.keys())
            }, categoria="analise_completa", session_id=session_id)

            # FASE 1: Preparação e validação de dados
            if progress_callback:
                progress_callback(1, "🔧 Preparando dados para análise unificada...")

            prepared_data = self._prepare_unified_data(data, session_id)

            # FASE 2: Execução das buscas e extrações (EXA + SUPADATA)
            if progress_callback:
                progress_callback(2, "🔍 Executando buscas unificadas com EXA e SUPADATA...")

            search_results = self._execute_unified_search(prepared_data, session_id)

            # FASE 3: Análise com engine apropriado
            if progress_callback:
                progress_callback(3, "🧠 Executando análise unificada...")

            analysis_results = self._execute_engine_analysis(
                {**prepared_data, **search_results},
                analysis_type,
                session_id
            )

            # FASE 4: Consolidação final
            if progress_callback:
                progress_callback(4, "📊 Consolidando resultados finais...")

            final_results = self._consolidate_results(
                prepared_data,
                search_results,
                analysis_results,
                session_id
            )

            execution_time = time.time() - start_time

            # Salva resultados finais
            salvar_etapa("master_analysis_concluida", {
                'session_id': session_id,
                'execution_time': execution_time,
                'results': final_results,
                'engines_used': analysis_results.get('engines_used', []),
                'total_data_points': len(str(final_results))
            }, categoria="analise_completa", session_id=session_id)

            logger.info(f"✅ Master Analysis CONCLUÍDA em {execution_time:.2f}s")

            return {
                'success': True,
                'session_id': session_id,
                'execution_time': execution_time,
                'results': final_results,
                'engines_used': analysis_results.get('engines_used', []),
                'data_sources': list(search_results.keys()),
                'analysis_type': analysis_type,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Erro crítico no Master Analysis Engine: {e}")
            salvar_erro("master_analysis_error", e, contexto={
                'session_id': session_id,
                'data': data,
                'analysis_type': analysis_type
            })

            # Retorna resultado de erro estruturado
            return {
                'success': False,
                'session_id': session_id,
                'error': str(e),
                'error_type': 'master_analysis_critical',
                'timestamp': datetime.now().isoformat()
            }

    def _prepare_unified_data(self, data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Prepara dados para análise unificada"""

        prepared = {
            'session_id': session_id,
            'segmento': data.get('segmento', ''),
            'produto': data.get('produto', ''),
            'publico': data.get('publico', ''),
            'query_principal': f"{data.get('segmento', '')} {data.get('produto', '')} Brasil 2024".strip(),
            'queries_especificas': self._generate_specific_queries(data),
            'timestamp': datetime.now().isoformat()
        }

        # Adiciona dados extras preservando estrutura
        for key, value in data.items():
            if key not in prepared and value:
                prepared[key] = value

        return prepared

    def _generate_specific_queries(self, data: Dict[str, Any]) -> List[str]:
        """Gera queries específicas para busca"""

        segmento = data.get('segmento', '')
        produto = data.get('produto', '')
        publico = data.get('publico', '')

        queries = [
            f"mercado {segmento} Brasil 2024",
            f"{produto} análise competitiva Brasil",
            f"tendências {segmento} brasileiro",
            f"{publico} comportamento consumo Brasil",
            f"oportunidades negócio {segmento} Brasil"
        ]

        return [q for q in queries if len(q.strip()) > 10]

    def _execute_unified_search(self, data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Executa buscas unificadas com EXA e SUPADATA"""

        search_results = {
            'exa_results': [],
            'supadata_results': [],
            'websailor_results': [],
            'search_summary': {}
        }

        query = data.get('query_principal', '')

        try:
            # 1. Busca com EXA (prioridade 1)
            logger.info("🔍 Executando busca EXA...")
            exa_data = exa_client.search(
                query=query,
                num_results=20,
                use_autoprompt=True,
                type="neural",
                start_published_date="2023-01-01"
            )

            if exa_data and 'results' in exa_data:
                search_results['exa_results'] = exa_data['results']
                logger.info(f"✅ EXA: {len(exa_data['results'])} resultados")

        except Exception as e:
            logger.error(f"❌ Erro EXA: {e}")
            salvar_erro("exa_search_error", e, contexto={'query': query, 'session_id': session_id})

        try:
            # 2. Busca com SUPADATA (YouTube + Redes Sociais)
            logger.info("📱 Executando busca SUPADATA...")
            supadata_data = mcp_supadata_manager.search_all_platforms(query, max_results_per_platform=10)

            if supadata_data and supadata_data.get('success'):
                search_results['supadata_results'] = supadata_data
                logger.info(f"✅ SUPADATA: {supadata_data.get('total_results', 0)} resultados")

        except Exception as e:
            logger.error(f"❌ Erro SUPADATA: {e}")
            salvar_erro("supadata_search_error", e, contexto={'query': query, 'session_id': session_id})

        try:
            # 3. Busca com WebSailor (complementar)
            logger.info("🌐 Executando busca WebSailor...")
            websailor_data = self.search_providers['websailor'].navigate_and_research_deep(
                query, data, max_pages=10, depth_levels=2, session_id=session_id
            )

            if websailor_data and websailor_data.get('status') == 'success':
                search_results['websailor_results'] = websailor_data.get('processed_results', [])
                logger.info(f"✅ WebSailor: {len(websailor_data.get('processed_results', []))} resultados")

        except Exception as e:
            logger.error(f"❌ Erro WebSailor: {e}")
            salvar_erro("websailor_search_error", e, contexto={'query': query, 'session_id': session_id})

        # Salva resultados das buscas
        salvar_etapa("unified_search_completed", search_results, categoria="pesquisa_web", session_id=session_id)

        return search_results

    def _execute_engine_analysis(self, data: Dict[str, Any], analysis_type: str, session_id: str) -> Dict[str, Any]:
        """Executa análise com engine apropriado"""

        engines_used = []
        analysis_results = {}

        try:
            if analysis_type == "complete" or analysis_type == "ultra":
                # Usa Ultra Detailed Engine
                logger.info("🧠 Executando Ultra Detailed Analysis...")
                ultra_results = ultra_detailed_analysis_engine.perform_ultra_detailed_analysis(data, session_id)
                analysis_results['ultra_detailed'] = ultra_results
                engines_used.append('ultra_detailed')

            if analysis_type == "complete" or analysis_type == "enhanced":
                # Usa Enhanced Engine
                logger.info("⚡ Executando Enhanced Analysis...")
                enhanced_results = enhanced_analysis_engine.analyze_comprehensive(data, session_id)
                analysis_results['enhanced'] = enhanced_results
                engines_used.append('enhanced')

            if analysis_type == "complete":
                # Usa Unified Engine
                logger.info("🔗 Executando Unified Analysis...")
                unified_results = unified_analysis_engine.execute_unified_analysis(data, session_id)
                analysis_results['unified'] = unified_results
                engines_used.append('unified')

            return {
                'engines_used': engines_used,
                'results': analysis_results,
                'analysis_type': analysis_type,
                'success': True
            }

        except Exception as e:
            logger.error(f"❌ Erro na análise com engines: {e}")
            salvar_erro("engine_analysis_error", e, contexto={
                'analysis_type': analysis_type,
                'session_id': session_id
            })

            return {
                'engines_used': engines_used,
                'results': analysis_results,
                'analysis_type': analysis_type,
                'success': False,
                'error': str(e)
            }

    def _consolidate_results(
        self,
        prepared_data: Dict[str, Any],
        search_results: Dict[str, Any],
        analysis_results: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Consolida todos os resultados em estrutura final"""

        consolidated = {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'input_data': prepared_data,
            'search_data': search_results,
            'analysis_data': analysis_results,
            'summary': self._generate_analysis_summary(search_results, analysis_results),
            'metrics': self._calculate_analysis_metrics(search_results, analysis_results)
        }

        return consolidated

    def _generate_analysis_summary(self, search_results: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Gera resumo da análise"""

        total_sources = (
            len(search_results.get('exa_results', [])) +
            search_results.get('supadata_results', {}).get('total_results', 0) +
            len(search_results.get('websailor_results', []))
        )

        return {
            'total_data_sources': total_sources,
            'engines_executed': len(analysis_results.get('results', {})),
            'analysis_success': analysis_results.get('success', False),
            'data_quality': 'high' if total_sources > 20 else 'medium' if total_sources > 10 else 'low'
        }

    def _calculate_analysis_metrics(self, search_results: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula métricas da análise"""

        return {
            'exa_data_points': len(search_results.get('exa_results', [])),
            'social_platforms_analyzed': len(search_results.get('supadata_results', {}).get('platforms', [])),
            'websailor_pages_processed': len(search_results.get('websailor_results', [])),
            'total_analysis_depth': len(str(analysis_results)),
            'analysis_completeness': 100 if analysis_results.get('success') else 50
        }

# Instância global
master_analysis_engine = MasterAnalysisEngine()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Analysis Engine - Motor Unificado de Análise
Centraliza todos os motores de análise em um único componente
"""

import os
import sys
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Adiciona src ao path
if 'src' not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_manager import ai_manager
from services.enhanced_search_coordinator import enhanced_search_coordinator
from services.component_orchestrator import component_orchestrator
from services.auto_save_manager import auto_save_manager
from services.production_logger import production_logger
from services.content_quality_validator import content_quality_validator
from services.professional_report_manager import professional_report_manager

logger = logging.getLogger(__name__)

class MasterAnalysisEngine:
    """Motor Principal de Análise - Unifica todos os componentes"""
    
    def __init__(self):
        self.logger = production_logger.get_logger("MasterAnalysisEngine")
        self.session_id = None
        self.analysis_results = {}
        self.components_status = {}
        
    def execute_complete_analysis(
        self, 
        query: str, 
        context: Dict[str, Any], 
        session_id: str = None
    ) -> Dict[str, Any]:
        """Executa análise completa usando motor unificado"""
        
        self.session_id = session_id or f"master_{int(time.time())}"
        
        try:
            self.logger.info(f"🚀 MASTER ENGINE: Iniciando análise completa para: {query}")
            
            # Salva início da análise
            auto_save_manager.salvar_etapa(
                "master_analysis_iniciada",
                {
                    "query": query,
                    "context": context,
                    "session_id": self.session_id,
                    "timestamp": datetime.now().isoformat(),
                    "engine": "MasterAnalysisEngine"
                },
                session_id=self.session_id,
                categoria="master_engine"
            )
            
            # 1. FASE DE PESQUISA WEB MASSIVA
            web_search_results = self._execute_web_search_phase(query, context)
            
            # 2. FASE DE ANÁLISE DE COMPONENTES
            components_results = self._execute_components_phase(query, context, web_search_results)
            
            # 3. FASE DE GERAÇÃO DE INSIGHTS
            insights_results = self._execute_insights_phase(query, context, components_results)
            
            # 4. FASE DE CONSOLIDAÇÃO FINAL
            final_results = self._execute_consolidation_phase(
                query, context, web_search_results, components_results, insights_results
            )
            
            # Salva resultado final consolidado
            auto_save_manager.salvar_etapa(
                "master_analysis_completa",
                final_results,
                session_id=self.session_id,
                categoria="master_engine"
            )
            
            self.logger.info("✅ MASTER ENGINE: Análise completa finalizada com sucesso")
            return final_results
            
        except Exception as e:
            self.logger.error(f"❌ MASTER ENGINE: Erro na análise: {e}")
            error_result = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "session_id": self.session_id
            }
            
            auto_save_manager.salvar_etapa(
                "master_analysis_erro",
                error_result,
                session_id=self.session_id,
                categoria="master_engine"
            )
            
            return error_result
    
    def _execute_web_search_phase(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa fase de pesquisa web massiva"""
        
        self.logger.info("🔍 MASTER ENGINE: Executando fase de pesquisa web")
        
        try:
            # Usa enhanced_search_coordinator para busca massiva
            search_results = enhanced_search_coordinator.execute_comprehensive_web_search(
                query, context
            )
            
            # Valida qualidade dos resultados
            validated_results = content_quality_validator.validate_search_results(
                search_results, context
            )
            
            # Salva resultados da pesquisa
            auto_save_manager.salvar_etapa(
                "master_web_search_phase",
                validated_results,
                session_id=self.session_id,
                categoria="master_engine"
            )
            
            self.components_status["web_search"] = "completed"
            return validated_results
            
        except Exception as e:
            self.logger.error(f"❌ MASTER ENGINE: Erro na fase de pesquisa: {e}")
            self.components_status["web_search"] = "error"
            return {"status": "error", "error": str(e)}
    
    def _execute_components_phase(
        self, 
        query: str, 
        context: Dict[str, Any], 
        web_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Executa fase de análise de componentes"""
        
        self.logger.info("🧠 MASTER ENGINE: Executando fase de componentes")
        
        try:
            # Usa component_orchestrator para executar todos os componentes
            components_results = component_orchestrator.execute_all_components(
                query, context, web_results, session_id=self.session_id
            )
            
            # Salva resultados dos componentes
            auto_save_manager.salvar_etapa(
                "master_components_phase",
                components_results,
                session_id=self.session_id,
                categoria="master_engine"
            )
            
            self.components_status["components"] = "completed"
            return components_results
            
        except Exception as e:
            self.logger.error(f"❌ MASTER ENGINE: Erro na fase de componentes: {e}")
            self.components_status["components"] = "error"
            return {"status": "error", "error": str(e)}
    
    def _execute_insights_phase(
        self, 
        query: str, 
        context: Dict[str, Any], 
        components_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Executa fase de geração de insights"""
        
        self.logger.info("💡 MASTER ENGINE: Executando fase de insights")
        
        try:
            # Gera insights consolidados usando IA
            insights_prompt = self._build_insights_prompt(query, context, components_results)
            
            insights_results = ai_manager.generate_content(
                insights_prompt,
                max_tokens=4000,
                temperature=0.7
            )
            
            insights_data = {
                "insights_generated": insights_results,
                "components_analyzed": list(components_results.keys()),
                "timestamp": datetime.now().isoformat()
            }
            
            # Salva insights gerados
            auto_save_manager.salvar_etapa(
                "master_insights_phase",
                insights_data,
                session_id=self.session_id,
                categoria="master_engine"
            )
            
            self.components_status["insights"] = "completed"
            return insights_data
            
        except Exception as e:
            self.logger.error(f"❌ MASTER ENGINE: Erro na fase de insights: {e}")
            self.components_status["insights"] = "error"
            return {"status": "error", "error": str(e)}
    
    def _execute_consolidation_phase(
        self, 
        query: str, 
        context: Dict[str, Any], 
        web_results: Dict[str, Any],
        components_results: Dict[str, Any],
        insights_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Executa fase de consolidação final"""
        
        self.logger.info("📋 MASTER ENGINE: Executando fase de consolidação")
        
        try:
            # Consolida todos os resultados
            consolidated_results = {
                "analysis_metadata": {
                    "query": query,
                    "context": context,
                    "session_id": self.session_id,
                    "timestamp": datetime.now().isoformat(),
                    "engine": "MasterAnalysisEngine",
                    "components_status": self.components_status
                },
                "web_search_results": web_results,
                "components_analysis": components_results,
                "insights_generated": insights_results,
                "final_report": None
            }
            
            # Gera relatório final profissional
            final_report = professional_report_manager.generate_comprehensive_report(
                consolidated_results, session_id=self.session_id
            )
            
            consolidated_results["final_report"] = final_report
            
            # Salva consolidação final
            auto_save_manager.salvar_etapa(
                "master_consolidation_final",
                consolidated_results,
                session_id=self.session_id,
                categoria="master_engine"
            )
            
            self.components_status["consolidation"] = "completed"
            self.logger.info("✅ MASTER ENGINE: Consolidação final concluída")
            
            return consolidated_results
            
        except Exception as e:
            self.logger.error(f"❌ MASTER ENGINE: Erro na consolidação: {e}")
            self.components_status["consolidation"] = "error"
            return {"status": "error", "error": str(e)}
    
    def _build_insights_prompt(
        self, 
        query: str, 
        context: Dict[str, Any], 
        components_results: Dict[str, Any]
    ) -> str:
        """Constrói prompt para geração de insights"""
        
        prompt = f"""
# GERAÇÃO DE INSIGHTS ESTRATÉGICOS AVANÇADOS

## ANÁLISE SOLICITADA
Query: {query}
Contexto: {context}

## RESULTADOS DOS COMPONENTES ANALISADOS
{self._format_components_for_prompt(components_results)}

## TAREFA: GERAR INSIGHTS ESTRATÉGICOS

Analise todos os dados coletados e gere insights estratégicos únicos e acionáveis que incluam:

1. **INSIGHTS DE MERCADO**
   - Tendências identificadas
   - Oportunidades específicas
   - Gaps no mercado

2. **INSIGHTS COMPETITIVOS**
   - Posicionamento dos concorrentes
   - Vantagens competitivas potenciais
   - Estratégias diferenciadas

3. **INSIGHTS DE PÚBLICO**
   - Comportamentos identificados
   - Necessidades não atendidas
   - Segmentos promissores

4. **INSIGHTS ESTRATÉGICOS**
   - Recomendações específicas
   - Próximos passos
   - Métricas importantes

## FORMATO DE RESPOSTA
Forneça insights únicos, específicos e baseados nos dados analisados.
"""
        
        return prompt
    
    def _format_components_for_prompt(self, components_results: Dict[str, Any]) -> str:
        """Formata resultados dos componentes para o prompt"""
        
        formatted = ""
        
        for component, result in components_results.items():
            formatted += f"\n### {component.upper()}\n"
            
            if isinstance(result, dict):
                for key, value in result.items():
                    if isinstance(value, (str, int, float)):
                        formatted += f"- {key}: {value}\n"
                    elif isinstance(value, list) and value:
                        formatted += f"- {key}: {', '.join(map(str, value[:3]))}\n"
            else:
                formatted += f"- Resultado: {str(result)[:200]}...\n"
        
        return formatted
    
    def get_analysis_status(self) -> Dict[str, Any]:
        """Retorna status atual da análise"""
        return {
            "session_id": self.session_id,
            "components_status": self.components_status,
            "timestamp": datetime.now().isoformat()
        }

# Instância global
master_analysis_engine = MasterAnalysisEngine()
