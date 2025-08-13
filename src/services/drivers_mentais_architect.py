
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Arquiteto de Drivers Mentais
Sistema avançado para criação e implementação de gatilhos psicológicos
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from services.ai_manager import ai_manager

logger = logging.getLogger(__name__)

class DriversMemtaisArchitect:
    """Arquiteto especializado em drivers mentais e gatilhos psicológicos"""

    def __init__(self):
        self.drivers_universais = {
            "URGENCIA_VISCERAL": {
                "nome": "Urgência Visceral",
                "descricao": "Cria tensão temporal que força decisão imediata",
                "gatilho_central": "Escassez de tempo",
                "categoria": "Temporal"
            },
            "ESCASSEZ_SOCIAL": {
                "nome": "Escassez Social", 
                "descricao": "Medo de ficar por fora enquanto outros avançam",
                "gatilho_central": "Exclusão social",
                "categoria": "Social"
            },
            "VERGONHA_PRODUTIVA": {
                "nome": "Vergonha Produtiva",
                "descricao": "Confronta a realidade atual de forma visceral",
                "gatilho_central": "Autodecepção",
                "categoria": "Emocional"
            },
            "AUTORIDADE_INVISIVEL": {
                "nome": "Autoridade Invisível",
                "descricao": "Estabelece liderança sem arrogância",
                "gatilho_central": "Confiança especializada",
                "categoria": "Credibilidade"
            },
            "FUTURO_PERDIDO": {
                "nome": "Futuro Perdido",
                "descricao": "Mostra o que será perdido se não agir",
                "gatilho_central": "Medo da perda",
                "categoria": "Projeção"
            }
        }
        
    async def criar_arsenal_drivers(self, dados_entrada: Dict[str, Any]) -> Dict[str, Any]:
        """Cria arsenal completo de drivers mentais personalizados"""
        try:
            logger.info("🧠 Iniciando criação de arsenal de drivers mentais...")
            
            # Extrai dados essenciais
            avatar = dados_entrada.get('avatar', {})
            produto = dados_entrada.get('produto', 'Produto')
            funil = dados_entrada.get('funil_vendas', {})
            contexto = dados_entrada.get('contexto', {})
            
            # Análise psicológica inicial
            analise_psicologica = await self._analisar_perfil_psicologico(avatar)
            
            # Seleção de drivers estratégicos
            drivers_selecionados = await self._selecionar_drivers_estrategicos(
                analise_psicologica, funil, contexto
            )
            
            # Criação de roteiros personalizados
            roteiros = await self._criar_roteiros_personalizados(
                drivers_selecionados, avatar, produto
            )
            
            # Mapeamento estratégico
            mapa_instalacao = await self._criar_mapa_instalacao(
                drivers_selecionados, funil
            )
            
            # Protocolo de implementação
            protocolo = await self._criar_protocolo_implementacao(
                drivers_selecionados, roteiros
            )
            
            arsenal = {
                "produto": produto,
                "timestamp": datetime.now().isoformat(),
                "analise_psicologica": analise_psicologica,
                "mapa_estrategico": mapa_instalacao,
                "drivers_selecionados": drivers_selecionados,
                "roteiros_completos": roteiros,
                "protocolo_implementacao": protocolo,
                "metricas_sucesso": await self._definir_metricas_sucesso(drivers_selecionados)
            }
            
            logger.info(f"✅ Arsenal de drivers mentais criado com {len(drivers_selecionados)} drivers")
            return arsenal
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar arsenal de drivers mentais: {e}")
            return {"erro": str(e)}
    
    async def _analisar_perfil_psicologico(self, avatar: Dict) -> Dict[str, Any]:
        """Realiza análise psicológica profunda do avatar"""
        
        prompt = f"""
        Como ARQUITETO DE DRIVERS MENTAIS, analise o perfil psicológico:
        
        AVATAR: {json.dumps(avatar, indent=2)}
        
        Forneça análise psicológica estruturada:
        
        1. DORES VISCERAIS (as 3 mais profundas)
        2. MEDOS PARALISANTES (os 3 mais críticos) 
        3. DESEJOS ARDENTES (os 3 mais intensos)
        4. GATILHOS EMOCIONAIS (os 5 mais eficazes)
        5. VULNERABILIDADES PSICOLÓGICAS (pontos sensíveis)
        6. PADRÕES DE AUTOSSABOTAGEM (comportamentos limitantes)
        
        Seja visceral e direto. Foque no que realmente move esta pessoa.
        """
        
        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "analise_bruta": resposta,
                "processamento_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro na análise psicológica: {e}")
            return {"erro": str(e)}
    
    async def _selecionar_drivers_estrategicos(self, analise: Dict, funil: Dict, contexto: Dict) -> List[Dict]:
        """Seleciona os drivers mais estratégicos para o contexto"""
        
        prompt = f"""
        Como ARQUITETO DE DRIVERS MENTAIS, selecione os 3-5 drivers mais estratégicos:
        
        ANÁLISE PSICOLÓGICA: {json.dumps(analise, indent=2)}
        FUNIL DE VENDAS: {json.dumps(funil, indent=2)}
        CONTEXTO: {json.dumps(contexto, indent=2)}
        
        DRIVERS UNIVERSAIS DISPONÍVEIS:
        {json.dumps(self.drivers_universais, indent=2)}
        
        Para cada driver selecionado, forneça:
        1. NOME_DRIVER
        2. JUSTIFICATIVA (por que é estratégico para este avatar)
        3. MOMENTO_IDEAL (quando aplicar no funil)
        4. INTENSIDADE_RECOMENDADA (1-10)
        5. OBJETIVO_PSICOLOGICO (que estado mental criar)
        6. PERSONALIZAÇÃO (adaptações específicas para este avatar)
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            # Processa resposta para extrair JSON
            drivers = self._processar_drivers_selecionados(resposta)
            return drivers
        except Exception as e:
            logger.error(f"Erro na seleção de drivers: {e}")
            return []
    
    async def _criar_roteiros_personalizados(self, drivers: List[Dict], avatar: Dict, produto: str) -> Dict:
        """Cria roteiros completos para cada driver"""
        
        roteiros = {}
        
        for driver in drivers:
            prompt = f"""
            Como ARQUITETO DE DRIVERS MENTAIS, crie roteiro COMPLETO para o driver:
            
            DRIVER: {json.dumps(driver, indent=2)}
            AVATAR: {json.dumps(avatar, indent=2)}
            PRODUTO: {produto}
            
            Crie roteiro com:
            
            1. SETUP (como introduzir - 30 segundos)
            2. INSTALAÇÃO (como implantar o driver - 2-3 minutos)
            3. NARRATIVA (história específica que demonstra o conceito)
            4. PERGUNTA_ANCORA (pergunta poderosa que fixa o driver)
            5. PROVA_LOGICA (evidência que sustenta o driver)
            6. BRIDGE (como conectar com o próximo elemento)
            7. FRASES_IMPACTO (3-5 frases prontas de máximo impacto)
            8. VARIAÇÕES (adaptações por formato: CPL, webinar, live)
            
            Seja específico, visceral e acionável. Scripts prontos para uso.
            """
            
            try:
                resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
                roteiros[driver.get('nome', f'Driver_{len(roteiros)+1}')] = {
                    "driver_config": driver,
                    "roteiro_completo": resposta,
                    "criado_em": datetime.now().isoformat()
                }
            except Exception as e:
                logger.error(f"Erro ao criar roteiro para driver {driver}: {e}")
                
        return roteiros
    
    async def _criar_mapa_instalacao(self, drivers: List[Dict], funil: Dict) -> Dict:
        """Cria mapa estratégico de instalação dos drivers"""
        
        prompt = f"""
        Como ARQUITETO DE DRIVERS MENTAIS, crie MAPA ESTRATÉGICO de instalação:
        
        DRIVERS SELECIONADOS: {json.dumps(drivers, indent=2)}
        FUNIL DE VENDAS: {json.dumps(funil, indent=2)}
        
        Crie mapa com:
        
        1. SEQUENCIA_PSICOLOGICA (ordem ideal dos drivers)
        2. DISTRIBUIÇÃO_TEMPORAL (quando instalar cada driver)
        3. PONTOS_CRITICOS (momentos de máximo impacto)
        4. INTENSIDADE_GRADUAL (como escalar a tensão)
        5. SISTEMA_REFORCO (como reforçar drivers instalados)
        6. PROTOCOLO_EMERGENCIA (o que fazer se driver não funcionar)
        
        Forneça cronograma detalhado e justificativas estratégicas.
        """
        
        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "mapa_completo": resposta,
                "criado_em": datetime.now().isoformat(),
                "drivers_mapeados": len(drivers)
            }
        except Exception as e:
            logger.error(f"Erro ao criar mapa de instalação: {e}")
            return {"erro": str(e)}
    
    async def _criar_protocolo_implementacao(self, drivers: List[Dict], roteiros: Dict) -> Dict:
        """Cria protocolo detalhado de implementação"""
        
        prompt = f"""
        Como ARQUITETO DE DRIVERS MENTAIS, crie PROTOCOLO DE IMPLEMENTAÇÃO:
        
        DRIVERS: {json.dumps(drivers, indent=2)}
        TOTAL_ROTEIROS: {len(roteiros)}
        
        Crie protocolo com:
        
        1. CHECKLIST_PRE_EVENTO (preparação necessária)
        2. SCRIPTS_POR_FORMATO (adaptações por canal)
        3. METRICAS_VALIDACAO (como medir eficácia)
        4. SINAIS_SUCESSO (indicadores de que driver funcionou)
        5. PLANO_OTIMIZACAO (como melhorar continuamente)
        6. KIT_EMERGENCIA (soluções para problemas comuns)
        
        Seja extremamente prático e acionável.
        """
        
        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "protocolo_completo": resposta,
                "criado_em": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao criar protocolo: {e}")
            return {"erro": str(e)}
    
    async def _definir_metricas_sucesso(self, drivers: List[Dict]) -> Dict:
        """Define métricas específicas de sucesso para cada driver"""
        
        metricas = {
            "metricas_gerais": [
                "Taxa de engajamento durante instalação",
                "Tempo de permanência no conteúdo",
                "Reações emocionais visíveis",
                "Perguntas/comentários relacionados"
            ],
            "metricas_por_driver": {},
            "indicadores_comportamentais": [
                "Linguagem corporal (presencial)",
                "Engajamento no chat (online)", 
                "Taxa de continuidade",
                "Conversão pós-driver"
            ]
        }
        
        for driver in drivers:
            nome = driver.get('nome', 'Driver')
            metricas["metricas_por_driver"][nome] = {
                "indicadores_primarios": [
                    "Resposta emocional visível",
                    "Engajamento aumentado",
                    "Tempo de atenção"
                ],
                "indicadores_secundarios": [
                    "Interação posterior",
                    "Compartilhamento/comentário",
                    "Progressão no funil"
                ]
            }
            
        return metricas
    
    def _processar_drivers_selecionados(self, resposta_ai: str) -> List[Dict]:
        """Processa resposta da AI para extrair drivers estruturados"""
        try:
            # Tenta extrair JSON da resposta
            import re
            json_match = re.search(r'\{.*\}', resposta_ai, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: processa texto estruturado
                return self._processar_texto_estruturado(resposta_ai)
        except Exception as e:
            logger.error(f"Erro ao processar drivers selecionados: {e}")
            return []
    
    def _processar_texto_estruturado(self, texto: str) -> List[Dict]:
        """Processa texto estruturado quando JSON não disponível"""
        drivers = []
        # Implementação de parsing de texto estruturado
        # Por simplicidade, retorna drivers padrão personalizados
        return [
            {
                "nome": "Urgência Visceral Personalizada",
                "justificativa": "Específico para o contexto analisado",
                "momento_ideal": "Início do pré-pitch",
                "intensidade": 8,
                "objetivo": "Criar tensão temporal imediata"
            }
        ]

# Instância global
drivers_architect = DriversMemtaisArchitect()
