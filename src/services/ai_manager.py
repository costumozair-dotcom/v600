import os
import logging
import time
import json
from typing import Dict, List, Optional, Any
import requests

# Imports condicionais para os clientes de IA
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from services.groq_client import groq_client
    HAS_GROQ_CLIENT = True
except ImportError:
    HAS_GROQ_CLIENT = False

logger = logging.getLogger(__name__)

class AIManager:
    """Gerenciador de IAs com sistema de fallback automático"""

    def __init__(self):
        """Inicializa o gerenciador de IAs"""
        self.providers = {
            'gemini': {
                'client': None,
                'available': False,
                'priority': 1,
                'error_count': 0,
                'model': 'gemini-2.5-pro',
                'max_errors': 2,
                'last_success': None,
                'consecutive_failures': 0,
                'enabled': True
            },
            'groq': {
                'client': None,
                'available': False,
                'priority': 2,
                'error_count': 0,
                'model': 'llama3-70b-8192',
                'max_errors': 2,
                'last_success': None,
                'consecutive_failures': 0,
                'enabled': True
            },
            'openai': {
                'client': None,
                'available': False,
                'priority': 3,
                'error_count': 0,
                'model': 'gpt-3.5-turbo',
                'max_errors': 2,
                'last_success': None,
                'consecutive_failures': 0,
                'enabled': True
            },
            'huggingface': {
                'client': None,
                'available': False,
                'priority': 4,
                'error_count': 0,
                'models': ["HuggingFaceH4/zephyr-7b-beta", "google/flan-t5-base"],
                'current_model_index': 0,
                'max_errors': 3,
                'last_success': None,
                'consecutive_failures': 0,
                'enabled': True
            }
        }

        self.initialize_providers()
        available_count = len([p for p in self.providers.values() if p['available']])
        logger.info(f"🤖 AI Manager inicializado com {available_count} provedores disponíveis.")

    def initialize_providers(self):
        """Inicializa todos os provedores de IA com base nas chaves de API disponíveis."""

        # Inicializa Gemini
        if HAS_GEMINI:
            try:
                gemini_key = os.getenv('GEMINI_API_KEY')
                if gemini_key:
                    genai.configure(api_key=gemini_key)
                    self.providers['gemini']['client'] = genai.GenerativeModel("gemini-2.5-pro")
                    self.providers['gemini']['available'] = True
                    logger.info("✅ Gemini 2.5 Pro (gemini-2.5-pro) inicializado como MODELO PRIMÁRIO")
            except Exception as e:
                logger.warning(f"⚠️ Falha ao inicializar Gemini: {str(e)}")
        else:
            logger.warning("⚠️ Biblioteca 'google-generativeai' não instalada.")

        # Inicializa OpenAI
        if HAS_OPENAI:
            try:
                openai_key = os.getenv('OPENAI_API_KEY')
                if openai_key:
                    self.providers["openai"]["client"] = openai.OpenAI(api_key=openai_key)
                    self.providers["openai"]["available"] = True
                    logger.info("✅ OpenAI (gpt-3.5-turbo) inicializado com sucesso")
            except Exception as e:
                logger.info(f"ℹ️ OpenAI não disponível: {str(e)}")
        else:
            logger.info("ℹ️ Biblioteca 'openai' não instalada.")

        # Inicializa Groq
        try:
            if HAS_GROQ_CLIENT and groq_client and groq_client.is_enabled():
                self.providers['groq']['client'] = groq_client
                self.providers['groq']['available'] = True
                logger.info("✅ Groq (llama3-70b-8192) inicializado com sucesso")
            else:
                logger.info("ℹ️ Groq client não configurado")
        except Exception as e:
            logger.info(f"ℹ️ Groq não disponível: {str(e)}")

        # Inicializa HuggingFace
        try:
            hf_key = os.getenv('HUGGINGFACE_API_KEY')
            if hf_key:
                self.providers['huggingface']['client'] = {
                    'api_key': hf_key,
                    'base_url': 'https://api-inference.huggingface.co/models/'
                }
                self.providers['huggingface']['available'] = True
                logger.info("✅ HuggingFace inicializado com sucesso")
        except Exception as e:
            logger.info(f"ℹ️ HuggingFace não disponível: {str(e)}")

    def get_best_provider(self) -> Optional[str]:
        """Retorna o melhor provedor disponível com base na prioridade e contagem de erros."""
        current_time = time.time()

        # Primeiro, tenta reabilitar provedores que podem ter se recuperado
        for name, provider in self.providers.items():
            if (not provider['available'] and 
                provider.get('last_success') and 
                current_time - provider['last_success'] > 300):  # 5 minutos
                logger.info(f"🔄 Tentando reabilitar provedor {name} após cooldown")
                provider['error_count'] = 0
                provider['consecutive_failures'] = 0
                if name == 'gemini' and HAS_GEMINI:
                    provider['available'] = True
                elif name == 'groq' and HAS_GROQ_CLIENT:
                    provider['available'] = True
                elif name == 'openai' and HAS_OPENAI:
                    provider['available'] = True
                elif name == 'huggingface':
                    provider['available'] = True

        available_providers = [
            (name, provider) for name, provider in self.providers.items() 
            if provider['available'] and provider['consecutive_failures'] < provider.get('max_errors', 2)
        ]

        if not available_providers:
            logger.warning("🔄 Nenhum provedor saudável disponível. Resetando contadores.")
            for provider in self.providers.values():
                provider['error_count'] = 0
                provider['consecutive_failures'] = 0
            available_providers = [(name, p) for name, p in self.providers.items() if p['available']]

        if available_providers:
            # Ordena por prioridade e falhas consecutivas
            available_providers.sort(key=lambda x: (x[1]['priority'], x[1]['consecutive_failures']))
            return available_providers[0][0]

        return None

    def generate_analysis(self, prompt: str, model: str = None, context: Dict[str, Any] = None, **kwargs) -> str:
        """
        Método para compatibilidade - redireciona para generate_response
        
        Args:
            prompt: O texto do prompt
            model: Modelo específico (ignorado - usa sistema de fallback automático)
            context: Contexto adicional (dicionário)
            **kwargs: Argumentos adicionais incluindo modelo_preferido
        """
        # CORREÇÃO CRÍTICA: Trata todos os argumentos possíveis
        if context is None:
            context = {}
        
        # Combina context com kwargs, priorizando context
        combined_kwargs = {**kwargs, **context}
        
        # Remove argumentos que não são aceitos pelo generate_response
        # mas mantém compatibilidade com código existente
        modelo_preferido = combined_kwargs.pop('modelo_preferido', model)
        
        # Extrai argumentos válidos para generate_response
        max_tokens = combined_kwargs.get('max_tokens', 4000)
        temperature = combined_kwargs.get('temperature', 0.7)
        system_prompt = combined_kwargs.get('system_prompt')
        
        # Remove argumentos já extraídos
        remaining_kwargs = {k: v for k, v in combined_kwargs.items() 
                          if k not in ['max_tokens', 'temperature', 'system_prompt']}
        
        # Chama generate_response com os parâmetros necessários
        try:
            response_data = self.generate_response(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                system_prompt=system_prompt,
                **remaining_kwargs
            )

            if response_data and isinstance(response_data, dict) and response_data.get('success'):
                return response_data.get('content', '')
            elif isinstance(response_data, str):
                # Se retornou diretamente uma string
                return response_data
            else:
                # Retorna uma string de erro se a geração falhar
                error_msg = response_data.get('error', 'Falha desconhecida') if isinstance(response_data, dict) else 'Resposta inválida'
                logger.error(f"❌ Erro na geração: {error_msg}")
                return f"Erro na geração: {error_msg}"
        except Exception as e:
            logger.error(f"❌ Erro crítico em generate_analysis: {e}")
            return f"Erro crítico na geração: {str(e)}"

    def generate_response(
            self,
            prompt: str,
            max_tokens: int = 4000,
            temperature: float = 0.7,
            system_prompt: str = None,
            **kwargs
        ) -> Dict[str, Any]:
        """Gera resposta usando o modelo primário com fallback automático"""
        try:
            # Validação de entrada
            if not prompt or not isinstance(prompt, str):
                return {
                    'success': False,
                    'error': 'Prompt inválido ou vazio',
                    'content': 'Erro: prompt inválido'
                }
            
            # Usa o Gemini como modelo primário
            if self.providers.get('gemini', {}).get('available'):
                try:
                    client = self.providers['gemini']['client']
                    
                    # Constrói o prompt completo se system_prompt for fornecido
                    full_prompt = prompt
                    if system_prompt:
                        full_prompt = f"{system_prompt}\n\n{prompt}"
                    
                    response = client.generate_content(
                        full_prompt, 
                        generation_config={
                            "temperature": temperature, 
                            "max_output_tokens": min(max_tokens, 8192)
                        },
                        safety_settings=[
                            {"category": c, "threshold": "BLOCK_NONE"} 
                            for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                                    "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]
                        ]
                    )

                    # Extrai texto de forma robusta
                    content = self._extract_text_from_gemini_response(response)
                    if content and content != "Erro na extração" and len(content.strip()) > 0:
                        self._record_success('gemini')
                        return {
                            'success': True,
                            'content': content,
                            'provider': 'gemini',
                            'error': None
                        }
                    else:
                        raise Exception("Resposta vazia ou inválida do Gemini")

                except Exception as e:
                    logger.warning(f"⚠️ Gemini falhou: {e}")
                    self._record_failure('gemini', str(e))

            # Fallback para outros modelos
            fallback_order = ['groq', 'openai', 'huggingface']

            for provider_name in fallback_order:
                provider_info = self.providers.get(provider_name)
                if provider_info and provider_info.get('available') and provider_info.get('client'):
                    try:
                        content = self._call_provider(provider_name, prompt, max_tokens, system_prompt)
                        if content and len(content.strip()) > 0:
                            self._record_success(provider_name)
                            return {
                                'success': True,
                                'content': content,
                                'provider': provider_name,
                                'error': None
                            }
                    except Exception as e:
                        logger.warning(f"⚠️ {provider_name} falhou: {e}")
                        self._record_failure(provider_name, str(e))
                        continue

            raise Exception("Todos os provedores de IA falharam")

        except Exception as e:
            logger.error(f"❌ Erro crítico no AI Manager: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': f'Erro na geração de resposta: {str(e)}'
            }

    def _call_provider(self, provider_name: str, prompt: str, max_tokens: int, system_prompt: str = None) -> Optional[str]:
        """Chama a função de geração do provedor especificado."""
        if provider_name == 'gemini':
            return self._generate_with_gemini(prompt, max_tokens, system_prompt)
        elif provider_name == 'groq':
            return self._generate_with_groq(prompt, max_tokens, system_prompt)
        elif provider_name == 'openai':
            return self._generate_with_openai(prompt, max_tokens, system_prompt)
        elif provider_name == 'huggingface':
            return self._generate_with_huggingface(prompt, max_tokens)
        return None

    def _generate_with_gemini(self, prompt: str, max_tokens: int, system_prompt: str = None) -> Optional[str]:
        """Gera conteúdo usando Gemini."""
        client = self.providers['gemini']['client']
        
        # Constrói o prompt completo se system_prompt for fornecido
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        config = {
            "temperature": 0.8,
            "max_output_tokens": min(max_tokens, 8192),
            "top_p": 0.95,
            "top_k": 64
        }
        safety = [
            {"category": c, "threshold": "BLOCK_NONE"} 
            for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                     "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]
        ]
        try:
            response = client.generate_content(full_prompt, generation_config=config, safety_settings=safety)
            content = self._extract_text_from_gemini_response(response)

            if content and "Erro na extração" not in content and len(content.strip()) > 0:
                logger.info(f"✅ Gemini 2.5 Pro gerou {len(content)} caracteres")
                return content
            elif "Erro na extração" in content:
                raise Exception(content)
            else:
                raise Exception("Resposta vazia do Gemini 2.5 Pro")
        except Exception as e:
            logger.error(f"❌ Falha ao gerar com Gemini: {e}")
            raise e

    def _extract_text_from_gemini_response(self, response) -> str:
        """Extrai texto da resposta do Gemini tratando diferentes formatos"""
        try:
            # Primeiro verifica se é uma resposta simples
            if hasattr(response, 'text') and response.text:
                try:
                    text_content = response.text
                    if text_content and isinstance(text_content, str) and len(text_content.strip()) > 0:
                        return text_content.strip()
                except Exception:
                    pass

            # Método robusto para respostas com múltiplas partes
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        if hasattr(candidate.content, 'parts') and candidate.content.parts:
                            text_parts = []
                            for part in candidate.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    text_parts.append(str(part.text).strip())
                            if text_parts:
                                combined_text = ' '.join(text_parts)
                                if combined_text.strip():
                                    return combined_text.strip()

            # Tenta acessar via parts diretamente no response
            if hasattr(response, 'parts') and response.parts:
                text_parts = []
                for part in response.parts:
                    if hasattr(part, 'text') and part.text:
                        text_parts.append(str(part.text).strip())
                if text_parts:
                    return ' '.join(text_parts).strip()

            # Fallback para responses que têm _result
            if hasattr(response, '_result') and response._result:
                return self._extract_text_from_gemini_response(response._result)

            logger.warning("Resposta Gemini não contém texto válido")
            return "Resposta gerada mas sem conteúdo textual acessível"

        except Exception as e:
            logger.error(f"❌ Erro crítico ao extrair texto da resposta Gemini: {e}")
            return f"Erro na extração: conteúdo gerado mas inacessível ({str(e)[:100]})"

    def _generate_with_groq(self, prompt: str, max_tokens: int, system_prompt: str = None) -> Optional[str]:
        """Gera conteúdo usando Groq."""
        client = self.providers['groq']['client']
        
        # Constrói o prompt completo se system_prompt for fornecido
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        content = client.generate(full_prompt, max_tokens=min(max_tokens, 8192))
        if content and len(content.strip()) > 0:
            logger.info(f"✅ Groq gerou {len(content)} caracteres")
            return content
        raise Exception("Resposta vazia do Groq")

    def _generate_with_openai(self, prompt: str, max_tokens: int, system_prompt: str = None) -> Optional[str]:
        """Gera conteúdo usando OpenAI."""
        client = self.providers['openai']['client']
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({"role": "system", "content": "Você é um especialista em análise de mercado ultra-detalhada."})
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=self.providers['openai']['model'],
            messages=messages,
            max_tokens=min(max_tokens, 4096),
            temperature=0.7
        )
        content = response.choices[0].message.content
        if content and len(content.strip()) > 0:
            logger.info(f"✅ OpenAI gerou {len(content)} caracteres")
            return content
        raise Exception("Resposta vazia do OpenAI")

    def _generate_with_huggingface(self, prompt: str, max_tokens: int) -> Optional[str]:
        """Gera conteúdo usando HuggingFace com rotação de modelos."""
        config = self.providers['huggingface']
        for _ in range(len(config['models'])):
            model_index = config['current_model_index']
            model = config['models'][model_index]
            config['current_model_index'] = (model_index + 1) % len(config['models'])

            try:
                url = f"{config['client']['base_url']}{model}"
                headers = {"Authorization": f"Bearer {config['client']['api_key']}"}
                payload = {"inputs": prompt, "parameters": {"max_new_tokens": min(max_tokens, 1024)}}
                response = requests.post(url, headers=headers, json=payload, timeout=60)

                if response.status_code == 200:
                    res_json = response.json()
                    if isinstance(res_json, list) and len(res_json) > 0:
                        content = res_json[0].get("generated_text", "")
                        if content and len(content.strip()) > 0:
                            logger.info(f"✅ HuggingFace ({model}) gerou {len(content)} caracteres")
                            return content
                elif response.status_code == 503:
                    logger.warning(f"⚠️ Modelo HuggingFace {model} está carregando (503), tentando próximo...")
                    continue
                else:
                    logger.warning(f"⚠️ Erro {response.status_code} no modelo {model}")
                    continue
            except Exception as e:
                logger.warning(f"⚠️ Erro no modelo {model}: {e}")
                continue
        raise Exception("Todos os modelos HuggingFace falharam")

    def reset_provider_errors(self, provider_name: str = None):
        """Reset contadores de erro dos provedores"""
        if provider_name:
            if provider_name in self.providers:
                self.providers[provider_name]['error_count'] = 0
                self.providers[provider_name]['consecutive_failures'] = 0
                self.providers[provider_name]['available'] = True
                logger.info(f"🔄 Reset erros do provedor: {provider_name}")
        else:
            for provider in self.providers.values():
                provider['error_count'] = 0
                provider['consecutive_failures'] = 0
                if provider.get('client'):
                    provider['available'] = True
            logger.info("🔄 Reset erros de todos os provedores")

    def _record_failure(self, provider_name: str, error_message: str):
        """Registra falha de um provedor"""
        if provider_name in self.providers:
            provider = self.providers[provider_name]
            provider['error_count'] += 1
            provider['consecutive_failures'] += 1

            # Desabilita provedor se exceder limite de erros
            if provider['consecutive_failures'] >= provider.get('max_errors', 2):
                provider['available'] = False
                logger.warning(f"⚠️ Provedor {provider_name} desabilitado após {provider['consecutive_failures']} falhas consecutivas")

    def _record_success(self, provider_name: str):
        """Registra sucesso de um provedor"""
        if provider_name in self.providers:
            provider = self.providers[provider_name]
            provider['consecutive_failures'] = 0
            provider['last_success'] = time.time()
            if not provider['available']:
                provider['available'] = True
                logger.info(f"✅ Provedor {provider_name} reabilitado após sucesso")

    def get_provider_status(self) -> Dict[str, Any]:
        """Retorna status detalhado dos provedores"""
        status = {}

        for name, provider in self.providers.items():
            status[name] = {
                'available': provider['available'],
                'priority': provider['priority'],
                'error_count': provider['error_count'],
                'consecutive_failures': provider['consecutive_failures'],
                'last_success': provider.get('last_success'),
                'max_errors': provider['max_errors'],
                'model': provider.get('model', 'N/A'),
                'enabled': provider.get('enabled', True)
            }

        return status

    def generate_content(self, prompt: str, max_tokens: int = 1000, **kwargs) -> Optional[str]:
        """Método alias para compatibilidade"""
        return self.generate_analysis(prompt, context={'max_tokens': max_tokens, **kwargs})

    def gerar_resposta_inteligente(self, prompt: str, modelo_preferido: str = 'gemini', max_tentativas: int = 2) -> Dict[str, Any]:
        """Método compatível com o Mental Drivers Architect"""
        try:
            # Validação de entrada
            if not prompt or not isinstance(prompt, str):
                return {
                    'error': 'Prompt inválido ou vazio',
                    'success': False
                }
            
            response_data = self.generate_response(
                prompt=prompt, 
                max_tokens=4000, 
                temperature=0.7
            )

            if response_data and isinstance(response_data, dict) and response_data.get('success'):
                return {
                    'response': response_data.get('content', ''),
                    'modelo_usado': response_data.get('provider', modelo_preferido),
                    'success': True
                }
            elif isinstance(response_data, str):
                # Se retornou diretamente uma string
                return {
                    'response': response_data,
                    'modelo_usado': modelo_preferido,
                    'success': True
                }
            else:
                error_msg = response_data.get('error', 'Falha desconhecida na geração') if isinstance(response_data, dict) else 'Resposta inválida'
                return {
                    'error': error_msg,
                    'success': False
                }

        except Exception as e:
            logger.error(f"❌ Erro em gerar_resposta_inteligente: {e}")
            return {
                'error': str(e),
                'success': False
            }


# Instância global
ai_manager = AIManager()
