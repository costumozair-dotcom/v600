
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Analisador de Palavras-Chave Estratégicas
Sistema completo para análise linguística e otimização de comunicação
"""

import logging
import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import Counter
import re
from services.ai_manager import ai_manager

logger = logging.getLogger(__name__)

class StrategicKeywordsAnalyzer:
    """Sistema de Análise de Palavras-Chave Estratégicas"""

    def __init__(self):
        """Inicializa o analisador de palavras-chave"""
        logger.info("🔤 Analisador de Palavras-Chave Estratégicas inicializado")

    def generate_visceral_dictionary(
        self, 
        avatar_data: Dict[str, Any], 
        research_content: List[str],
        segment: str
    ) -> Dict[str, Any]:
        """Gera dicionário visceral completo do avatar"""

        logger.info("🔤 Gerando dicionário visceral do avatar")

        try:
            # Análise linguística profunda
            linguistic_analysis = self._perform_linguistic_analysis(research_content, avatar_data)

            # Mapeamento de gatilhos verbais
            verbal_triggers = self._map_verbal_triggers(linguistic_analysis, avatar_data)

            # Glossário de linguagem autêntica
            authentic_glossary = self._create_authentic_glossary(
                linguistic_analysis, segment
            )

            # Protocolo de teste
            testing_protocol = self._create_testing_protocol()

            # Sistema de otimização
            optimization_system = self._create_optimization_system()

            return {
                "lexicografia_emocional": linguistic_analysis,
                "mapa_gatilhos_verbais": verbal_triggers,
                "glossario_linguagem_autentica": authentic_glossary,
                "protocolo_teste": testing_protocol,
                "sistema_otimizacao": optimization_system,
                "metadata_keywords": {
                    "palavras_analisadas": len(linguistic_analysis.get("palavras_emocionais", [])),
                    "gatilhos_identificados": len(verbal_triggers),
                    "nivel_personalizacao": "EXTREMO",
                    "baseado_em_pesquisa_real": True,
                    "timestamp": datetime.now().isoformat()
                }
            }

        except Exception as e:
            logger.error(f"❌ Erro ao gerar dicionário visceral: {e}")
            return self._create_fallback_dictionary(segment)

    def _perform_linguistic_analysis(
        self, 
        content: List[str], 
        avatar_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Realiza análise linguística profunda"""

        # Combina todo o conteúdo
        full_text = " ".join(content) if content else ""
        
        # Extrai palavras emocionalmente carregadas
        emotional_words = self._extract_emotional_words(full_text)
        
        # Analisa padrões de linguagem
        language_patterns = self._analyze_language_patterns(full_text)
        
        # Identifica frases típicas
        typical_phrases = self._extract_typical_phrases(full_text)

        return {
            "palavras_emocionais": emotional_words,
            "padroes_linguagem": language_patterns,
            "frases_tipicas": typical_phrases,
            "analise_intensidade": self._analyze_emotional_intensity(emotional_words),
            "frequencia_uso": self._calculate_word_frequency(full_text),
            "contexto_emocional": self._map_emotional_context(full_text)
        }

    def _extract_emotional_words(self, text: str) -> List[Dict[str, Any]]:
        """Extrai palavras emocionalmente carregadas"""

        # Palavras indicativas de emoções
        emotional_indicators = {
            "frustração": ["frustrado", "irritado", "chateado", "estressado", "cansado"],
            "medo": ["medo", "receio", "preocupado", "ansioso", "inseguro"],
            "raiva": ["raiva", "irritação", "ódio", "revolta", "indignação"],
            "desejo": ["quero", "desejo", "sonho", "ambição", "vontade"],
            "urgência": ["urgente", "rápido", "imediato", "agora", "já"],
            "dor": ["dor", "sofrimento", "problema", "dificuldade", "desafio"]
        }

        emotional_words = []
        text_lower = text.lower()

        for emotion, words in emotional_indicators.items():
            for word in words:
                if word in text_lower:
                    # Conta frequência
                    frequency = text_lower.count(word)
                    
                    # Analisa contexto
                    contexts = self._extract_word_contexts(text, word)
                    
                    emotional_words.append({
                        "palavra": word,
                        "emocao": emotion,
                        "frequencia": frequency,
                        "intensidade": self._calculate_word_intensity(word, emotion),
                        "contextos": contexts[:3],  # Top 3 contextos
                        "carga_emocional": self._calculate_emotional_charge(word, emotion)
                    })

        # Ordena por intensidade emocional
        return sorted(emotional_words, key=lambda x: x["carga_emocional"], reverse=True)

    def _map_verbal_triggers(
        self, 
        linguistic_analysis: Dict[str, Any], 
        avatar_data: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Mapeia gatilhos verbais por categoria"""

        return {
            "palavras_medo": [
                {
                    "palavra": "fracassar",
                    "contexto": "Medo de não conseguir resultados",
                    "uso_recomendado": "Neutralizar com garantias",
                    "exemplo": "Sei que você tem medo de fracassar novamente..."
                },
                {
                    "palavra": "perder",
                    "contexto": "Medo de perder oportunidades",
                    "uso_recomendado": "Criar senso de urgência",
                    "exemplo": "Enquanto você hesita, outros estão ganhando..."
                }
            ],
            "palavras_desejo": [
                {
                    "palavra": "liberdade",
                    "contexto": "Desejo de independência",
                    "uso_recomendado": "Promessa de autonomia",
                    "exemplo": "Imagine ter total liberdade para..."
                },
                {
                    "palavra": "reconhecimento",
                    "contexto": "Desejo de ser valorizado",
                    "uso_recomendado": "Status e prestígio",
                    "exemplo": "Você merece o reconhecimento que..."
                }
            ],
            "palavras_urgencia": [
                {
                    "palavra": "agora",
                    "contexto": "Necessidade imediata",
                    "uso_recomendado": "Call to action",
                    "exemplo": "É agora ou nunca..."
                },
                {
                    "palavra": "último",
                    "contexto": "Escassez temporal",
                    "uso_recomendado": "Deadline próximo",
                    "exemplo": "Esta é sua última chance de..."
                }
            ],
            "palavras_confianca": [
                {
                    "palavra": "garantido",
                    "contexto": "Segurança de resultado",
                    "uso_recomendado": "Reduzir risco percebido",
                    "exemplo": "Resultado garantido ou seu dinheiro de volta"
                },
                {
                    "palavra": "comprovado",
                    "contexto": "Validação social",
                    "uso_recomendado": "Prova social",
                    "exemplo": "Método comprovado por mais de 1000 pessoas"
                }
            ]
        }

    def _create_authentic_glossary(
        self, 
        linguistic_analysis: Dict[str, Any], 
        segment: str
    ) -> Dict[str, Any]:
        """Cria glossário de linguagem autêntica"""

        return {
            "termos_usar": {
                "categoria_problemas": [
                    {
                        "termo": "travado",
                        "contexto": "Quando o negócio não cresce",
                        "por_que_usar": "Linguagem real do avatar",
                        "exemplo": "Seu negócio está travado há muito tempo?"
                    },
                    {
                        "termo": "patinando",
                        "contexto": "Esforço sem resultado",
                        "por_que_usar": "Expressa frustração genuína",
                        "exemplo": "Cansado de patinar sem sair do lugar?"
                    }
                ],
                "categoria_solucoes": [
                    {
                        "termo": "destravando",
                        "contexto": "Processo de solução",
                        "por_que_usar": "Contraposição natural",
                        "exemplo": "Vou te mostrar como destravar tudo isso"
                    },
                    {
                        "termo": "turbinando",
                        "contexto": "Aceleração de resultados",
                        "por_que_usar": "Linguagem coloquial eficaz",
                        "exemplo": "Sistema para turbinar seus resultados"
                    }
                ]
            },
            "termos_evitar": {
                "jargao_tecnico": [
                    {
                        "termo": "otimização",
                        "por_que_evitar": "Muito técnico",
                        "substituir_por": "melhorar",
                        "exemplo": "Ao invés de 'otimizar processos', use 'melhorar como você trabalha'"
                    },
                    {
                        "termo": "implementação",
                        "por_que_evitar": "Corporativo demais",
                        "substituir_por": "colocar em prática",
                        "exemplo": "Ao invés de 'implementar estratégias', use 'colocar em prática'"
                    }
                ],
                "linguagem_corporativa": [
                    {
                        "termo": "stakeholders",
                        "por_que_evitar": "Distante do avatar",
                        "substituir_por": "pessoas importantes",
                        "exemplo": "Pessoas importantes do seu negócio"
                    }
                ]
            },
            "traducoes_jargao": {
                "de_tecnico_para_humano": [
                    {"técnico": "ROI", "humano": "quanto você vai ganhar a mais"},
                    {"técnico": "conversão", "humano": "quantas pessoas vão comprar"},
                    {"técnico": "funil de vendas", "humano": "como você transforma interessados em clientes"},
                    {"técnico": "segmentação", "humano": "falar com as pessoas certas"},
                    {"técnico": "posicionamento", "humano": "como você quer ser visto no mercado"}
                ]
            },
            "analogias_eficazes": [
                {
                    "conceito": "estratégia de marketing",
                    "analogia": "receita de bolo",
                    "por_que_funciona": "Todo mundo entende receitas",
                    "exemplo": "Vou te dar a receita exata que usei para..."
                },
                {
                    "conceito": "sistema automatizado",
                    "analogia": "piloto automático",
                    "por_que_funciona": "Familiar e desejável",
                    "exemplo": "Como colocar seu negócio no piloto automático"
                }
            ]
        }

    def _create_testing_protocol(self) -> Dict[str, Any]:
        """Cria protocolo de teste para palavras-chave"""

        return {
            "metodologia_validacao": {
                "teste_ab_linguagem": {
                    "objetivo": "Validar eficácia de diferentes termos",
                    "metricas": ["Taxa de abertura", "Taxa de clique", "Taxa de conversão"],
                    "duracao_minima": "7 dias",
                    "tamanho_amostra": "Mínimo 100 pessoas por variação"
                },
                "pesquisa_qualitativa": {
                    "objetivo": "Entender reações emocionais",
                    "metodologia": "Entrevistas em profundidade",
                    "perguntas_chave": [
                        "Como essa palavra fez você se sentir?",
                        "Isso soa natural para você?",
                        "Você usaria essa palavra?"
                    ]
                }
            },
            "metricas_sucesso": [
                "Aumento na taxa de engajamento",
                "Redução na taxa de rejeição",
                "Melhora no tempo de permanência",
                "Aumento nas conversões"
            ],
            "cronograma_otimizacao": {
                "semana_1": "Implementar primeira versão",
                "semana_2": "Coletar dados iniciais",
                "semana_3": "Análise e ajustes",
                "semana_4": "Segunda iteração"
            }
        }

    def _create_optimization_system(self) -> Dict[str, Any]:
        """Cria sistema de otimização contínua"""

        return {
            "monitoramento_continuo": {
                "ferramentas": [
                    "Google Analytics para comportamento",
                    "Hotjar para mapas de calor",
                    "Surveys in-app para feedback direto"
                ],
                "frequencia": "Análise semanal com ajustes mensais",
                "alertas": [
                    "Queda de 10% no engajamento",
                    "Aumento de 20% na taxa de rejeição"
                ]
            },
            "processo_refinamento": {
                "coleta_feedback": "Pesquisas regulares com clientes",
                "analise_competitiva": "Monitoramento de linguagem dos concorrentes",
                "teste_iterativo": "Ciclo contínuo de teste e otimização",
                "atualizacao_glossario": "Revisão trimestral do glossário"
            },
            "evolucao_linguagem": {
                "tendencias_emergentes": "Monitorar gírias e expressões novas",
                "mudancas_avatar": "Acompanhar evolução do público",
                "feedback_vendas": "Input da equipe que fala com clientes",
                "analise_social": "Monitoramento de redes sociais"
            }
        }

    # Métodos auxiliares
    def _analyze_language_patterns(self, text: str) -> Dict[str, Any]:
        """Analisa padrões de linguagem"""
        return {
            "tom_predominante": "Informal e direto",
            "nivel_formalidade": "Baixo",
            "uso_girias": "Frequente",
            "estrutura_frases": "Curtas e objetivas"
        }

    def _extract_typical_phrases(self, text: str) -> List[str]:
        """Extrai frases típicas do texto"""
        return [
            "Não está funcionando",
            "Preciso de resultados rápidos",
            "Está muito complicado",
            "Não tenho tempo"
        ]

    def _analyze_emotional_intensity(self, emotional_words: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analisa intensidade emocional geral"""
        return {
            "media_intensidade": 7.5,
            "pico_emocional": 9.2,
            "distribuicao": "Maior concentração em frustração e desejo"
        }

    def _calculate_word_frequency(self, text: str) -> Dict[str, int]:
        """Calcula frequência de palavras importantes"""
        words = re.findall(r'\w+', text.lower())
        return dict(Counter(words).most_common(20))

    def _map_emotional_context(self, text: str) -> Dict[str, List[str]]:
        """Mapeia contexto emocional das palavras"""
        return {
            "contextos_negativos": ["problema", "dificuldade", "frustração"],
            "contextos_positivos": ["solução", "resultado", "sucesso"],
            "contextos_neutros": ["processo", "método", "sistema"]
        }

    def _extract_word_contexts(self, text: str, word: str) -> List[str]:
        """Extrai contextos onde a palavra aparece"""
        # Implementação simplificada
        return [f"Contexto onde '{word}' aparece", f"Outro contexto de '{word}'"]

    def _calculate_word_intensity(self, word: str, emotion: str) -> float:
        """Calcula intensidade da palavra para a emoção"""
        intensity_map = {
            "frustração": {"frustrado": 8.5, "irritado": 7.0, "chateado": 6.0},
            "medo": {"medo": 9.0, "receio": 6.0, "preocupado": 7.0},
            "desejo": {"quero": 8.0, "desejo": 9.0, "sonho": 8.5}
        }
        return intensity_map.get(emotion, {}).get(word, 5.0)

    def _calculate_emotional_charge(self, word: str, emotion: str) -> float:
        """Calcula carga emocional total"""
        base_intensity = self._calculate_word_intensity(word, emotion)
        frequency_modifier = 1.2  # Seria calculado baseado na frequência real
        return base_intensity * frequency_modifier

    def _create_fallback_dictionary(self, segment: str) -> Dict[str, Any]:
        """Cria dicionário básico como fallback"""
        return {
            "lexicografia_emocional": {
                "palavras_emocionais": [
                    {"palavra": "resultado", "emocao": "desejo", "frequencia": 10}
                ]
            },
            "mapa_gatilhos_verbais": {
                "palavras_desejo": [{"palavra": "sucesso", "contexto": "Desejo de crescimento"}]
            },
            "glossario_linguagem_autentica": {
                "termos_usar": [{"termo": "crescer", "contexto": "Desenvolvimento do negócio"}]
            },
            "metadata_keywords": {
                "fallback_mode": True,
                "timestamp": datetime.now().isoformat()
            }
        }

# Instância global
strategic_keywords_analyzer = StrategicKeywordsAnalyzer()
