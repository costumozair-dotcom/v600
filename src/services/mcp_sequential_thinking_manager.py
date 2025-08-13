
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - MCP Sequential Thinking Manager
Gerenciador de raciocínio sequencial para análises complexas
"""

import os
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class MCPSequentialThinkingManager:
    """Gerenciador de raciocínio sequencial para análises complexas"""

    def __init__(self):
        """Inicializa o manager de pensamento sequencial"""
        self.thinking_steps = [
            'data_analysis',
            'pattern_recognition', 
            'insight_generation',
            'strategic_conclusions',
            'actionable_recommendations'
        ]
        
        self.step_prompts = {
            'data_analysis': """
Analise os dados fornecidos de forma sistemática:
1. Identifique os principais pontos de dados
2. Classifique informações por relevância
3. Detecte tendências e padrões iniciais
4. Avalie a qualidade e completude dos dados

Dados para análise: {data}
""",
            'pattern_recognition': """
Com base na análise anterior, identifique padrões mais profundos:
1. Correlações entre diferentes variáveis
2. Padrões comportamentais do público
3. Tendências de mercado emergentes
4. Oportunidades e ameaças implícitas

Análise anterior: {previous_step}
Dados originais: {data}
""",
            'insight_generation': """
Gere insights estratégicos baseados nos padrões identificados:
1. Insights sobre o comportamento do consumidor
2. Oportunidades de mercado não exploradas
3. Pontos de diferenciação competitiva
4. Riscos e desafios potenciais

Padrões identificados: {previous_step}
Contexto completo: {data}
""",
            'strategic_conclusions': """
Formule conclusões estratégicas sólidas:
1. Posicionamento recomendado no mercado
2. Estratégias de entrada ou expansão
3. Vantagens competitivas sustentáveis
4. Roadmap estratégico de alto nível

Insights gerados: {previous_step}
Contexto do negócio: {data}
""",
            'actionable_recommendations': """
Desenvolva recomendações práticas e acionáveis:
1. Ações imediatas (0-30 dias)
2. Estratégias de médio prazo (1-6 meses)
3. Iniciativas de longo prazo (6+ meses)
4. KPIs e métricas de acompanhamento

Conclusões estratégicas: {previous_step}
Contexto operacional: {data}
"""
        }
        
        logger.info("🧠 MCP Sequential Thinking Manager inicializado")

    def execute_sequential_analysis(
        self,
        data: Dict[str, Any],
        session_id: str,
        focus_area: str = "market_analysis",
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """Executa análise sequencial completa"""
        
        try:
            logger.info(f"🧠 Iniciando análise sequencial - Foco: {focus_area}")
            start_time = time.time()
            
            results = {
                'session_id': session_id,
                'focus_area': focus_area,
                'steps_completed': [],
                'step_results': {},
                'final_synthesis': {},
                'execution_metrics': {}
            }
            
            # Executa cada etapa sequencialmente
            previous_result = ""
            
            for i, step in enumerate(self.thinking_steps):
                try:
                    if progress_callback:
                        progress_callback(
                            i + 1, 
                            f"🧠 Executando etapa {i+1}/5: {step.replace('_', ' ').title()}"
                        )
                    
                    logger.info(f"🔄 Executando etapa: {step}")
                    
                    step_result = self._execute_thinking_step(
                        step, data, previous_result, session_id
                    )
                    
                    if step_result and step_result.get('success'):
                        results['steps_completed'].append(step)
                        results['step_results'][step] = step_result
                        previous_result = step_result.get('content', '')
                        
                        # Salva resultado da etapa
                        salvar_etapa(f"sequential_thinking_{step}", step_result, 
                                   categoria="drivers_mentais", session_id=session_id)
                        
                        logger.info(f"✅ Etapa {step} concluída")
                    else:
                        logger.warning(f"⚠️ Etapa {step} falhou - continuando")
                        
                except Exception as e:
                    logger.error(f"❌ Erro na etapa {step}: {e}")
                    salvar_erro(f"sequential_thinking_{step}_error", e, 
                              contexto={'session_id': session_id, 'step': step})
                    continue
            
            # Síntese final
            if progress_callback:
                progress_callback(6, "🔮 Gerando síntese final do raciocínio...")
            
            final_synthesis = self._generate_final_synthesis(results, data, session_id)
            results['final_synthesis'] = final_synthesis
            
            execution_time = time.time() - start_time
            results['execution_metrics'] = {
                'total_time': execution_time,
                'steps_successful': len(results['steps_completed']),
                'completion_rate': (len(results['steps_completed']) / len(self.thinking_steps)) * 100
            }
            
            # Salva resultado final
            salvar_etapa("sequential_thinking_complete", results, 
                       categoria="analise_completa", session_id=session_id)
            
            logger.info(f"✅ Análise sequencial concluída em {execution_time:.2f}s")
            
            return {
                'success': True,
                'results': results,
                'completion_rate': results['execution_metrics']['completion_rate'],
                'execution_time': execution_time
            }
            
        except Exception as e:
            logger.error(f"❌ Erro crítico na análise sequencial: {e}")
            salvar_erro("sequential_thinking_critical", e, 
                      contexto={'session_id': session_id, 'focus_area': focus_area})
            
            return {
                'success': False,
                'error': str(e),
                'session_id': session_id
            }

    def _execute_thinking_step(
        self,
        step: str,
        data: Dict[str, Any],
        previous_result: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Executa uma etapa específica do pensamento"""
        
        try:
            prompt_template = self.step_prompts.get(step, "")
            if not prompt_template:
                return {'success': False, 'error': f'Prompt não encontrado para etapa: {step}'}
            
            # Formata prompt com dados
            formatted_prompt = prompt_template.format(
                data=str(data),
                previous_step=previous_result
            )
            
            # Executa com AI Manager
            ai_response = ai_manager.generate_response(
                formatted_prompt,
                max_tokens=2000,
                temperature=0.7,
                system_prompt=f"Você é um especialista em {step.replace('_', ' ')} realizando análise estratégica profunda."
            )
            
            if ai_response and ai_response.get('success'):
                return {
                    'success': True,
                    'step': step,
                    'content': ai_response.get('content', ''),
                    'provider_used': ai_response.get('provider', 'unknown'),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'step': step,
                    'error': ai_response.get('error', 'AI response failed')
                }
                
        except Exception as e:
            logger.error(f"❌ Erro executando etapa {step}: {e}")
            return {
                'success': False,
                'step': step,
                'error': str(e)
            }

    def _generate_final_synthesis(
        self,
        results: Dict[str, Any],
        original_data: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Gera síntese final do raciocínio sequencial"""
        
        try:
            # Compila todos os resultados das etapas
            all_insights = []
            for step, result in results['step_results'].items():
                if result.get('success'):
                    all_insights.append(f"{step.replace('_', ' ').title()}:\n{result.get('content', '')}")
            
            synthesis_prompt = f"""
Com base no raciocínio sequencial completo realizado, gere uma síntese final que:

1. Integre todos os insights das etapas anteriores
2. Identifique os 3 pontos mais críticos para o negócio
3. Apresente uma recomendação estratégica clara
4. Sugira próximos passos práticos

Etapas do raciocínio:
{chr(10).join(all_insights)}

Contexto original do negócio:
Segmento: {original_data.get('segmento', '')}
Produto: {original_data.get('produto', '')}
Público: {original_data.get('publico', '')}

Forneça uma síntese executiva concisa mas abrangente.
"""
            
            ai_response = ai_manager.generate_response(
                synthesis_prompt,
                max_tokens=1500,
                temperature=0.6,
                system_prompt="Você é um consultor estratégico senior gerando síntese executiva."
            )
            
            if ai_response and ai_response.get('success'):
                return {
                    'success': True,
                    'synthesis': ai_response.get('content', ''),
                    'steps_integrated': len(results['steps_completed']),
                    'provider_used': ai_response.get('provider', 'unknown'),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': 'Falha na geração da síntese final'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro gerando síntese final: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Instância global
mcp_sequential_thinking_manager = MCPSequentialThinkingManager()
