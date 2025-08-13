
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Service Health Checker
Verifica integridade de todos os serviços do sistema
"""

import logging
import traceback
from typing import Dict, List, Any, Tuple

logger = logging.getLogger(__name__)

class ServiceHealthChecker:
    """Verificador de saúde dos serviços do sistema"""

    def __init__(self):
        self.services_status = {}
        self.critical_services = ['ai_manager', 'auto_save_manager']
        self.optional_services = [
            'enhanced_search_coordinator',
            'production_search_manager',
            'mental_drivers_architect',
            'visual_proofs_generator',
            'anti_objection_system',
            'pre_pitch_architect',
            'future_prediction_engine',
            'mcp_supadata_manager',
            'alibaba_websailor',
            'enhanced_report_generator'
        ]

    def check_all_services(self) -> Dict[str, Any]:
        """Verifica todos os serviços do sistema"""
        results = {
            'overall_health': 'healthy',
            'critical_services': {},
            'optional_services': {},
            'import_errors': [],
            'runtime_errors': [],
            'recommendations': []
        }

        # Verifica serviços críticos
        critical_ok = 0
        for service_name in self.critical_services:
            status, error = self._check_service_import(service_name)
            results['critical_services'][service_name] = {
                'status': status,
                'error': error
            }
            if status == 'ok':
                critical_ok += 1
            else:
                results['import_errors'].append(f"CRÍTICO: {service_name} - {error}")

        # Verifica serviços opcionais
        optional_ok = 0
        for service_name in self.optional_services:
            status, error = self._check_service_import(service_name)
            results['optional_services'][service_name] = {
                'status': status,
                'error': error
            }
            if status == 'ok':
                optional_ok += 1
            else:
                results['import_errors'].append(f"OPCIONAL: {service_name} - {error}")

        # Determina saúde geral
        if critical_ok < len(self.critical_services):
            results['overall_health'] = 'critical'
            results['recommendations'].append("Serviços críticos com falha - sistema pode não funcionar")
        elif critical_ok == len(self.critical_services) and optional_ok < len(self.optional_services) * 0.7:
            results['overall_health'] = 'degraded'
            results['recommendations'].append("Muitos serviços opcionais indisponíveis - funcionalidade limitada")
        else:
            results['overall_health'] = 'healthy'

        # Testa funcionalidades básicas
        runtime_tests = self._run_runtime_tests()
        results['runtime_tests'] = runtime_tests
        
        return results

    def _check_service_import(self, service_name: str) -> Tuple[str, str]:
        """Verifica se um serviço pode ser importado"""
        try:
            if service_name == 'ai_manager':
                from services.ai_manager import ai_manager
                if ai_manager:
                    return 'ok', ''
                else:
                    return 'error', 'Service is None after import'

            elif service_name == 'auto_save_manager':
                from services.auto_save_manager import salvar_etapa, salvar_erro
                return 'ok', ''

            elif service_name == 'enhanced_search_coordinator':
                from services.enhanced_search_coordinator import enhanced_search_coordinator
                return 'ok', ''

            elif service_name == 'production_search_manager':
                from services.production_search_manager import production_search_manager
                return 'ok', ''

            elif service_name == 'mental_drivers_architect':
                from services.mental_drivers_architect import mental_drivers_architect
                return 'ok', ''

            elif service_name == 'visual_proofs_generator':
                from services.visual_proofs_generator import visual_proofs_generator
                return 'ok', ''

            elif service_name == 'anti_objection_system':
                from services.anti_objection_system import AntiObjectionSystem
                return 'ok', ''

            elif service_name == 'pre_pitch_architect':
                from services.pre_pitch_architect import pre_pitch_architect
                return 'ok', ''

            elif service_name == 'future_prediction_engine':
                from services.future_prediction_engine import future_prediction_engine
                return 'ok', ''

            elif service_name == 'mcp_supadata_manager':
                from services.mcp_supadata_manager import mcp_supadata_manager
                return 'ok', ''

            elif service_name == 'alibaba_websailor':
                from services.alibaba_websailor import AlibabaWebSailorAgent
                return 'ok', ''

            elif service_name == 'enhanced_report_generator':
                from services.enhanced_report_generator import enhanced_report_generator
                return 'ok', ''

            else:
                return 'error', f'Unknown service: {service_name}'

        except ImportError as e:
            return 'import_error', str(e)
        except Exception as e:
            return 'error', str(e)

    def _run_runtime_tests(self) -> Dict[str, Any]:
        """Executa testes básicos de funcionalidade"""
        tests = {
            'ai_manager_basic': self._test_ai_manager(),
            'auto_save_basic': self._test_auto_save(),
            'super_orchestrator_init': self._test_super_orchestrator()
        }
        return tests

    def _test_ai_manager(self) -> Dict[str, Any]:
        """Testa funcionalidade básica do AI Manager"""
        try:
            from services.ai_manager import ai_manager
            if ai_manager:
                # Teste básico - não executa uma requisição real
                return {'status': 'ok', 'message': 'AI Manager available'}
            else:
                return {'status': 'error', 'message': 'AI Manager is None'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def _test_auto_save(self) -> Dict[str, Any]:
        """Testa funcionalidade básica do Auto Save"""
        try:
            from services.auto_save_manager import salvar_etapa
            # Teste básico sem salvar arquivo real
            return {'status': 'ok', 'message': 'Auto Save functions available'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def _test_super_orchestrator(self) -> Dict[str, Any]:
        """Testa inicialização do Super Orchestrator"""
        try:
            from services.super_orchestrator import super_orchestrator
            if super_orchestrator:
                return {'status': 'ok', 'message': 'Super Orchestrator initialized'}
            else:
                return {'status': 'error', 'message': 'Super Orchestrator is None'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def generate_health_report(self) -> str:
        """Gera relatório de saúde em formato texto"""
        health_data = self.check_all_services()
        
        report = []
        report.append("=" * 60)
        report.append("RELATÓRIO DE SAÚDE DO SISTEMA ARQV30")
        report.append("=" * 60)
        report.append(f"Status Geral: {health_data['overall_health'].upper()}")
        report.append("")

        # Serviços críticos
        report.append("SERVIÇOS CRÍTICOS:")
        for service, status in health_data['critical_services'].items():
            status_icon = "✅" if status['status'] == 'ok' else "❌"
            report.append(f"  {status_icon} {service}: {status['status']}")
            if status['error']:
                report.append(f"      Erro: {status['error']}")

        report.append("")

        # Serviços opcionais
        report.append("SERVIÇOS OPCIONAIS:")
        for service, status in health_data['optional_services'].items():
            status_icon = "✅" if status['status'] == 'ok' else "⚠️"
            report.append(f"  {status_icon} {service}: {status['status']}")

        report.append("")

        # Testes de runtime
        report.append("TESTES DE FUNCIONALIDADE:")
        for test_name, result in health_data['runtime_tests'].items():
            status_icon = "✅" if result['status'] == 'ok' else "❌"
            report.append(f"  {status_icon} {test_name}: {result['status']}")
            if result.get('message'):
                report.append(f"      {result['message']}")

        # Recomendações
        if health_data['recommendations']:
            report.append("")
            report.append("RECOMENDAÇÕES:")
            for rec in health_data['recommendations']:
                report.append(f"  • {rec}")

        report.append("")
        report.append("=" * 60)

        return "\n".join(report)


# Instância global
service_health_checker = ServiceHealthChecker()

def run_health_check():
    """Executa verificação de saúde e imprime resultado"""
    print(service_health_checker.generate_health_report())

if __name__ == '__main__':
    run_health_check()
