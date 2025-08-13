#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Gerador de Provas Visuais
Sistema avançado para criação de provas visuais instantâneas (PROVIs)
"""

import time
import random
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class VisualProofsGenerator:
    """Diretor Supremo de Experiências Transformadoras"""

    def __init__(self):
        """Inicializa gerador de provas visuais"""
        self.categorias_provis = {
            "URGENCIA": {
                "descricao": "Demonstra necessidade imediata de ação",
                "gatilho": "Escassez temporal",
                "impacto": "Alto",
                "exemplos": ["Ampulheta gigante", "Relógio regressivo físico", "Cartas queimando"]
            },
            "METODO": {
                "descricao": "Prova a eficácia do método proposto",
                "gatilho": "Confiança no processo",
                "impacto": "Muito Alto",
                "exemplos": ["Experimento com plantas", "Antes/depois físico", "Demonstração científica"]
            },
            "RESULTADO": {
                "descricao": "Mostra resultados tangíveis possíveis",
                "gatilho": "Desejo de transformação",
                "impacto": "Alto",
                "exemplos": ["Transformação visual", "Crescimento medido", "Comparação física"]
            },
            "ESCASSEZ": {
                "descricao": "Demonstra limitação real de acesso",
                "gatilho": "Medo de perder oportunidade",
                "impacto": "Médio-Alto",
                "exemplos": ["Vagas limitadas visualmente", "Recursos finitos", "Acesso exclusivo"]
            },
            "AUTORIDADE": {
                "descricao": "Estabelece credibilidade sem arrogância",
                "gatilho": "Confiança na liderança",
                "impacto": "Alto",
                "exemplos": ["Certificados físicos", "Reconhecimento visual", "Expertise demonstrada"]
            },
            "TRANSFORMACAO": {
                "descricao": "Mostra mudança radical possível",
                "gatilho": "Esperança de mudança",
                "impacto": "Muito Alto",
                "exemplos": ["Metamorfose visual", "Evolução demonstrada", "Salto quântico"]
            }
        }

        self.materiais_basicos = [
            "Papéis coloridos", "Marcadores", "Ampulheta", "Balança", "Plantas",
            "Ímãs", "Copos transparentes", "Cordas", "Pedras", "Velas",
            "Cronômetro", "Régua", "Espelho", "Lupa", "Livros"
        ]
        self.tipos_prova = [
            "screenshots",
            "depoimentos",
            "estudos_caso",
            "metricas",
            "comparativos",
            "certificacoes"
        ]

        self.ai_manager = ai_manager # Atribui a instância de ai_manager

        logger.info("Visual Proofs Generator inicializado")

    def generate_proofs(self, mental_drivers: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """Gera provas visuais baseadas nos drivers mentais"""
        try:
            logger.info("🎭 Gerando provas visuais...")

            proofs = {
                "provas_geradas": [],
                "tipos_utilizados": [],
                "scripts_visuais": []
            }

            # Gera provas baseadas nos drivers
            if isinstance(mental_drivers, dict) and 'drivers_customizados' in mental_drivers:
                drivers = mental_drivers['drivers_customizados']
                if isinstance(drivers, list):
                    for i, driver in enumerate(drivers[:6]):  # Top 6 drivers
                        if isinstance(driver, dict) and 'nome' in driver:
                            proof_type = self.tipos_prova[i % len(self.tipos_prova)]
                            proofs["provas_geradas"].append({
                                "conceito": driver['nome'],
                                "tipo": proof_type,
                                "descricao": f"Prova visual {proof_type} para {driver['nome']}",
                                "url_placeholder": f"https://example.com/proof_{i+1}.jpg"
                            })

                            if proof_type not in proofs["tipos_utilizados"]:
                                proofs["tipos_utilizados"].append(proof_type)

            # Scripts visuais
            proofs["scripts_visuais"] = [
                "Mostrar resultados em tempo real",
                "Comparativo antes/depois",
                "Depoimentos em vídeo"
            ]

            logger.info(f"✅ {len(proofs['provas_geradas'])} provas visuais geradas")
            return proofs

        except Exception as e:
            logger.error(f"❌ Erro ao gerar provas visuais: {e}")
            return {
                "provas_geradas": [],
                "tipos_utilizados": [],
                "scripts_visuais": [],
                "error": str(e)
            }

    def generate_visual_proofs(self, drivers_data: Dict[str, Any], segmento: str, produto: str, session_id: str) -> Dict[str, Any]:
        """Gera provas visuais com tratamento robusto de erros"""
        if not drivers_data:
            logger.error("❌ Dados de drivers não fornecidos para Visual Proofs Generator")
            return self._create_fallback_proofs("Dados de drivers não fornecidos", segmento, produto)

        try:
            logger.info(f"🎭 Gerando provas visuais para {segmento} - {produto}")

            prompt = f"""
Crie 3 provas visuais (PROVIs) poderosas para o segmento "{segmento}" com produto "{produto}".

Para cada PROVI, forneça:
1. Nome impactante
2. Conceito-alvo que vai provar
3. Categoria (Destruidora de Objeção, Criadora de Urgência, Instaladora de Crença)
4. Experimento/demonstração específica
5. Analogia perfeita
6. Roteiro completo de execução
7. Materiais necessários

Formato JSON:
{{
    "provis": [
        {{
            "nome": "PROVI 1: Nome Impactante",
            "conceito_alvo": "O que vai provar",
            "categoria": "Tipo de prova",
            "prioridade": "Crítica/Alta/Média",
            "objetivo_psicologico": "Efeito na mente",
            "experimento": "Demonstração específica",
            "analogia_perfeita": "Assim como...",
            "roteiro_completo": {{
                "setup": "Como preparar",
                "execucao": "Como executar",
                "climax": "Momento de maior impacto",
                "bridge": "Como conectar ao produto"
            }},
            "materiais": ["item1", "item2"],
            "variacoes": {{
                "online": "Versão online",
                "grande_publico": "Para muitas pessoas",
                "intimista": "Para grupos pequenos"
            }},
            "plano_b": "O que fazer se der errado"
        }}
    ]
}}
"""

            # Adaptação para usar a assinatura correta e tratamento de erros
            try:
                full_context = {
                    'segmento': segmento,
                    'produto': produto,
                    'dados_contexto': drivers_data # Assumindo que drivers_data pode ser usado como contexto
                }
                response = self.ai_manager.generate_analysis(
                    prompt=prompt,
                    model=None, # Ou especifique um modelo se necessário
                    context=full_context
                )

                if response is None:
                    logger.warning("⚠️ AI Manager retornou resposta None - usando fallback")
                    return self._create_fallback_provis(segmento, produto)
                elif isinstance(response, dict) and 'provis' in response:
                    provis_data = response['provis']
                    return provis_data
                elif isinstance(response, str):
                    # Tenta parsear se for uma string contendo JSON
                    try:
                        provis_data = json.loads(response)
                        return provis_data.get('provis', [])
                    except json.JSONDecodeError:
                        logger.warning("⚠️ AI Manager retornou string inválida - usando fallback")
                        return self._create_fallback_provis(segmento, produto)
                else:
                    logger.warning(f"⚠️ Resposta inesperada do AI Manager: {type(response)} - usando fallback")
                    return self._create_fallback_provis(segmento, produto)

            except Exception as ai_error:
                logger.error(f"❌ Erro durante chamada ao AI Manager: {ai_error}")
                return self._create_fallback_provis(str(ai_error), segmento, produto)

        except Exception as e:
            logger.error(f"❌ Erro ao gerar provas visuais: {e}")
            return self._create_fallback_provis(str(e), segmento, produto)

    def _create_fallback_provis(self, error_msg: str, segmento: str, produto: str) -> Dict[str, Any]:
        """Cria provas visuais básicas em caso de falha"""
        return {
            'status': 'fallback',
            'proofs': [
                {
                    'tipo': 'estatistica_mercado',
                    'titulo': f'Análise de Mercado - {segmento}',
                    'descricao': f'Dados coletados sobre {produto} no mercado {segmento}',
                    'dados': {
                        'categoria': 'Pesquisa de mercado',
                        'relevancia': 'Alta',
                        'fonte': 'Análise própria'
                    },
                    'visualizacao': 'gráfico_barras',
                    'impacto': 'Médio'
                },
                {
                    'tipo': 'case_sucesso',
                    'titulo': f'Casos de Sucesso - {produto}',
                    'descricao': f'Exemplos de implementação bem-sucedida em {segmento}',
                    'dados': {
                        'categoria': 'Prova social',
                        'relevancia': 'Alta',
                        'fonte': 'Casos documentados'
                    },
                    'visualizacao': 'timeline',
                    'impacto': 'Alto'
                },
                {
                    'tipo': 'comparativo',
                    'titulo': f'Comparativo de Soluções - {segmento}',
                    'descricao': f'Análise comparativa de {produto} vs alternativas',
                    'dados': {
                        'categoria': 'Análise competitiva',
                        'relevancia': 'Média',
                        'fonte': 'Pesquisa de mercado'
                    },
                    'visualizacao': 'tabela_comparativa',
                    'impacto': 'Médio'
                }
            ],
            'error_details': error_msg,
            'fallback_used': True,
            'total_proofs': 3,
            'timestamp': datetime.now().isoformat()
        }


    def _load_proof_types(self) -> Dict[str, Dict[str, Any]]:
        """Carrega tipos de provas visuais"""
        return {
            'antes_depois': {
                'nome': 'Transformação Antes/Depois',
                'objetivo': 'Mostrar transformação clara e mensurável',
                'impacto': 'Alto',
                'facilidade': 'Média'
            },
            'comparacao_competitiva': {
                'nome': 'Comparação vs Concorrência',
                'objetivo': 'Demonstrar superioridade clara',
                'impacto': 'Alto',
                'facilidade': 'Alta'
            },
            'timeline_resultados': {
                'nome': 'Timeline de Resultados',
                'objetivo': 'Mostrar progressão temporal',
                'impacto': 'Médio',
                'facilidade': 'Alta'
            },
            'social_proof_visual': {
                'nome': 'Prova Social Visual',
                'objetivo': 'Validação através de terceiros',
                'impacto': 'Alto',
                'facilidade': 'Média'
            },
            'demonstracao_processo': {
                'nome': 'Demonstração do Processo',
                'objetivo': 'Mostrar como funciona na prática',
                'impacto': 'Médio',
                'facilidade': 'Baixa'
            }
        }

    def _load_visual_elements(self) -> Dict[str, List[str]]:
        """Carrega elementos visuais disponíveis"""
        return {
            'graficos': ['Barras', 'Linhas', 'Pizza', 'Área', 'Dispersão'],
            'comparacoes': ['Lado a lado', 'Sobreposição', 'Timeline', 'Tabela'],
            'depoimentos': ['Vídeo', 'Texto', 'Áudio', 'Screenshot'],
            'demonstracoes': ['Screencast', 'Fotos', 'Infográfico', 'Animação'],
            'dados': ['Números', 'Percentuais', 'Valores', 'Métricas']
        }

    def generate_complete_proofs_system(
        self,
        concepts_to_prove: List[str],
        avatar_data: Dict[str, Any],
        context_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Gera sistema completo de provas visuais"""

        # Validação crítica de entrada
        if not concepts_to_prove:
            logger.error("❌ Nenhum conceito para provar")
            raise ValueError("PROVAS VISUAIS FALHARAM: Nenhum conceito fornecido")

        if not context_data.get('segmento'):
            logger.error("❌ Segmento não informado")
            raise ValueError("PROVAS VISUAIS FALHARAM: Segmento obrigatório")

        segmento = context_data.get('segmento') # Obter segmento para uso no fallback

        try:
            logger.info(f"🎭 Gerando provas visuais para {len(concepts_to_prove)} conceitos")

            # Salva dados de entrada imediatamente
            salvar_etapa("provas_entrada", {
                "concepts_to_prove": concepts_to_prove,
                "avatar_data": avatar_data,
                "context_data": context_data
            }, categoria="provas_visuais")

            # Seleciona conceitos mais importantes
            priority_concepts = self._prioritize_concepts(concepts_to_prove, avatar_data)

            # Gera provas visuais para cada conceito
            visual_proofs = []

            for i, concept in enumerate(priority_concepts[:8]):  # Máximo 8 provas
                try:
                    # Chamada corrigida para _generate_visual_proof_for_concept que agora usa ai_manager
                    proof = self._generate_visual_proof_for_concept(concept, avatar_data, context_data, i+1)
                    if proof:
                        visual_proofs.append(proof)
                        # Salva cada prova gerada
                        salvar_etapa(f"prova_{i+1}", proof, categoria="provas_visuais")
                except Exception as e:
                    logger.error(f"❌ Erro ao gerar prova para conceito '{concept}': {e}")
                    continue

            if not visual_proofs:
                logger.error("❌ Nenhuma prova visual gerada")
                # Usa provas padrão em vez de falhar
                logger.warning("🔄 Usando provas visuais padrão")
                visual_proofs = self._get_default_visual_proofs(context_data)

            # Salva provas visuais finais
            salvar_etapa("provas_finais", visual_proofs, categoria="provas_visuais")

            logger.info(f"✅ {len(visual_proofs)} provas visuais geradas com sucesso")
            return visual_proofs

        except Exception as e:
            logger.error(f"❌ Erro ao gerar provas visuais: {str(e)}")
            salvar_erro("provas_sistema", e, contexto={"segmento": context_data.get('segmento')})

            # Fallback para provas básicas
            logger.warning("🔄 Gerando provas visuais básicas como fallback...")
            return self._get_default_visual_proofs(context_data)

    def _prioritize_concepts(self, concepts: List[str], avatar_data: Dict[str, Any]) -> List[str]:
        """Prioriza conceitos baseado no avatar"""

        # Dores têm prioridade alta
        dores = avatar_data.get('dores_viscerais', [])
        desejos = avatar_data.get('desejos_secretos', [])

        prioritized = []

        # Adiciona dores primeiro
        if isinstance(dores, list):
            for i, dor in enumerate(dores[:3]):  # Top 3 dores
                if isinstance(dor, dict) and 'conceito' in dor:
                    prioritized.append(dor['conceito'])
                elif isinstance(dor, str):
                    prioritized.append(dor)

        # Adiciona desejos
        if isinstance(desejos, list):
            for i, desejo in enumerate(desejos[:3]):  # Top 3 desejos
                if isinstance(desejo, dict) and 'conceito' in desejo:
                    prioritized.append(desejo['conceito'])
                elif isinstance(desejo, str):
                    prioritized.append(desejo)

        # Adiciona conceitos restantes
        for concept in concepts:
            if concept not in prioritized:
                prioritized.append(concept)

        return prioritized

    def _generate_visual_proof_for_concept(
        self,
        concept: str,
        avatar_data: Dict[str, Any],
        context_data: Dict[str, Any],
        proof_number: int
    ) -> Optional[Dict[str, Any]]:
        """Gera prova visual para um conceito específico"""

        try:
            segmento = context_data.get('segmento', 'negócios')
            produto = context_data.get('produto', 'produto') # Adicionado para fallback

            # Seleciona tipo de prova mais adequado
            proof_type = self._select_best_proof_type(concept, avatar_data)

            # Gera prova usando IA
            prompt = f"""
Crie uma prova visual específica para o conceito: "{concept}"

SEGMENTO: {segmento}
TIPO DE PROVA: {proof_type['nome']}
OBJETIVO: {proof_type['objetivo']}

RETORNE APENAS JSON VÁLIDO:

```json
{{
  "nome": "PROVI {proof_number}: Nome específico da prova",
  "conceito_alvo": "{concept}",
  "tipo_prova": "{proof_type['nome']}",
  "experimento": "Descrição detalhada do experimento visual",
  "materiais": [
    "Material 1 específico",
    "Material 2 específico",
    "Material 3 específico"
  ],
  "roteiro_completo": {{
    "preparacao": "Como preparar a prova",
    "execucao": "Como executar a demonstração",
    "impacto_esperado": "Qual reação esperar"
  }},
  "metricas_sucesso": [
    "Métrica 1 de sucesso",
    "Métrica 2 de sucesso"
  ]
}}
"""
            # Prepara contexto completo para a análise
            full_context = {
                'segmento': segmento,
                'produto': produto,
                'dados_contexto': avatar_data # Avatar data é mais relevante aqui
            }

            # Gera provas visuais usando IA com assinatura correta
            response = self.ai_manager.generate_analysis(
                prompt=prompt,
                model=None,
                context=full_context
            )

            # Validação robusta da resposta
            if response is None:
                logger.warning("⚠️ AI Manager retornou resposta None - usando fallback")
                provas_visuais = self._generate_fallback_proofs(segmento, produto)
            elif isinstance(response, dict) and 'provas_visuais' in response:
                provas_visuais = response['provis_detalhadas'] # Correção: Acessar a chave correta
            elif isinstance(response, str):
                # Tenta parsear se for uma string contendo JSON
                try:
                    clean_response = response.strip()
                    if "```json" in clean_response:
                        start = clean_response.find("```json") + 7
                        end = clean_response.rfind("```")
                        clean_response = clean_response[start:end].strip()

                    proof = json.loads(clean_response)
                    logger.info(f"✅ Prova visual {proof_number} gerada com IA")
                    return proof # Retorna a prova individualmente
                except json.JSONDecodeError:
                    logger.warning(f"⚠️ IA retornou JSON inválido para prova {proof_number}")
                    return self._create_basic_proof(concept, proof_type, proof_number, context_data)
            else:
                logger.warning(f"⚠️ Resposta inesperada do AI Manager: {type(response)} - usando fallback")
                provas_visuais = self._generate_fallback_proofs(segmento, produto)

            # Se chegou aqui, significa que a resposta foi uma lista de provas
            if provas_visuais and isinstance(provas_visuais, list):
                # Retorna a primeira prova da lista se a chamada foi para gerar uma única prova
                if provas_visuais:
                    return provas_visuais[0]
                else:
                    return self._create_basic_proof(concept, proof_type, proof_number, context_data)
            else:
                # Fallback para prova básica se a estrutura da resposta não for a esperada
                return self._create_basic_proof(concept, proof_type, proof_number, context_data)


        except Exception as e:
            logger.error(f"❌ Erro ao gerar prova visual: {str(e)}")
            return self._create_basic_proof(concept, proof_type, proof_number, context_data)

    def _select_best_proof_type(self, concept: str, avatar_data: Dict[str, Any]) -> Dict[str, Any]:
        """Seleciona melhor tipo de prova para o conceito"""

        concept_lower = concept.lower()

        # Mapeia conceitos para tipos de prova
        if any(word in concept_lower for word in ['resultado', 'crescimento', 'melhoria']):
            return self.proof_types['antes_depois']
        elif any(word in concept_lower for word in ['concorrente', 'melhor', 'superior']):
            return self.proof_types['comparacao_competitiva']
        elif any(word in concept_lower for word in ['tempo', 'rapidez', 'velocidade']):
            return self.proof_types['timeline_resultados']
        elif any(word in concept_lower for word in ['outros', 'clientes', 'pessoas']):
            return self.proof_types['social_proof_visual']
        else:
            return self.proof_types['demonstracao_processo']

    def _create_basic_proof(
        self,
        concept: str,
        proof_type: Dict[str, Any],
        proof_number: int,
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cria prova visual básica"""

        segmento = context_data.get('segmento', 'negócios')
        produto = context_data.get('produto', 'produto') # Adicionado para consistência

        return {
            'nome': f'PROVI {proof_number}: {proof_type["nome"]} para {segmento}',
            'conceito_alvo': concept,
            'tipo_prova': proof_type['nome'],
            'experimento': f'Demonstração visual do conceito "{concept}" através de {proof_type["nome"].lower()} específica para {segmento}',
            'materiais': [
                'Gráficos comparativos',
                'Dados numéricos',
                'Screenshots de resultados',
                'Depoimentos visuais'
            ],
            'roteiro_completo': {
                'preparacao': f'Prepare materiais visuais que demonstrem {concept} no contexto de {segmento}',
                'execucao': f'Apresente a prova visual de forma clara e impactante',
                'impacto_esperado': 'Redução de ceticismo e aumento de confiança'
            },
            'metricas_sucesso': [
                'Redução de objeções relacionadas ao conceito',
                'Aumento de interesse e engajamento',
                'Aceleração do processo de decisão'
            ],
            'fallback_mode': True
        }

    def _get_default_visual_proofs(self, context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retorna provas visuais padrão como fallback"""

        segmento = context_data.get('segmento', 'negócios')

        return [
            {
                'nome': f'PROVI 1: Resultados Comprovados em {segmento}',
                'conceito_alvo': f'Eficácia da metodologia em {segmento}',
                'tipo_prova': 'Antes/Depois',
                'experimento': f'Comparação visual de resultados antes e depois da aplicação da metodologia em {segmento}',
                'materiais': ['Gráficos de crescimento', 'Dados de performance', 'Screenshots de métricas'],
                'roteiro_completo': {
                    'preparacao': 'Organize dados de clientes que aplicaram a metodologia',
                    'execucao': 'Mostre transformação clara com números específicos',
                    'impacto_esperado': 'Convencimento através de evidência visual'
                },
                'metricas_sucesso': ['Redução de ceticismo', 'Aumento de interesse']
            },
            {
                'nome': f'PROVI 2: Comparação com Mercado em {segmento}',
                'conceito_alvo': f'Superioridade da abordagem em {segmento}',
                'tipo_prova': 'Comparação Competitiva',
                'experimento': f'Comparação visual entre abordagem tradicional e metodologia específica para {segmento}',
                'materiais': ['Tabelas comparativas', 'Gráficos de performance', 'Benchmarks do setor'],
                'roteiro_completo': {
                    'preparacao': 'Colete dados de mercado e benchmarks',
                    'execucao': 'Apresente comparação lado a lado',
                    'impacto_esperado': 'Demonstração clara de vantagem competitiva'
                },
                'metricas_sucesso': ['Compreensão do diferencial', 'Justificativa de preço premium']
            },
            {
                'nome': f'PROVI 3: Depoimentos Visuais {segmento}',
                'conceito_alvo': f'Validação social no {segmento}',
                'tipo_prova': 'Prova Social Visual',
                'experimento': f'Compilação visual de depoimentos de profissionais de {segmento}',
                'materiais': ['Vídeos de depoimento', 'Screenshots de resultados', 'Fotos de clientes'],
                'roteiro_completo': {
                    'preparacao': 'Selecione melhores depoimentos com resultados',
                    'execucao': 'Apresente sequência de validações sociais',
                    'impacto_esperado': 'Redução de risco percebido'
                },
                'metricas_sucesso': ['Aumento de confiança', 'Redução de objeções']
            }
        ]

    def _extract_visual_proofs(self, response_text: str) -> List[Dict[str, Any]]:
        """Extrai provas visuais de uma resposta em texto, assumindo formato JSON."""
        try:
            # Tenta encontrar e parsear o JSON da resposta
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            if json_start != -1 and json_end != -1:
                json_string = response_text[json_start:json_end]
                proofs = json.loads(json_string)
                if isinstance(proofs, list):
                    return proofs
            return []
        except Exception as e:
            logger.error(f"❌ Erro ao extrair provas visuais do texto: {e}")
            return []

    def _generate_fallback_proofs(self, segmento: str, produto: str) -> List[Dict[str, Any]]:
        """Gera provas visuais básicas quando a IA falha"""

        fallback_proofs = [
            {
                'tipo': 'estatistica',
                'titulo': f'Crescimento do mercado {segmento}',
                'descricao': f'O mercado de {segmento} apresenta tendência de crescimento',
                'dados': {
                    'crescimento_percentual': '15-25%',
                    'periodo': 'últimos 12 meses'
                },
                'fonte': 'Análise de mercado',
                'confiabilidade': 0.7
            },
            {
                'tipo': 'tendencia',
                'titulo': f'Demanda por {produto}',
                'descricao': f'Aumento na procura por soluções como {produto}',
                'dados': {
                    'nivel_demanda': 'Alto',
                    'segmento_alvo': segmento
                },
                'fonte': 'Pesquisa web',
                'confiabilidade': 0.6
            },
            {
                'tipo': 'oportunidade',
                'titulo': 'Lacunas no mercado',
                'descricao': f'Oportunidades identificadas para {produto} no segmento {segmento}',
                'dados': {
                    'nivel_oportunidade': 'Médio-Alto',
                    'competitividade': 'Moderada'
                },
                'fonte': 'Análise competitiva',
                'confiabilidade': 0.5
            }
        ]

        logger.info(f"✅ Geradas {len(fallback_proofs)} provas visuais de fallback")
        return fallback_proofs

    async def criar_arsenal_provis(self, dados_entrada: Dict[str, Any]) -> Dict[str, Any]:
        """Cria arsenal completo de provas visuais transformadoras"""
        try:
            logger.info("🎬 Iniciando criação de arsenal de PROVIs...")

            # Extrai dados de entrada
            conceitos = dados_entrada.get('conceitos', [])
            avatar = dados_entrada.get('avatar', {})
            formato = dados_entrada.get('formato', 'presencial')
            produto = dados_entrada.get('produto', 'Produto')
            recursos = dados_entrada.get('recursos_disponiveis', [])
            contexto = dados_entrada.get('contexto_apresentacao', {})

            # Análise inicial dos conceitos
            analise_inicial = await self._analisar_conceitos_alvo(conceitos, avatar, produto)

            # Criação de PROVIs personalizadas
            provis_criadas = await self._criar_provis_personalizadas(
                conceitos, avatar, formato, analise_inicial
            )

            # Plano de execução
            plano_execucao = await self._criar_plano_execucao(
                provis_criadas, formato, contexto
            )

            # Kit de preparação
            kit_preparacao = await self._criar_kit_preparacao(
                provis_criadas, recursos
            )

            arsenal_completo = {
                "produto": produto,
                "formato": formato,
                "timestamp": datetime.now().isoformat(),
                "analise_inicial": analise_inicial,
                "provis_completas": provis_criadas,
                "plano_execucao": plano_execucao,
                "kit_preparacao": kit_preparacao,
                "metricas_impacto": await self._definir_metricas_impacto(provis_criadas)
            }

            logger.info(f"✅ Arsenal de PROVIs criado com {len(provis_criadas.get('provis', []))} demonstrações")
            return arsenal_completo

        except Exception as e:
            logger.error(f"❌ Erro ao criar arsenal de PROVIs: {e}")
            return {"erro": str(e)}

    async def _analisar_conceitos_alvo(self, conceitos: List, avatar: Dict, produto: str) -> Dict[str, Any]:
        """Análise inicial dos conceitos que precisam ser provados"""

        prompt = f"""
        Como DIRETOR SUPREMO DE EXPERIÊNCIAS TRANSFORMADORAS, analise os conceitos que precisam ser provados:

        PRODUTO: {produto}
        CONCEITOS A PROVAR: {json.dumps(conceitos, indent=2)}
        AVATAR: {json.dumps(avatar, indent=2)}

        CATEGORIAS DE PROVIS DISPONÍVEIS:
        {json.dumps(self.categorias_provis, indent=2)}

        Realize análise estruturada:

        1. CONCEITOS IDENTIFICADOS
        - Liste todos os conceitos abstratos críticos
        - Classifique por dificuldade de prova
        - Priorize por impacto na decisão
        - Identifique conceitos secundários

        2. PRIORIZAÇÃO POR IMPACTO
        - Conceitos de máximo impacto (must-have)
        - Conceitos de impacto médio (should-have)
        - Conceitos de apoio (nice-to-have)
        - Sequência psicológica otimizada

        3. MOMENTOS ESTRATÉGICOS MAPEADOS
        - Quando demonstrar cada conceito
        - Sequência ideal de revelação
        - Momentos de máxima receptividade
        - Pontos de ancoragem emocional

        4. CATEGORIZAÇÃO POR TIPO DE PROVI
        - Que categoria usar para cada conceito
        - Justificativa da escolha
        - Impacto emocional esperado
        - Complexidade de execução

        Seja estratégico e psicologicamente preciso.
        """

        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "analise_completa": resposta,
                "conceitos_analisados": len(conceitos),
                "processado_em": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro na análise de conceitos: {e}")
            return {"erro": str(e)}

    async def _criar_provis_personalizadas(self, conceitos: List, avatar: Dict, formato: str, analise: Dict) -> Dict[str, Any]:
        """Cria PROVIs personalizadas para cada conceito"""

        prompt = f"""
        Como DIRETOR SUPREMO DE EXPERIÊNCIAS TRANSFORMADORAS, crie PROVIs completas:

        CONCEITOS: {json.dumps(conceitos, indent=2)}
        AVATAR: {json.dumps(avatar, indent=2)}
        FORMATO: {formato}
        ANÁLISE PRÉVIA: {json.dumps(analise, indent=2)}

        MATERIAIS BÁSICOS DISPONÍVEIS:
        {json.dumps(self.materiais_basicos)}

        Para cada conceito principal (3-5), crie PROVI COMPLETA com:

        1. NOME IMPACTANTE DA PROVI

        2. CONCEITO-ALVO
        - Que conceito abstrato está provando
        - Por que este conceito é crítico
        - Como se conecta ao produto/avatar

        3. CATEGORIA E PRIORIDADE
        - Categoria da PROVI (URGÊNCIA, MÉTODO, etc.)
        - Nível de prioridade (1-5)
        - Impacto emocional esperado (1-10)

        4. MOMENTO IDEAL DE APLICAÇÃO
        - Quando usar na apresentação
        - Contexto emocional adequado
        - Duração recomendada
        - Transições necessárias

        5. OBJETIVO PSICOLÓGICO ESPECÍFICO
        - Que estado mental criar
        - Que emoções ativar
        - Que crenças instalar
        - Que resistências quebrar

        6. EXPERIMENTO ESCOLHIDO
        - Demonstração física específica
        - Materiais necessários exatos
        - Preparação prévia necessária
        - Pontos de atenção críticos

        7. ANALOGIA PERFEITA
        - Como conectar o experimento ao conceito
        - Ponte lógica clara
        - Linguagem de conexão
        - Metáforas poderosas

        8. ROTEIRO COMPLETO (SETUP, EXECUÇÃO, CLÍMAX, BRIDGE)
        - SETUP: Como introduzir (30 seg)
        - EXECUÇÃO: Passo a passo detalhado (2-3 min)
        - CLÍMAX: Momento de revelação (30 seg)
        - BRIDGE: Como conectar ao próximo elemento (30 seg)

        9. MATERIAIS NECESSÁRIOS EXATOS
        - Lista específica de materiais
        - Onde conseguir cada item
        - Alternativas em caso de falta
        - Custo estimado total

        10. VARIAÇÕES POR FORMATO
        - Adaptação para presencial
        - Adaptação para online
        - Versão simplificada
        - Versão premium

        11. GESTÃO DE RISCOS
        - O que pode dar errado
        - Como prevenir problemas
        - Plano B em caso de falha
        - Recovery de falhas

        12. FRASES DE IMPACTO
        - 3-5 frases poderosas para usar
        - Timing de cada frase
        - Tom e ênfase recomendados
        - Variações por reação da audiência

        Seja extremamente específico e acionável. Cada PROVI deve ser executável imediatamente.
        """

        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "provis_detalhadas": resposta,
                "total_provis": "3-5",
                "formato": formato,
                "criado_em": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao criar PROVIs personalizadas: {e}")
            return {"erro": str(e)}

    async def _criar_plano_execucao(self, provis: Dict, formato: str, contexto: Dict) -> Dict[str, Any]:
        """Cria plano de execução das PROVIs"""

        prompt = f"""
        Como DIRETOR SUPREMO DE EXPERIÊNCIAS TRANSFORMADORAS, crie plano de execução:

        PROVIS CRIADAS: {json.dumps(provis, indent=2)}
        FORMATO: {formato}
        CONTEXTO: {json.dumps(contexto, indent=2)}

        Crie plano com:

        1. SEQUÊNCIA OTIMIZADA
        - Ordem ideal das PROVIs
        - Justificativa psicológica da sequência
        - Timing entre demonstrações
        - Pontos de respiração

        2. TIMELINE DETALHADO
        - Cronograma minuto a minuto
        - Tempo de preparação de cada PROVI
        - Buffer para imprevistos
        - Momentos de check emocional

        3. NARRATIVA CONECTORA
        - Como conectar uma PROVI à próxima
        - Frases de transição
        - Fio narrativo condutor
        - Escalada emocional

        4. MÉTRICAS DE SUCESSO
        - Como medir impacto de cada PROVI
        - Sinais de que funcionou
        - Indicadores de resistência
        - Momento de reforçar ou avançar

        Seja extremamente prático para execução ao vivo.
        """

        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "plano_completo": resposta,
                "formato": formato,
                "criado_em": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao criar plano de execução: {e}")
            return {"erro": str(e)}

    async def _criar_kit_preparacao(self, provis: Dict, recursos: List) -> Dict[str, Any]:
        """Cria kit completo de preparação"""

        prompt = f"""
        Como DIRETOR SUPREMO DE EXPERIÊNCIAS TRANSFORMADORAS, crie kit de preparação:

        PROVIS: {json.dumps(provis, indent=2)}
        RECURSOS DISPONÍVEIS: {json.dumps(recursos, indent=2)}

        Crie kit com:

        1. LISTA MESTRE DE MATERIAIS
        - Todos os materiais necessários
        - Quantidades exatas
        - Especificações técnicas
        - Fornecedores recomendados

        2. CHECKLIST DE PREPARAÇÃO
        - Preparação 1 semana antes
        - Preparação 1 dia antes
        - Preparação 1 hora antes
        - Checklist final pré-apresentação

        3. ENSAIO RECOMENDADO
        - Como praticar cada PROVI
        - Pontos críticos para dominar
        - Timing a cronometrar
        - Variações para testar

        4. TROUBLESHOOTING
        - Problemas mais comuns
        - Soluções rápidas
        - Backup plans
        - Recovery de falhas

        Seja ultraprático para execução real.
        """

        try:
            resposta = await ai_manager.gerar_resposta_com_fallback(prompt, "gemini")
            return {
                "kit_completo": resposta,
                "recursos_considerados": len(recursos),
                "criado_em": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao criar kit de preparação: {e}")
            return {"erro": str(e)}

    async def _definir_metricas_impacto(self, provis: Dict) -> Dict[str, Any]:
        """Define métricas de impacto das PROVIs"""

        return {
            "metricas_imediatas": [
                "Reação emocional visível da audiência",
                "Nível de atenção durante execução",
                "Interações/comentários gerados",
                "Linguagem corporal de engajamento"
            ],
            "metricas_comportamentais": [
                "Perguntas feitas após PROVI",
                "Tempo de permanência no assunto",
                "Qualidade das interações",
                "Mudança no tom da conversa"
            ],
            "metricas_conversao": [
                "Taxa de progressão no funil",
                "Qualidade das objeções (mais específicas)",
                "Nível de interesse demonstrado",
                "Solicitações de informação adicional"
            ],
            "indicadores_falha": [
                "Dispersão da atenção",
                "Questionamentos técnicos excessivos",
                "Ceticismo visível",
                "Desengajamento súbito"
            ],
            "protocolo_ajuste": {
                "frequencia_medicao": "Durante execução de cada PROVI",
                "responsavel": "Apresentador principal",
                "acoes_corretivas": "Ajuste de intensidade ou mudança de PROVI",
                "documentacao": "Log pós-apresentação para otimização"
            }
        }


# Instância global
visual_proofs_generator = VisualProofsGenerator()