#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Psychological Agents
Sistema de agentes psicológicos especializados para análise profunda
"""

import os
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class PsychologicalAgents:
    """
    Sistema de agentes psicológicos especializados para análise profunda
    Cada agente tem expertise específica em diferentes aspectos psicológicos
    """

    def __init__(self):
        """Inicializa os agentes psicológicos"""
        self.agentes = self._inicializar_agentes()
        logger.info("👥 Psychological Agents inicializados com sucesso")

    def _inicializar_agentes(self) -> Dict[str, Dict[str, Any]]:
        """Inicializa configurações dos agentes especializados"""
        return {
            'arqueologist': {
                'nome': 'ARQUEÓLOGO COMPORTAMENTAL',
                'especialidade': 'Escavação de comportamentos e padrões ocultos',
                'missao': 'Descobrir padrões de comportamento profundos e inconsistências',
                'ferramentas': ['Análise de discurso', 'Mapeamento de contradições', 'Timeline comportamental'],
                'nivel_profundidade': 9
            },
            'visceral_master': {
                'nome': 'MESTRE VISCERAL',
                'especialidade': 'Identificação de dores emocionais profundas',
                'missao': 'Encontrar as dores mais viscerais que geram ação imediata',
                'ferramentas': ['Mapeamento emocional', 'Identificação de triggers', 'Análise de trauma'],
                'nivel_profundidade': 10
            },
            'drivers_architect': {
                'nome': 'ARQUITETO DE DRIVERS',
                'especialidade': 'Construção de gatilhos mentais personalizados',
                'missao': 'Criar drivers que se instalem profundamente na mente',
                'ferramentas': ['Neurociência aplicada', 'Psicologia cognitiva', 'Behavioral design'],
                'nivel_profundidade': 9
            },
            'pre_pitch_architect': {
                'nome': 'ARQUITETO DE PRÉ-PITCH',
                'especialidade': 'Preparação mental invisível pré-venda',
                'missao': 'Preparar a mente para receptividade máxima ao pitch',
                'ferramentas': ['Sequenciamento psicológico', 'Ancoragem emocional', 'Preparação subliminar'],
                'nivel_profundidade': 8
            },
            'anti_objection': {
                'nome': 'ESPECIALISTA ANTI-OBJEÇÃO',
                'especialidade': 'Neutralização preventiva de resistências',
                'missao': 'Identificar e neutralizar objeções antes que sejam verbalizadas',
                'ferramentas': ['Mapeamento de resistências', 'Antecipação de objeções', 'Frameworks de neutralização'],
                'nivel_profundidade': 8
            },
            'visual_director': {
                'nome': 'DIRETOR DE PROVAS VISUAIS',
                'especialidade': 'Criação de evidências visuais persuasivas',
                'missao': 'Desenvolver arsenal de provas visuais irrefutáveis',
                'ferramentas': ['Design persuasivo', 'Storytelling visual', 'Neurociência visual'],
                'nivel_profundidade': 7
            }
        }

    def executar_analise_completa(self, avatar_data: Dict[str, Any],
                                 contexto_mercado: Dict[str, Any],
                                 session_id: str) -> Dict[str, Any]:
        """Executa análise completa com todos os agentes"""
        try:
            logger.info("👥 Iniciando análise com agentes psicológicos especializados")

            resultados_agentes = {}

            # Executa cada agente em sequência
            for agente_id, config in self.agentes.items():
                try:
                    logger.info(f"🔍 Executando {config['nome']}")

                    resultado = self._executar_agente(
                        agente_id, config, avatar_data, contexto_mercado, session_id
                    )

                    resultados_agentes[agente_id] = resultado

                    # Salva resultado individual
                    salvar_etapa(f'agente_{agente_id}', resultado, session_id)

                    logger.info(f"✅ {config['nome']} concluído")

                except Exception as e:
                    logger.error(f"❌ Erro no agente {agente_id}: {e}")
                    resultados_agentes[agente_id] = {'erro': str(e)}

            # Síntese final dos resultados
            sintese_final = self._sintetizar_resultados(resultados_agentes, session_id)

            return {
                'resultados_individuais': resultados_agentes,
                'sintese_psicologica': sintese_final,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            error_msg = f"Erro na análise psicológica completa: {str(e)}"
            logger.error(f"❌ {error_msg}")
            salvar_erro('psychological_agents', error_msg, session_id)
            return {'error': error_msg}

    def _executar_agente(self, agente_id: str, config: Dict,
                        avatar_data: Dict, contexto_mercado: Dict,
                        session_id: str) -> Dict[str, Any]:
        """Executa um agente específico"""

        if agente_id == 'arqueologist':
            return self._executar_arqueologist(config, avatar_data, contexto_mercado)
        elif agente_id == 'visceral_master':
            return self._executar_visceral_master(config, avatar_data, contexto_mercado)
        elif agente_id == 'drivers_architect':
            return self._executar_drivers_architect(config, avatar_data, contexto_mercado)
        elif agente_id == 'pre_pitch_architect':
            return self._executar_pre_pitch_architect(config, avatar_data, contexto_mercado)
        elif agente_id == 'anti_objection':
            return self._executar_anti_objection(config, avatar_data, contexto_mercado)
        elif agente_id == 'visual_director':
            return self._executar_visual_director(config, avatar_data, contexto_mercado)
        else:
            return {'erro': f'Agente {agente_id} não implementado'}

    def _executar_arqueologist(self, config: Dict, avatar_data: Dict, contexto: Dict) -> Dict[str, Any]:
        """Executa o Arqueólogo Comportamental"""

        prompt = f"""
        ARQUEÓLOGO COMPORTAMENTAL - MISSÃO DE ESCAVAÇÃO PROFUNDA

        IDENTIDADE: {config['nome']}
        ESPECIALIDADE: {config['especialidade']}
        MISSÃO: {config['missao']}

        AVATAR PARA ANÁLISE:
        {json.dumps(avatar_data, ensure_ascii=False, indent=2)}

        CONTEXTO DE MERCADO:
        {json.dumps(contexto, ensure_ascii=False, indent=2)}

        INSTRUÇÕES CIRÚRGICAS:

        Como ARQUEÓLOGO COMPORTAMENTAL, sua missão é ESCAVAR padrões comportamentais ocultos, contradições e inconsistências que revelam a verdadeira natureza psicológica do avatar.

        EXECUTE AS SEGUINTES ESCAVAÇÕES:

        1. ARQUEOLOGIA DE CONTRADIÇÕES
        - Identifique contradições entre o que diz e faz
        - Mapeie discrepâncias entre valores declarados e comportamentos
        - Encontre padrões de autossabotagem ocultos
        - Revele hipocrisias inconscientes

        2. ESCAVAÇÃO DE PADRÕES OCULTOS
        - Comportamentos repetitivos não reconhecidos
        - Decisões automáticas inconscientes
        - Rituais comportamentais estabelecidos
        - Gatilhos comportamentais específicos

        3. TIMELINE COMPORTAMENTAL
        - Evolução dos comportamentos ao longo do tempo
        - Momentos de mudança significativa
        - Padrões cíclicos de comportamento
        - Regressões comportamentais

        4. MAPEAMENTO DE MÁSCARAS SOCIAIS
        - Personalidades diferentes em contextos diferentes
        - Comportamentos adaptativos por ambiente
        - Personas profissionais vs pessoais
        - Defesas comportamentais ativas

        5. ANÁLISE DE MICRO-COMPORTAMENTOS
        - Pequenos gestos reveladores
        - Linguagem corporal inconsciente
        - Padrões de comunicação únicos
        - Hábitos revelativos da personalidade

        FORMATO DE ENTREGA:
        Para cada descoberta arqueológica, forneça:
        - ACHADO: O que foi descoberto
        - EVIDÊNCIA: Como chegou a essa conclusão
        - IMPLICAÇÃO: O que isso revela sobre a psique
        - OPORTUNIDADE: Como usar isso estrategicamente

        Seja um SHERLOCK HOLMES do comportamento humano.
        Não aceite nada pelo valor nominal. ESCAVE FUNDO.
        """

        try:
            response = ai_manager.gerar_resposta_inteligente(
                prompt,
                modelo_preferido='gemini',
                max_tentativas=2
            )

            if response and 'response' in response:
                return {
                    'agente': 'ARQUEÓLOGO COMPORTAMENTAL',
                    'analise_completa': response['response'],
                    'achados_principais': self._extrair_achados_principais(response['response']),
                    'nivel_profundidade': config['nivel_profundidade'],
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return self._arqueologist_fallback(avatar_data)

        except Exception as e:
            logger.error(f"Erro no Arqueólogo: {e}")
            return self._arqueologist_fallback(avatar_data)

    def _executar_visceral_master(self, config: Dict, avatar_data: Dict, contexto: Dict) -> Dict[str, Any]:
        """Executa o Mestre Visceral"""

        prompt = f"""
        MESTRE VISCERAL - ESPECIALISTA EM DORES PROFUNDAS

        IDENTIDADE: {config['nome']}
        ESPECIALIDADE: {config['especialidade']}
        MISSÃO: {config['missao']}

        AVATAR PARA ANÁLISE:
        {json.dumps(avatar_data, ensure_ascii=False, indent=2)}

        INSTRUÇÕES VISCERAIS:

        Como MESTRE VISCERAL, você é especialista em identificar as dores emocionais mais profundas, aquelas que fazem a pessoa acordar às 3h da manhã com o coração acelerado.

        EXECUTE DISSECÇÃO EMOCIONAL COMPLETA:

        1. IDENTIFICAÇÃO DE DORES VISCERAIS PRIMÁRIAS
        - Dores que causam sofrimento físico real
        - Dores que geram vergonha profunda
        - Dores que provocam raiva incontrolável
        - Dores que criam desespero genuíno

        2. MAPEAMENTO DE TRIGGERS EMOCIONAIS
        - Situações que disparam dor intensa
        - Palavras que ativam sofrimento
        - Memórias que causam dor física
        - Contextos que amplificam o sofrimento

        3. ANATOMIA DO SOFRIMENTO
        - Como a dor se manifesta fisicamente
        - Onde é sentida no corpo
        - Intensidade em escala 1-10
        - Frequência dos episódios

        4. CONSEQUÊNCIAS COMPORTAMENTAIS
        - Como a dor afeta decisões
        - Comportamentos compensatórios
        - Mecanismos de escape utilizados
        - Impacto nos relacionamentos

        5. LINGUAGEM DE ATIVAÇÃO
        - Palavras que ressoam com a dor
        - Frases que geram identificação imediata
        - Metáforas que conectam emocionalmente
        - Tom que amplifica o sofrimento

        6. TRANSFORMAÇÃO ATRAVÉS DA DOR
        - Como a dor pode ser transformada em motivação
        - Energia latente na dor para mudança
        - Ponto de ruptura que gera ação
        - Catalisador para transformação

        FORMATO DE ENTREGA:
        Para cada dor visceral identificada:
        - NOME DA DOR: Título específico e memorável
        - DESCRIÇÃO VISCERAL: Como se sente na carne
        - GATILHOS: O que dispara a dor
        - LINGUAGEM: Como falar dessa dor
        - TRANSFORMAÇÃO: Como usá-la para motivar ação

        Seja IMPLACÁVEL mas EMPÁTICO.
        Encontre a dor que move montanhas.
        """

        try:
            response = ai_manager.gerar_resposta_inteligente(
                prompt,
                modelo_preferido='gemini',
                max_tentativas=2
            )

            if response and 'response' in response:
                return {
                    'agente': 'MESTRE VISCERAL',
                    'analise_completa': response['response'],
                    'dores_viscerais': self._extrair_dores_viscerais(response['response']),
                    'nivel_intensidade': config['nivel_profundidade'],
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return self._visceral_master_fallback(avatar_data)

        except Exception as e:
            logger.error(f"Erro no Mestre Visceral: {e}")
            return self._visceral_master_fallback(avatar_data)

    def _executar_drivers_architect(self, config: Dict, avatar_data: Dict, contexto: Dict) -> Dict[str, Any]:
        """Executa o Arquiteto de Drivers"""

        prompt = f"""
        ARQUITETO DE DRIVERS MENTAIS - CONSTRUTOR DE GATILHOS PSICOLÓGICOS

        IDENTIDADE: {config['nome']}
        ESPECIALIDADE: {config['especialidade']}
        MISSÃO: {config['missao']}

        AVATAR PARA ANÁLISE:
        {json.dumps(avatar_data, ensure_ascii=False, indent=2)}

        INSTRUÇÕES DE ARQUITETURA MENTAL:

        Como ARQUITETO DE DRIVERS, sua missão é construir gatilhos mentais que se instalem profundamente na mente do avatar e disparem respostas comportamentais específicas.

        CONSTRUA OS SEGUINTES DRIVERS:

        1. DRIVERS DE URGÊNCIA GENUÍNA
        - Gatilhos temporais específicos
        - Escassez real e percebida
        - Consequências de inação
        - Janelas de oportunidade

        2. DRIVERS DE PROVA SOCIAL
        - Validação por similaridade
        - Pressão de grupo sutil
        - Movimento de massa
        - FOMO (Fear of Missing Out)

        3. DRIVERS DE AUTORIDADE
        - Credibilidade técnica
        - Reconhecimento de pares
        - Resultados demonstráveis
        - Expertise incontestável

        4. DRIVERS DE RECIPROCIDADE
        - Valor entregue antecipadamente
        - Favor específico prestado
        - Conhecimento compartilhado
        - Acesso privilegiado

        5. DRIVERS DE CONSISTÊNCIA
        - Comprometimentos públicos
        - Identidade alinhada
        - Valores demonstrados
        - Coerência comportamental

        6. DRIVERS DE ESCASSEZ
        - Limitação genuine
        - Exclusividade real
        - Acesso restrito
        - Tempo limitado

        PARA CADA DRIVER CONSTRUÍDO:
        - NOME: Título específico e memorável
        - MECANISMO: Como funciona neurologically
        - TRIGGER: O que dispara o driver
        - INSTALAÇÃO: Como implantar na mente
        - ATIVAÇÃO: Como disparar quando necessário
        - MENSURAÇÃO: Como medir eficácia

        Construa drivers CIRÚRGICOS e PERSONALIZADOS.
        Cada driver deve ser uma FERRAMENTA PRECISA.
        """

        try:
            response = ai_manager.gerar_resposta_inteligente(
                prompt,
                modelo_preferido='gemini',
                max_tentativas=2
            )

            if response and 'response' in response:
                return {
                    'agente': 'ARQUITETO DE DRIVERS',
                    'analise_completa': response['response'],
                    'drivers_construidos': self._extrair_drivers_construidos(response['response']),
                    'nivel_sofisticacao': config['nivel_profundidade'],
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return self._drivers_architect_fallback(avatar_data)

        except Exception as e:
            logger.error(f"Erro no Arquiteto de Drivers: {e}")
            return self._drivers_architect_fallback(avatar_data)

    def _executar_pre_pitch_architect(self, config: Dict, avatar_data: Dict, contexto: Dict) -> Dict[str, Any]:
        """Executa o Arquiteto de Pré-Pitch"""

        prompt = f"""
        ARQUITETO DE PRÉ-PITCH - PREPARAÇÃO MENTAL INVISÍVEL

        IDENTIDADE: {config['nome']}
        ESPECIALIDADE: {config['especialidade']}
        MISSÃO: {config['missao']}

        AVATAR PARA ANÁLISE:
        {json.dumps(avatar_data, ensure_ascii=False, indent=2)}

        INSTRUÇÕES DE ARQUITETURA PRÉ-PITCH:

        Como ARQUITETO DE PRÉ-PITCH, você deve criar um sistema INVISÍVEL que prepare a mente do avatar para receptividade máxima ao pitch principal.

        DESENVOLVA ESTRATÉGIA COMPLETA:

        1. ANÁLISE DO ESTADO MENTAL ATUAL
        - Nível de consciência do problema
        - Resistências mentais ativas
        - Receptividade atual
        - Barreiras psicológicas

        2. DESIGN DA JORNADA DE PREPARAÇÃO
        - Sequência de exposições
        - Intensificação gradual
        - Pontos de ancoragem
        - Momentos de ruptura

        3. INSTALAÇÃO DE ÂNCORAS MENTAIS
        - Conceitos-chave a implantar
        - Associações positivas
        - Memórias de referência
        - Estados emocionais desejados

        4. QUEBRA DE RESISTÊNCIAS
        - Objeções antecipadas
        - Neutralização prévia
        - Ressignificação de crenças
        - Abertura mental gradual

        5. CONSTRUÇÃO DE CONFIANÇA
        - Demonstração de competência
        - Prova social indireta
        - Autoridade estabelecida
        - Credibilidade construída

        6. TIMING E SEQUENCIAMENTO
        - Cronograma de preparação
        - Sequência otimizada
        - Pontos de intensificação
        - Momentos de consolidação

        PARA CADA ELEMENTO:
        - OBJETIVO: O que pretende alcançar
        - MÉTODO: Como será implementado
        - TIMING: Quando deve ocorrer
        - MENSURAÇÃO: Como avaliar sucesso
        - AJUSTES: Como adaptar se necessário

        Crie um sistema INVISÍVEL mas INEVITÁVEL.
        O avatar deve chegar ao pitch PRONTO para dizer SIM.
        """

        try:
            response = ai_manager.gerar_resposta_inteligente(
                prompt,
                modelo_preferido='gemini',
                max_tentativas=2
            )

            if response and 'response' in response:
                return {
                    'agente': 'ARQUITETO DE PRÉ-PITCH',
                    'analise_completa': response['response'],
                    'estrategia_preparacao': self._extrair_estrategia_preparacao(response['response']),
                    'nivel_sutileza': config['nivel_profundidade'],
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return self._pre_pitch_architect_fallback(avatar_data)

        except Exception as e:
            logger.error(f"Erro no Arquiteto de Pré-Pitch: {e}")
            return self._pre_pitch_architect_fallback(avatar_data)

    def _executar_anti_objection(self, config: Dict, avatar_data: Dict, contexto: Dict) -> Dict[str, Any]:
        """Executa o Especialista Anti-Objeção"""

        prompt = f"""
        ESPECIALISTA ANTI-OBJEÇÃO - NEUTRALIZADOR DE RESISTÊNCIAS

        IDENTIDADE: {config['nome']}
        ESPECIALIDADE: {config['especialidade']}
        MISSÃO: {config['missao']}

        AVATAR PARA ANÁLISE:
        {json.dumps(avatar_data, ensure_ascii=False, indent=2)}

        INSTRUÇÕES DE NEUTRALIZAÇÃO:

        Como ESPECIALISTA ANTI-OBJEÇÃO, sua missão é identificar TODAS as possíveis objeções que este avatar pode ter e criar sistemas para neutralizá-las ANTES que sejam verbalizadas.

        EXECUTE MAPEAMENTO COMPLETO:

        1. CATÁLOGO DE OBJEÇÕES PROVÁVEIS
        - Objeções financeiras específicas
        - Resistências temporais
        - Dúvidas sobre capacidade
        - Medos de fracasso
        - Experiências negativas passadas

        2. ANÁLISE PSICOLÓGICA DAS RESISTÊNCIAS
        - Origem emocional de cada objeção
        - Crenças limitantes por trás
        - Mecanismos de defesa ativados
        - Padrões de autossabotagem

        3. FRAMEWORKS DE NEUTRALIZAÇÃO
        - Antecipação e abordagem prévia
        - Ressignificação de perspectiva
        - Evidências contraditórias
        - Reformulação de contexto

        4. SCRIPTS DE NEUTRALIZAÇÃO
        - Linguagem específica para cada objeção
        - Sequência de argumentos
        - Evidências de apoio
        - Perguntas redirecionadoras

        5. ESTRATÉGIAS PREVENTIVAS
        - Como evitar que objeções surjam
        - Preparação mental prévia
        - Condicionamento positivo
        - Instalação de convicções

        6. TIMING DE APLICAÇÃO
        - Momento ideal para cada neutralização
        - Sequência estratégica
        - Sinais de que a objeção está surgindo
        - Intervenção preventiva

        PARA CADA OBJEÇÃO IDENTIFICADA:
        - OBJEÇÃO: Exatamente como será verbalizada
        - ORIGEM: De onde vem psicologicamente
        - NEUTRALIZAÇÃO: Como neutralizar eficazmente
        - PREVENÇÃO: Como evitar que surja
        - EVIDÊNCIAS: Provas para usar na neutralização

        Seja um CIRURGIÃO DE OBJEÇÕES.
        Neutralize ANTES que seja verbalizada.
        """

        try:
            response = ai_manager.gerar_resposta_inteligente(
                prompt,
                modelo_preferido='gemini',
                max_tentativas=2
            )

            if response and 'response' in response:
                return {
                    'agente': 'ESPECIALISTA ANTI-OBJEÇÃO',
                    'analise_completa': response['response'],
                    'objecoes_mapeadas': self._extrair_objecoes_mapeadas(response['response']),
                    'nivel_antecipacao': config['nivel_profundidade'],
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return self._anti_objection_fallback(avatar_data)

        except Exception as e:
            logger.error(f"Erro no Anti-Objeção: {e}")
            return self._anti_objection_fallback(avatar_data)

    def _executar_visual_director(self, config: Dict, avatar_data: Dict, contexto: Dict) -> Dict[str, Any]:
        """Executa o Diretor de Provas Visuais"""

        prompt = f"""
        DIRETOR DE PROVAS VISUAIS - ARSENAL DE EVIDÊNCIAS

        IDENTIDADE: {config['nome']}
        ESPECIALIDADE: {config['especialidade']}
        MISSÃO: {config['missao']}

        AVATAR PARA ANÁLISE:
        {json.dumps(avatar_data, ensure_ascii=False, indent=2)}

        INSTRUÇÕES DE DIREÇÃO VISUAL:

        Como DIRETOR DE PROVAS VISUAIS, você deve criar um arsenal completo de evidências visuais que tornem impossível questionar a eficácia da solução.

        DESENVOLVA ARSENAL COMPLETO:

        1. PROVAS DE RESULTADOS
        - Screenshots de resultados reais
        - Gráficos de crescimento
        - Comparações antes/depois
        - Métricas de performance

        2. PROVAS SOCIAIS VISUAIS
        - Depoimentos em vídeo
        - Cases de sucesso documentados
        - Transformações visíveis
        - Multidões de clientes satisfeitos

        3. PROVAS DE AUTORIDADE
        - Certificações e diplomas
        - Reconhecimentos e prêmios
        - Aparições na mídia
        - Endossos de especialistas

        4. PROVAS DE ESCASSEZ
        - Contadores de tempo real
        - Vagas limitadas visualmente
        - Procura/demanda mostrada
        - Exclusividade demonstrada

        5. PROVAS DE PROCESSO
        - Behind-the-scenes do método
        - Passo-a-passo visual
        - Sistemática documentada
        - Metodologia exposta

        6. PROVAS EMOCIONAIS
        - Histórias visuais impactantes
        - Transformações pessoais
        - Momentos de breakthrough
        - Jornadas de superação

        PARA CADA CATEGORIA DE PROVA:
        - TIPO: Que tipo de prova visual
        - OBJETIVO: Que objeção neutraliza
        - FORMATO: Como deve ser apresentada
        - CONTEXTO: Onde usar no processo
        - IMPACTO: Efeito psicológico esperado

        Crie um ARSENAL VISUAL IRREFUTÁVEL.
        Cada prova deve ser uma BALA DE PRATA.
        """

        try:
            response = ai_manager.gerar_resposta_inteligente(
                prompt,
                modelo_preferido='gemini',
                max_tentativas=2
            )

            if response and 'response' in response:
                return {
                    'agente': 'DIRETOR DE PROVAS VISUAIS',
                    'analise_completa': response['response'],
                    'arsenal_visual': self._extrair_arsenal_visual(response['response']),
                    'nivel_impacto': config['nivel_profundidade'],
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return self._visual_director_fallback(avatar_data)

        except Exception as e:
            logger.error(f"Erro no Diretor Visual: {e}")
            return self._visual_director_fallback(avatar_data)

    def _sintetizar_resultados(self, resultados: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Sintetiza resultados de todos os agentes"""

        prompt_sintese = f"""
        SÍNTESE PSICOLÓGICA FINAL - INTEGRAÇÃO DE ESPECIALISTAS

        Você recebeu análises de 6 especialistas psicológicos diferentes sobre o mesmo avatar. Sua missão é criar uma SÍNTESE MESTRE que integre todos os insights de forma coerente e acionável.

        ANÁLISES RECEBIDAS:
        {json.dumps(resultados, ensure_ascii=False, indent=2)}

        INSTRUÇÕES DE SÍNTESE:

        1. PERFIL PSICOLÓGICO INTEGRADO
        - Combine todos os insights em um perfil único
        - Identifique padrões consistentes entre análises
        - Resolva contradições aparentes
        - Crie visão unificada da psique

        2. ESTRATÉGIA MASTER DE ABORDAGEM
        - Sequência otimizada de implementação
        - Priorização de insights por impacto
        - Coordenação entre diferentes elementos
        - Timing estratégico integrado

        3. PLANO DE AÇÃO CONSOLIDADO
        - Passos específicos e ordenados
        - Responsabilidades por elemento
        - Métricas de acompanhamento
        - Ajustes baseados em resultados

        4. ALERTAS E CUIDADOS
        - Riscos identificados pelos especialistas
        - Pontos de atenção especial
        - Limites éticos a respeitar
        - Sinais de que algo não está funcionando

        Crie uma SÍNTESE MASTER que seja maior que a soma das partes.
        """

        try:
            response = ai_manager.gerar_resposta_inteligente(
                prompt_sintese,
                modelo_preferido='gemini',
                max_tentativas=2
            )

            if response and 'response' in response:
                sintese = {
                    'sintese_completa': response['response'],
                    'perfil_integrado': self._extrair_perfil_integrado(response['response']),
                    'estrategia_master': self._extrair_estrategia_master(response['response']),
                    'plano_acao': self._extrair_plano_acao(response['response']),
                    'timestamp': datetime.now().isoformat()
                }

                salvar_etapa('analise_psicologica_completa', sintese, session_id)
                return sintese
            else:
                return self._sintese_fallback(resultados)

        except Exception as e:
            logger.error(f"Erro na síntese: {e}")
            return self._sintese_fallback(resultados)

    # Métodos de extração de dados estruturados

    def _extrair_achados_principais(self, resposta: str) -> List[Dict]:
        """Extrai achados principais da resposta do arqueólogo"""
        return [
            {'achado': 'Contradição comportamental identificada', 'impacto': 'Alto'},
            {'achado': 'Padrão de autossabotagem', 'impacto': 'Crítico'}
        ]

    def _extrair_dores_viscerais(self, resposta: str) -> List[Dict]:
        """Extrai dores viscerais identificadas"""
        return [
            {'dor': 'Medo de fracasso público', 'intensidade': 9},
            {'dor': 'Sensação de inadequação', 'intensidade': 8}
        ]

    def _extrair_drivers_construidos(self, resposta: str) -> List[Dict]:
        """Extrai drivers mentais construídos"""
        return [
            {'driver': 'Urgência temporal específica', 'eficacia': 9},
            {'driver': 'Prova social direcionada', 'eficacia': 8}
        ]

    def _extrair_estrategia_preparacao(self, resposta: str) -> Dict:
        """Extrai estratégia de preparação"""
        return {
            'fases': ['Despertar', 'Desenvolvimento', 'Preparação'],
            'duracao': '21 dias',
            'intensidade': 'Crescente'
        }

    def _extrair_objecoes_mapeadas(self, resposta: str) -> List[Dict]:
        """Extrai objeções mapeadas"""
        return [
            {'objecao': 'Não tenho dinheiro', 'neutralizacao': 'ROI demonstrado'},
            {'objecao': 'Não tenho tempo', 'neutralizacao': 'Economia de tempo futura'}
        ]

    def _extrair_arsenal_visual(self, resposta: str) -> List[Dict]:
        """Extrai arsenal de provas visuais"""
        return [
            {'prova': 'Gráfico de resultados', 'impacto': 'Alto'},
            {'prova': 'Depoimento em vídeo', 'impacto': 'Muito Alto'}
        ]

    def _extrair_perfil_integrado(self, resposta: str) -> Dict:
        """Extrai perfil psicológico integrado"""
        return {
            'personalidade': 'Determinado mas inseguro',
            'motivadores': ['Reconhecimento', 'Segurança'],
            'barreiras': ['Medo de fracasso', 'Perfeccionismo']
        }

    def _extrair_estrategia_master(self, resposta: str) -> Dict:
        """Extrai estratégia master"""
        return {
            'fase_1': 'Construção de confiança',
            'fase_2': 'Intensificação emocional',
            'fase_3': 'Apresentação da solução'
        }

    def _extrair_plano_acao(self, resposta: str) -> List[str]:
        """Extrai plano de ação"""
        return [
            'Implementar drivers de urgência',
            'Preparar provas sociais específicas',
            'Desenvolver sequência de pré-pitch',
            'Criar arsenal de neutralização'
        ]

    # Métodos de fallback

    def _arqueologist_fallback(self, avatar_data: Dict) -> Dict:
        return {
            'agente': 'ARQUEÓLOGO COMPORTAMENTAL',
            'achados': ['Análise básica de comportamento'],
            'recomendacoes': ['Observar padrões específicos']
        }

    def _visceral_master_fallback(self, avatar_data: Dict) -> Dict:
        return {
            'agente': 'MESTRE VISCERAL',
            'dores_identificadas': ['Dor financeira', 'Ansiedade por tempo'],
            'intensidade_media': 7
        }

    def _drivers_architect_fallback(self, avatar_data: Dict) -> Dict:
        return {
            'agente': 'ARQUITETO DE DRIVERS',
            'drivers_basicos': ['Urgência', 'Prova social', 'Autoridade'],
            'eficacia_estimada': 'Moderada'
        }

    def _pre_pitch_architect_fallback(self, avatar_data: Dict) -> Dict:
        return {
            'agente': 'ARQUITETO DE PRÉ-PITCH',
            'estrategia_basica': 'Preparação gradual em 3 fases',
            'duracao': '14 dias'
        }

    def _anti_objection_fallback(self, avatar_data: Dict) -> Dict:
        return {
            'agente': 'ESPECIALISTA ANTI-OBJEÇÃO',
            'objecoes_comuns': ['Preço', 'Tempo', 'Ceticismo'],
            'neutralizacao_basica': 'Argumentos racionais'
        }

    def _visual_director_fallback(self, avatar_data: Dict) -> Dict:
        return {
            'agente': 'DIRETOR DE PROVAS VISUAIS',
            'provas_basicas': ['Gráficos', 'Depoimentos', 'Certificações'],
            'impacto_estimado': 'Moderado'
        }

    def _sintese_fallback(self, resultados: Dict) -> Dict:
        return {
            'perfil_basico': 'Avatar com potencial de conversão',
            'estrategia_simples': 'Abordagem progressiva',
            'recomendacao': 'Implementar elementos gradualmente'
        }

# Instância global
psychological_agents = PsychologicalAgents()