#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Sistema Anti-Objeção
Sistema avançado para identificação e neutralização de objeções
"""

import logging
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from services.ai_manager import ai_manager

logger = logging.getLogger(__name__)

class AntiObjectionSystem:
    """Sistema especializado em neutralização de objeções"""

    def __init__(self):
        self.objecoes_universais = {
            "TEMPO": {
                "categoria": "Recurso",
                "manifestacoes": ["Não tenho tempo", "Muito ocupado", "Talvez mais tarde"],
                "raiz_emocional": "Medo de mais compromissos"
            },
            "DINHEIRO": {
                "categoria": "Financeira",
                "manifestacoes": ["Muito caro", "Sem orçamento", "Preciso pensar"],
                "raiz_emocional": "Medo de perda financeira"
            },
            "CONFIANCA": {
                "categoria": "Credibilidade",
                "manifestacoes": ["Não conheço vocês", "Parece bom demais", "Já fui enganado"],
                "raiz_emocional": "Medo de ser enganado"
            },
            "AUTOSSUFICIENCIA": {
                "categoria": "Ego",
                "manifestacoes": ["Consigo sozinho", "Já tentei tudo", "Conheço o assunto"],
                "raiz_emocional": "Medo de admitir fragilidade"
            },
            "TIMING": {
                "categoria": "Circunstancial",
                "manifestacoes": ["Não é o momento", "Muita coisa acontecendo", "Depois resolvo"],
                "raiz_emocional": "Medo da mudança"
            },
            "COMPLEXIDADE": {
                "categoria": "Capacidade",
                "manifestacoes": ["Parece complicado", "Não sei se conseguiria", "É muito técnico"],
                "raiz_emocional": "Medo de não conseguir executar"
            }
        }

    async def create_comprehensive_anti_objection_system(self, dados_entrada: Dict[str, Any]) -> Dict[str, Any]:
        """MÉTODO PRINCIPAL - Cria sistema completo anti-objeção personalizado"""
        try:
            logger.info("🛡️ Iniciando criação do sistema anti-objeção...")

            # Extrai dados de entrada
            avatar = dados_entrada.get('avatar', {})
            produto = dados_entrada.get('produto', 'Produto')
            funil = dados_entrada.get('funil_vendas', {})
            pesquisas = dados_entrada.get('pesquisas', [])
            historico_objecoes = dados_entrada.get('historico_objecoes', [])

            # Análise psicológica da audiência
            perfil_psicologico = await self._analisar_perfil_psicologico(avatar, pesquisas)

            # Diagnóstico completo de objeções
            diagnostico_objecoes = await self._diagnosticar_objecoes(
                avatar, historico_objecoes, pesquisas
            )

            # Desenvolvimento de arsenal de drivers mentais
            arsenal_drivers = await self._criar_arsenal_drivers_mentais(
                diagnostico_objecoes, perfil_psicologico, produto
            )

            # Sistema de implementação
            sistema_implementacao = await self._criar_sistema_implementacao(
                arsenal_drivers, funil, avatar
            )

            # Kit de emergência
            kit_emergencia = await self._criar_kit_emergencia(
                diagnostico_objecoes, arsenal_drivers
            )

            sistema_completo = {
                "produto": produto,
                "timestamp": datetime.now().isoformat(),
                "resumo_executivo": await self._criar_resumo_executivo(
                    perfil_psicologico, diagnostico_objecoes, arsenal_drivers
                ),
                "analise_psicologica_detalhada": perfil_psicologico,
                "diagnostico_objecoes": diagnostico_objecoes,
                "arsenal_drivers_mentais": arsenal_drivers,
                "sistema_implementacao": sistema_implementacao,
                "kit_emergencia": kit_emergencia,
                "metricas_eficacia": await self._definir_metricas_eficacia()
            }

            logger.info("✅ Sistema anti-objeção criado com sucesso")
            return sistema_completo

        except Exception as e:
            logger.error(f"❌ Erro ao criar sistema anti-objeção: {e}")
            return self._create_fallback_system(str(e))

    async def criar_sistema_anti_objecao(self, dados_entrada: Dict[str, Any]) -> Dict[str, Any]:
        """Método alternativo - chama o método principal"""
        return await self.create_comprehensive_anti_objection_system(dados_entrada)

    def _create_fallback_system(self, error_msg: str) -> Dict[str, Any]:
        """Cria sistema anti-objeção básico em caso de falha"""
        return {
            'status': 'fallback',
            'sistema_anti_objecao': {
                'objecoes_mapeadas': [
                    'Preço alto',
                    'Falta de confiança',
                    'Complexidade da solução',
                    'Falta de tempo',
                    'Comparação com concorrentes'
                ],
                'respostas_preparadas': [
                    'Demonstração de ROI e valor agregado',
                    'Apresentação de casos de sucesso e depoimentos',
                    'Explicação simplificada do processo',
                    'Proposta de implementação gradual',
                    'Análise comparativa de diferenciais'
                ],
                'estrategias_aplicacao': [
                    'Usar prova social',
                    'Mostrar garantias',
                    'Oferecer teste gratuito',
                    'Apresentar plano de implementação',
                    'Destacar exclusividade'
                ]
            },
            'error_details': error_msg,
            'fallback_used': True,
            'timestamp': datetime.now().isoformat()
        }

    async def _analisar_perfil_psicologico(self, avatar: Dict, pesquisas: List) -> Dict[str, Any]:
        """Análise psicológica profunda da audiência"""

        prompt = f"""
        Como ESPECIALISTA EM PSICOLOGIA DE VENDAS, analise o perfil psicológico para identificar padrões de objeção:

        AVATAR: {json.dumps(avatar, indent=2)}
        PESQUISAS: {json.dumps(pesquisas[:3], indent=2) if pesquisas else "Não disponível"}

        Forneça análise psicológica estruturada:

        1. PERFIL PSICOLÓGICO DA AUDIÊNCIA
        - Traços de personalidade dominantes
        - Padrões de tomada de decisão
        - Níveis de resistência típicos
        - Mecanismos de defesa mais comuns

        2. TOP 3 OBJEÇÕES MAIS CRÍTICAS
        - Objeções verbalizadas com mais frequência
        - Intensidade emocional de cada objeção
        - Momento típico de manifestação
        - Raiz psicológica profunda

        3. ESTRATÉGIA GERAL DE NEUTRALIZAÇÃO
        - Abordagem psicológica mais eficaz
        - Sequência ideal de neutralização
        - Tom e linguagem recomendados
        - Momentos estratégicos de intervenção

        4. MOMENTOS CRÍTICOS DO LANÇAMENTO
        - Quando as objeções são mais prováveis
        - Pontos de maior resistência
        - Oportunidades de prevenção
        - Sinais de alerta para monitorar

        Seja visceral e baseado em psicologia profunda.
        """

        try:
            resposta = await asyncio.wait_for(
                ai_manager.generate_analysis(prompt, modelo_preferido="gemini"),
                timeout=60.0
            )
            return {
                "analise_completa": resposta,
                "processado_em": datetime.now().isoformat(),
                "dados_analisados": len(pesquisas)
            }
        except Exception as e:
            logger.error(f"Erro na análise psicológica: {e}")
            return {
                "erro": str(e),
                "analise_fallback": "Análise psicológica básica: Avatar típico de mercado B2B/B2C com resistências padrão relacionadas a preço, tempo e confiança."
            }

    async def _diagnosticar_objecoes(self, avatar: Dict, historico: List, pesquisas: List) -> Dict[str, Any]:
        """Diagnóstico completo das objeções universais e ocultas"""

        prompt = f"""
        Como ESPECIALISTA EM PSICOLOGIA DE VENDAS, realize diagnóstico forense das objeções:

        AVATAR: {json.dumps(avatar, indent=2)}
        HISTÓRICO DE OBJEÇÕES: {json.dumps(historico, indent=2) if historico else "Não disponível"}
        PESQUISAS: {json.dumps(pesquisas[:3], indent=2) if pesquisas else "Não disponível"}

        OBJEÇÕES UNIVERSAIS CONHECIDAS:
        {json.dumps(self.objecoes_universais, indent=2)}

        Realize análise forense completa:

        1. MAPEAMENTO EMOCIONAL DAS RESPOSTAS
        - Como cada objeção se manifesta emocionalmente
        - Linguagem corporal e verbal típica
        - Estados emocionais associados
        - Intensidade de cada reação

        2. IDENTIFICAÇÃO DE PADRÕES COMPORTAMENTAIS
        - Sequência típica de objeções
        - Padrões de escalada
        - Comportamentos de evitação
        - Sinais precursores

        3. DIAGNÓSTICO DAS OBJEÇÕES UNIVERSAIS
        - Quais das objeções universais são mais relevantes
        - Como se manifestam especificamente neste avatar
        - Frequência e intensidade de cada uma
        - Momentos de maior probabilidade

        4. DIAGNÓSTICO DAS OBJEÇÕES OCULTAS
        - Objeções não verbalizadas
        - Resistências subconscientes
        - Medos não admitidos
        - Autossabotagens típicas

        5. PERFIS/PERSONAS PRINCIPAIS
        - Diferentes tipos dentro do avatar
        - Objeções específicas por perfil
        - Estratégias diferenciadas necessárias
        - Hierarquia de resistência

        Seja extremamente detalhado e psicologicamente profundo.
        """

        try:
            resposta = await asyncio.wait_for(
                ai_manager.generate_analysis(prompt, modelo_preferido="gemini"),
                timeout=60.0
            )
            return {
                "diagnostico_completo": resposta,
                "objecoes_mapeadas": len(self.objecoes_universais),
                "processado_em": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro no diagnóstico de objeções: {e}")
            return {
                "erro": str(e),
                "diagnostico_fallback": "Diagnóstico básico: Objeções universais aplicáveis - TEMPO, DINHEIRO, CONFIANÇA como principais resistências."
            }

    async def _criar_arsenal_drivers_mentais(self, diagnostico: Dict, perfil: Dict, produto: str) -> Dict[str, Any]:
        """Cria arsenal completo de drivers mentais anti-objeção"""

        prompt = f"""
        Como ESPECIALISTA EM PSICOLOGIA DE VENDAS, crie arsenal de drivers mentais:

        PRODUTO: {produto}
        DIAGNÓSTICO: {json.dumps(diagnostico, indent=2)}
        PERFIL PSICOLÓGICO: {json.dumps(perfil, indent=2)}

        Crie 5+ DRIVERS MENTAIS ESPECÍFICOS, cada um com:

        1. NOME IMPACTANTE DO DRIVER
        2. OBJEÇÃO-ALVO (qual objeção neutraliza)
        3. GATILHO PSICOLÓGICO CENTRAL
        4. MECÂNICA DE FUNCIONAMENTO
        - Como funciona psicologicamente
        - Por que é eficaz para este avatar
        - Timing ideal de aplicação

        5. ROTEIRO COMPLETO DE INSTALAÇÃO
        - Setup (como introduzir)
        - Desenvolvimento (como implantar)
        - Clímax (momento de máximo impacto)
        - Ancoragem (como fixar)

        6. TEMPLATES E SCRIPTS PERSONALIZADOS
        - Scripts específicos por situação
        - Variações por formato (CPL, webinar, live)
        - Frases de máximo impacto
        - Palavras-gatilho específicas

        7. HISTÓRIAS E CASOS PARA CADA SITUAÇÃO
        - Narrativas que demonstram o conceito
        - Casos reais ou fictícios relevantes
        - Provas sociais específicas
        - Analogias poderosas

        8. LINGUAGEM ESPECÍFICA PARA CADA PERFIL
        - Adaptações por tipo de persona
        - Tom e estilo por situação
        - Palavras que ressoam
        - Termos que devem evitar

        Para cada driver, seja visceralmente específico e acionável.
        """

        try:
            resposta = await asyncio.wait_for(
                ai_manager.generate_analysis(prompt, modelo_preferido="gemini"),
                timeout=90.0
            )
            return {
                "arsenal_completo": resposta,
                "total_drivers": "5+",
                "criado_em": datetime.now().isoformat(),
                "produto": produto
            }
        except Exception as e:
            logger.error(f"Erro ao criar arsenal de drivers: {e}")
            return {
                "erro": str(e),
                "arsenal_fallback": "Arsenal básico: Drivers de urgência, escassez, prova social, autoridade e reciprocidade adaptados ao produto."
            }

    async def _criar_sistema_implementacao(self, arsenal: Dict, funil: Dict, avatar: Dict) -> Dict[str, Any]:
        """Cria sistema completo de implementação"""

        prompt = f"""
        Como ESPECIALISTA EM PSICOLOGIA DE VENDAS, crie sistema de implementação:

        ARSENAL DE DRIVERS: {json.dumps(arsenal, indent=2)}
        FUNIL DE VENDAS: {json.dumps(funil, indent=2)}
        AVATAR: {json.dumps(avatar, indent=2)}

        Crie sistema com:

        1. CRONOGRAMA DE USO POR ESTÁGIO
        - Que drivers usar em cada etapa do funil
        - Timing específico de cada aplicação
        - Sequência psicológica otimizada
        - Intervalos entre aplicações

        2. PERSONALIZAÇÃO POR PERSONA
        - Adaptações para diferentes perfis
        - Intensidade por tipo de pessoa
        - Linguagem específica
        - Abordagens diferenciadas

        3. ORDEM PSICOLÓGICA IDEAL
        - Sequência de máximo impacto
        - Como escalar a intensidade
        - Momentos de reforço
        - Protocolo de recuperação

        4. MÉTRICAS DE EFICÁCIA
        - Como medir sucesso de cada driver
        - Indicadores de resistência
        - Sinais de aceitação
        - Métricas de conversão

        Seja extremamente prático e acionável.
        """

        try:
            resposta = await asyncio.wait_for(
                ai_manager.generate_analysis(prompt, modelo_preferido="gemini"),
                timeout=60.0
            )
            return {
                "sistema_completo": resposta,
                "criado_em": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao criar sistema de implementação: {e}")
            return {
                "erro": str(e),
                "implementacao_fallback": "Sistema básico: Aplicação sequencial por estágio do funil com monitoramento de engajamento."
            }

    async def _criar_kit_emergencia(self, diagnostico: Dict, arsenal: Dict) -> Dict[str, Any]:
        """Cria kit de emergência para objeções de última hora"""

        prompt = f"""
        Como ESPECIALISTA EM PSICOLOGIA DE VENDAS, crie kit de emergência:

        DIAGNÓSTICO: {json.dumps(diagnostico, indent=2)}
        ARSENAL: {json.dumps(arsenal, indent=2)}

        Crie kit com:

        1. OBJEÇÕES DE ÚLTIMA HORA
        - Objeções típicas no momento da decisão
        - Resistências de emergência
        - Autossabotagens finais
        - Medos de comprador

        2. PRIMEIROS SOCORROS PSICOLÓGICOS
        - Protocolos de resposta imediata
        - Como lidar com resistência intensa
        - Técnicas de desescalada
        - Estratégias de reconexão

        3. SCRIPTS DE EMERGÊNCIA
        - Respostas prontas para cada situação
        - Frases de impacto imediato
        - Perguntas que quebram resistência
        - Técnicas de redirecionamento

        4. SINAIS DE ALERTA
        - Como identificar resistência crescente
        - Linguagem corporal de alerta
        - Padrões comportamentais problemáticos
        - Momentos de intervenção crítica

        Seja prático para situações de alta pressão.
        """

        try:
            resposta = await asyncio.wait_for(
                ai_manager.generate_analysis(prompt, modelo_preferido="gemini"),
                timeout=60.0
            )
            return {
                "kit_completo": resposta,
                "criado_em": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao criar kit de emergência: {e}")
            return {
                "erro": str(e),
                "kit_fallback": "Kit básico: Respostas rápidas para objeções de preço, tempo e decisão com técnicas de fechamento."
            }

    async def _criar_resumo_executivo(self, perfil: Dict, diagnostico: Dict, arsenal: Dict) -> Dict[str, Any]:
        """Cria resumo executivo do sistema"""

        return {
            "visao_geral": "Sistema anti-objeção personalizado criado com base em análise psicológica profunda",
            "principais_objecoes": "Identificadas objeções universais e ocultas específicas do avatar",
            "arsenal_drivers": "Criados 5+ drivers mentais específicos para neutralização",
            "sistema_implementacao": "Protocolo completo de implementação por estágio do funil",
            "kit_emergencia": "Kit de primeiros socorros para situações críticas",
            "nivel_personalizacao": "Máximo - adaptado especificamente para este avatar",
            "confiabilidade": "Alta - baseado em dados reais e análise psicológica",
            "criado_em": datetime.now().isoformat()
        }

    async def _definir_metricas_eficacia(self) -> Dict[str, Any]:
        """Define métricas de eficácia do sistema"""

        return {
            "metricas_primarias": [
                "Taxa de redução de objeções por estágio",
                "Tempo médio de neutralização",
                "Taxa de conversão pós-neutralização",
                "Nível de engajamento durante aplicação"
            ],
            "metricas_secundarias": [
                "Qualidade da interação pós-driver",
                "Feedback qualitativo dos prospects",
                "Taxa de reengajamento",
                "Progressão no funil após neutralização"
            ],
            "indicadores_comportamentais": [
                "Linguagem corporal (presencial)",
                "Engajamento no chat (online)",
                "Tempo de resposta a perguntas",
                "Qualidade das perguntas feitas"
            ],
            "protocolo_medicao": {
                "frequencia": "Por aplicação de driver",
                "responsavel": "Equipe de vendas/apresentador",
                "ferramentas": "Observação direta + métricas digitais",
                "relatorios": "Semanais com análise de eficácia"
            }
        }

    # Métodos auxiliares para compatibilidade
    async def generate_anti_objection_system(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Método de compatibilidade"""
        return await self.create_comprehensive_anti_objection_system(dados)

    async def create_objection_neutralization_system(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Método de compatibilidade"""
        return await self.create_comprehensive_anti_objection_system(dados)

# Instância global
anti_objection_engine = AntiObjectionSystem()
anti_objection_system = anti_objection_engine  # Export para compatibilidade
