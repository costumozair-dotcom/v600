
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Arqueólogo do Avatar
Sistema avançado para análise profunda de avatares
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from services.ai_manager import ai_manager

logger = logging.getLogger(__name__)

class AvatarArqueologicoAnalyzer:
    """Arqueólogo especializado em análise profunda de avatares"""

    def __init__(self):
        self.dimensoes_analise = {
            "demografica": ["idade", "genero", "localizacao", "renda", "educacao"],
            "psicografica": ["valores", "crenças", "personalidade", "estilo_vida"],
            "comportamental": ["habitos", "padroes_compra", "canais_preferidos"],
            "emocional": ["dores", "desejos", "medos", "frustracoes"],
            "social": ["influencias", "grupos", "status", "aspiracoes"]
        }
        
    async def criar_dashboard_arqueologico(self, dados_entrada: Dict[str, Any]) -> Dict[str, Any]:
        """Cria dashboard arqueológico completo do avatar"""
        try:
            logger.info("🏺 Iniciando análise arqueológica do avatar...")
            
            # Extrai dados de entrada
            pesquisas = dados_entrada.get('pesquisas', [])
            interacoes = dados_entrada.get('interacoes', [])
            contexto = dados_entrada.get('contexto', {})
            produto = dados_entrada.get('produto', 'Produto')
            
            # Análise multidimensional
            perfil_demografico = await self._analisar_dimensao_demografica(pesquisas)
            analise_dores = await self._analisar_dores_profundas(pesquisas, interacoes)
            desejos_motivacoes = await self._analisar_desejos_motivacoes(pesquisas)
            comportamento = await self._analisar_comportamento(interacoes, pesquisas)
            insights_ocultos = await self._descobrir_insights_ocultos(
                perfil_demografico, analise_dores, desejos_motivacoes, comportamento
            )
            
            # Criação do avatar final
            avatar_consolidado = await self._consolidar_avatar(
                perfil_demografico, analise_dores, desejos_motivacoes, 
                comportamento, insights_ocultos, produto
            )
            
            dashboard = {
                "produto": produto,
                "timestamp": datetime.now().isoformat(),
                "perfil_demografico_psicografico": perfil_demografico,
                "analise_dores": analise_dores,
                "desejos_motivacoes": desejos_motivacoes, 
                "comportamento": comportamento,
                "insights_ocultos_recomendacoes": insights_ocultos,
                "avatar_consolidado": avatar_consolidado,
                "metricas_confianca": await self._calcular_metricas_confianca(pesquisas, interacoes)
            }
            
            logger.info("✅ Dashboard arqueológico criado com sucesso")
            return dashboard
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar dashboard arqueológico: {e}")
            return {"erro": str(e)}
    
    async def _analisar_dimensao_demografica(self, pesquisas: List) -> Dict[str, Any]:
        """Análise demográfica e psicográfica detalhada"""
        
        prompt = f"""
        Como ARQUEÓLOGO DO AVATAR, analise os dados demográficos e psicográficos:
        
        DADOS DE PESQUISAS: {json.dumps(pesquisas[:5], indent=2) if pesquisas else "Não disponível"}
        
        Forneça análise estruturada:
        
        1. DISTRIBUIÇÃO POR FATURAMENTO/SEGMENTO
        - Faixas de faturamento predominantes
        - Segmentos de negócio mais comuns
        - Correlações entre faturamento e desafios
        
        2. PRINCIPAIS DESAFIOS IDENTIFICADOS
        - Top 5 desafios mais mencionados
        - Desafios por segmento de faturamento
        - Intensidade emocional de cada desafio
        
        3. ARQUÉTIPOS DOMINANTES
        - Personalidades predominantes
        - Padrões de comportamento
        - Estilos de liderança
        
        4. MEDOS QUE PARALISAM DECISÕES
        - Medos mais frequentes
        - Como estes medos afetam decisões
        - Padrões de autossabotagem
        
        Seja detalhado e baseado em dados reais.
        """
        
        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "analise_completa": resposta,
                "processado_em": datetime.now().isoformat(),
                "fonte_dados": len(pesquisas)
            }
        except Exception as e:
            logger.error(f"Erro na análise demográfica: {e}")
            return {"erro": str(e)}
    
    async def _analisar_dores_profundas(self, pesquisas: List, interacoes: List) -> Dict[str, Any]:
        """Análise profunda das dores do avatar"""
        
        prompt = f"""
        Como ARQUEÓLOGO DO AVATAR, realize análise forense das dores:
        
        PESQUISAS: {json.dumps(pesquisas[:3], indent=2) if pesquisas else "Não disponível"}
        INTERAÇÕES: {json.dumps(interacoes[:3], indent=2) if interacoes else "Não disponível"}
        
        Analise as dores em 4 dimensões:
        
        1. TOP 5 DORES ESTRUTURADAS (com frequência %)
        - Dor específica
        - Frequência de menção
        - Intensidade emocional (1-10)
        - Contexto de manifestação
        - Impacto na vida/negócio
        
        2. DORES ABERTAS vs ESTRUTURADAS
        - Dores que as pessoas falam abertamente
        - Dores que elas escondem ou minimizam
        - Dores que nem sabem que têm
        - Discrepâncias entre discurso e realidade
        
        3. ANÁLISE COMPARATIVA
        - Dores por faixa de faturamento
        - Dores por tipo de negócio
        - Evolução das dores ao longo do tempo
        - Correlações ocultas
        
        4. INSIGHTS OCULTOS
        - Padrões não óbvios identificados
        - Contradições reveladas
        - Dores sistêmicas vs pontuais
        - Oportunidades de intervenção
        
        Seja visceral e direto. Mergulhe no que realmente dói.
        """
        
        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "analise_dores": resposta,
                "processado_em": datetime.now().isoformat(),
                "fontes_analisadas": len(pesquisas) + len(interacoes)
            }
        except Exception as e:
            logger.error(f"Erro na análise de dores: {e}")
            return {"erro": str(e)}
    
    async def _analisar_desejos_motivacoes(self, pesquisas: List) -> Dict[str, Any]:
        """Análise profunda de desejos e motivações"""
        
        prompt = f"""
        Como ARQUEÓLOGO DO AVATAR, desvende os desejos mais profundos:
        
        DADOS: {json.dumps(pesquisas[:3], indent=2) if pesquisas else "Não disponível"}
        
        Analise em 4 dimensões:
        
        1. SONHOS MAIS PROFUNDOS
        - O que realmente querem alcançar
        - Visão de futuro ideal
        - Estados emocionais desejados
        - Símbolos de sucesso para eles
        
        2. DESEJOS EXPRESSOS DIRETAMENTE
        - O que falam que querem
        - Objetivos declarados
        - Metas mencionadas
        - Aspirações verbalizadas
        
        3. CONTRADIÇÕES IDENTIFICADAS
        - Discrepâncias entre fala e comportamento
        - Desejos conflitantes
        - Autossabotagem inconsciente
        - Resistências internas
        
        4. HIERARQUIA DE DESEJOS
        - Desejos primários (mais urgentes)
        - Desejos secundários (importantes mas não urgentes)
        - Desejos ocultos (não verbalizados)
        - Motivações verdadeiras vs aparentes
        
        Seja psicológico e profundo.
        """
        
        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "analise_desejos": resposta,
                "processado_em": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro na análise de desejos: {e}")
            return {"erro": str(e)}
    
    async def _analisar_comportamento(self, interacoes: List, pesquisas: List) -> Dict[str, Any]:
        """Análise comportamental detalhada"""
        
        prompt = f"""
        Como ARQUEÓLOGO DO AVATAR, analise padrões comportamentais:
        
        INTERAÇÕES: {json.dumps(interacoes[:3], indent=2) if interacoes else "Não disponível"}
        PESQUISAS: {json.dumps(pesquisas[:3], indent=2) if pesquisas else "Não disponível"}
        
        Forneça análise em 4 áreas:
        
        1. ARQUÉTIPOS DOMINANTES
        - Personalidades mais comuns
        - Estilos de comunicação
        - Padrões de tomada de decisão
        - Influências que seguem
        
        2. MEDOS QUE PARALISAM
        - Medos mais frequentes
        - Como se manifestam comportamentalmente
        - Mecanismos de defesa
        - Padrões de evitação
        
        3. OBJEÇÕES REAIS (não as óbvias)
        - Resistências verdadeiras
        - Objeções não verbalizadas
        - Desculpas vs razões reais
        - Gatilhos de resistência
        
        4. PADRÕES DE DECISÃO
        - Como tomam decisões importantes
        - Influências externas críticas
        - Tempo de maturação típico
        - Fatores determinantes finais
        
        Foque nos padrões invisíveis.
        """
        
        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "analise_comportamental": resposta,
                "processado_em": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro na análise comportamental: {e}")
            return {"erro": str(e)}
    
    async def _descobrir_insights_ocultos(self, perfil: Dict, dores: Dict, desejos: Dict, comportamento: Dict) -> Dict[str, Any]:
        """Descobre insights ocultos e gera recomendações"""
        
        prompt = f"""
        Como ARQUEÓLOGO DO AVATAR, descubra insights ocultos e gere recomendações:
        
        PERFIL: {json.dumps(perfil, indent=2)}
        DORES: {json.dumps(dores, indent=2)}
        DESEJOS: {json.dumps(desejos, indent=2)}
        COMPORTAMENTO: {json.dumps(comportamento, indent=2)}
        
        Gere insights e recomendações em 4 dimensões:
        
        1. GATILHOS EMOCIONAIS EFICAZES
        - Top 5 gatilhos mais poderosos
        - Como ativar cada gatilho
        - Momentos ideais de aplicação
        - Palavras/frases que funcionam
        
        2. ABORDAGENS DE MAIOR IMPACTO
        - Estratégias de comunicação mais eficazes
        - Ângulos que geram mais conexão
        - Formatos de conteúdo preferidos
        - Timing ideal de abordagem
        
        3. LINGUAGEM RECOMENDADA
        - Palavras que ressoam
        - Termos que devem evitar
        - Tom de voz adequado
        - Metáforas poderosas
        
        4. ESTRATÉGIAS DE POSICIONAMENTO
        - Como se posicionar diante deste avatar
        - Que autoridade demonstrar
        - Como construir confiança
        - Diferenciação estratégica
        
        Seja estratégico e acionável.
        """
        
        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "insights_recomendacoes": resposta,
                "processado_em": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao descobrir insights: {e}")
            return {"erro": str(e)}
    
    async def _consolidar_avatar(self, perfil: Dict, dores: Dict, desejos: Dict, comportamento: Dict, insights: Dict, produto: str) -> Dict[str, Any]:
        """Consolida todas as análises em um avatar final"""
        
        prompt = f"""
        Como ARQUEÓLOGO DO AVATAR, consolide todas as análises em UM AVATAR FINAL visceral:
        
        PRODUTO: {produto}
        PERFIL: {json.dumps(perfil, indent=2)}
        DORES: {json.dumps(dores, indent=2)}
        DESEJOS: {json.dumps(desejos, indent=2)}
        COMPORTAMENTO: {json.dumps(comportamento, indent=2)}
        INSIGHTS: {json.dumps(insights, indent=2)}
        
        Crie AVATAR CONSOLIDADO com:
        
        1. NOME FICTÍCIO REPRESENTATIVO
        
        2. PERFIL DEMOGRÁFICO E PSICOGRÁFICO
        - Idade, localização, faturamento
        - Personalidade dominante
        - Contexto de vida/negócio
        
        3. JORNADA DE DOR DETALHADA
        - Como chegou onde está
        - Tentativas anteriores de solução
        - Frustrações acumuladas
        - Estado atual de desesperança
        
        4. DORES SECRETAS E INCONFESSÁVEIS
        - O que nunca admite publicamente
        - Vergonhas que carrega
        - Medos que paralizam
        - Sentimentos de inadequação
        
        5. DESEJOS ARDENTES E PROIBIDOS
        - O que realmente quer
        - Fantasias de transformação
        - Estados desejados
        - Símbolos de sucesso
        
        6. MEDOS PARALISANTES
        - Que cenários evita
        - Autossabotagens comuns
        - Resistências internas
        - Mecanismos de defesa
        
        7. FRUSTRAÇÕES DIÁRIAS
        - Irritações constantes
        - Problemas recorrentes
        - Fontes de estresse
        - Ciclos viciosos
        
        8. LINGUAGEM INTERNA E EXTERNA
        - Como pensa para si mesmo
        - Como se expressa para outros
        - Palavras que usa
        - Tom emocional típico
        
        9. OBJEÇÕES REAIS
        - Resistências verdadeiras
        - Desculpas que usa
        - Mecanismos de procrastinação
        - Justificativas para não agir
        
        10. DIA PERFEITO E PIOR PESADELO
        - Visão de futuro ideal
        - Cenário que mais teme
        - Contrastes emocionais
        - Motivação por prazer vs dor
        
        Seja visceral, específico e memorável. Este avatar precisa ser TÃO REAL que qualquer pessoa da equipe o reconheceria na rua.
        """
        
        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "avatar_final": resposta,
                "consolidado_em": datetime.now().isoformat(),
                "nivel_detalhamento": "maximo"
            }
        except Exception as e:
            logger.error(f"Erro ao consolidar avatar: {e}")
            return {"erro": str(e)}
    
    async def _calcular_metricas_confianca(self, pesquisas: List, interacoes: List) -> Dict[str, Any]:
        """Calcula métricas de confiança da análise"""
        
        total_dados = len(pesquisas) + len(interacoes)
        
        if total_dados >= 10:
            nivel_confianca = "Alto"
        elif total_dados >= 5:
            nivel_confianca = "Médio"
        else:
            nivel_confianca = "Baixo"
            
        return {
            "total_dados_analisados": total_dados,
            "pesquisas": len(pesquisas),
            "interacoes": len(interacoes),
            "nivel_confianca": nivel_confianca,
            "recomendacao": self._get_recomendacao_confianca(nivel_confianca),
            "calculado_em": datetime.now().isoformat()
        }
    
    def _get_recomendacao_confianca(self, nivel: str) -> str:
        """Retorna recomendação baseada no nível de confiança"""
        recomendacoes = {
            "Alto": "Avatar possui alta confiabilidade. Pode ser usado para estratégias críticas.",
            "Médio": "Avatar possui confiabilidade adequada. Recomendado validar com mais dados.",
            "Baixo": "Avatar possui baixa confiabilidade. Colete mais dados antes de usar estratégias críticas."
        }
        return recomendacoes.get(nivel, "Nível de confiança desconhecido")

# Instância global
avatar_arqueologico_analyzer = AvatarArqueologicoAnalyzer()
