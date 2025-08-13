#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Code Cleanup Manager
Sistema para identificar e remover código desnecessário
"""

import os
import logging
import re
import ast
from typing import Dict, List, Any, Set, Tuple
from pathlib import Path
from datetime import datetime
from services.auto_save_manager import salvar_etapa

logger = logging.getLogger(__name__)

class CodeCleanupManager:
    """Gerenciador de limpeza de código"""

    def __init__(self):
        """Inicializa o gerenciador de limpeza"""
        self.project_root = Path("src")
        self.disposable_patterns = [
            r'# TODO.*',
            r'# FIXME.*',
            r'# XXX.*',
            r'print\s*\([^)]*debug[^)]*\)',
            r'console\.log\s*\([^)]*\)',
            r'import\s+pdb.*',
            r'pdb\.set_trace\(\)',
            r'debugger;',
            r'\/\*.*test.*\*\/',
            r'#.*test.*placeholder.*',
            r'#.*mock.*data.*',
            r'#.*temporary.*',
            r'#.*hardcoded.*',
            r'if\s+False\s*:',
            r'if\s+0\s*:',
            r'pass\s*#.*'
        ]

        self.unused_imports = set()
        self.dead_code_blocks = []
        self.disposable_files = []

        logger.info("🧹 Code Cleanup Manager inicializado")

    def analyze_codebase(self, session_id: str) -> Dict[str, Any]:
        """Analisa a base de código para identificar itens descartáveis"""

        try:
            logger.info("🔍 Analisando base de código para limpeza...")

            analysis_results = {
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'disposable_files': [],
                'unused_imports': [],
                'dead_code_blocks': [],
                'hardcoded_values': [],
                'debug_statements': [],
                'mock_placeholders': [],
                'temporary_code': [],
                'duplicate_code': [],
                'cleanup_summary': {}
            }

            # Analisa todos os arquivos Python
            python_files = list(self.project_root.rglob("*.py"))

            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Analisa arquivo específico
                    file_analysis = self._analyze_file(file_path, content)

                    # Adiciona resultados ao análise geral
                    if file_analysis['is_disposable']:
                        analysis_results['disposable_files'].append({
                            'path': str(file_path),
                            'reason': file_analysis['disposable_reason'],
                            'size_bytes': len(content),
                            'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        })

                    analysis_results['unused_imports'].extend(file_analysis['unused_imports'])
                    analysis_results['dead_code_blocks'].extend(file_analysis['dead_code'])
                    analysis_results['hardcoded_values'].extend(file_analysis['hardcoded_values'])
                    analysis_results['debug_statements'].extend(file_analysis['debug_statements'])
                    analysis_results['mock_placeholders'].extend(file_analysis['mock_placeholders'])
                    analysis_results['temporary_code'].extend(file_analysis['temporary_code'])

                except Exception as e:
                    logger.warning(f"Erro ao analisar {file_path}: {e}")
                    continue

            # Identifica código duplicado
            analysis_results['duplicate_code'] = self._find_duplicate_code(python_files)

            # Gera resumo da limpeza
            analysis_results['cleanup_summary'] = self._generate_cleanup_summary(analysis_results)

            # Salva análise
            salvar_etapa(
                "code_cleanup_analysis",
                analysis_results,
                session_id=session_id,
                categoria="code_cleanup"
            )

            logger.info(f"✅ Análise de limpeza concluída: {len(analysis_results['disposable_files'])} arquivos descartáveis encontrados")
            return analysis_results

        except Exception as e:
            logger.error(f"❌ Erro na análise de limpeza: {e}")
            return {
                'session_id': session_id,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _analyze_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analisa um arquivo específico"""

        analysis = {
            'file_path': str(file_path),
            'is_disposable': False,
            'disposable_reason': '',
            'unused_imports': [],
            'dead_code': [],
            'hardcoded_values': [],
            'debug_statements': [],
            'mock_placeholders': [],
            'temporary_code': []
        }

        try:
            # Verifica se é arquivo de teste ou backup
            file_name = file_path.name.lower()
            if any(pattern in file_name for pattern in ['test_', '_test', 'backup', 'copy', 'temp', 'tmp', 'old']):
                analysis['is_disposable'] = True
                analysis['disposable_reason'] = f"Arquivo de teste/backup/temporário: {file_name}"

            # Verifica se é arquivo vazio ou só comentários
            content_lines = [line.strip() for line in content.split('\n') if line.strip()]
            code_lines = [line for line in content_lines if not line.startswith('#') and not line.startswith('"""') and not line.startswith("'''")]

            if len(code_lines) < 5:
                analysis['is_disposable'] = True
                analysis['disposable_reason'] = f"Arquivo muito pequeno ou vazio: {len(code_lines)} linhas de código"

            # Procura por padrões específicos
            lines = content.split('\n')
            for i, line in enumerate(lines):
                line_stripped = line.strip()

                # Debug statements
                if any(pattern in line_stripped.lower() for pattern in ['print(', 'console.log', 'pdb.set_trace', 'debugger']):
                    if 'debug' in line_stripped.lower() or 'test' in line_stripped.lower():
                        analysis['debug_statements'].append({
                            'line_number': i + 1,
                            'content': line_stripped,
                            'file': str(file_path)
                        })

                # Mock/placeholder code
                if any(pattern in line_stripped.lower() for pattern in ['mock', 'placeholder', 'todo', 'fixme', 'hardcoded']):
                    analysis['mock_placeholders'].append({
                        'line_number': i + 1,
                        'content': line_stripped,
                        'file': str(file_path)
                    })

                # Temporary code
                if any(pattern in line_stripped.lower() for pattern in ['temporary', 'temp', 'delete me', 'remove this']):
                    analysis['temporary_code'].append({
                        'line_number': i + 1,
                        'content': line_stripped,
                        'file': str(file_path)
                    })

                # Hardcoded values (strings/números suspeitos)
                hardcoded_patterns = [
                    r'api_key\s*=\s*["\'][^"\']{20,}["\']',
                    r'password\s*=\s*["\'][^"\']+["\']',
                    r'secret\s*=\s*["\'][^"\']+["\']',
                    r'token\s*=\s*["\'][^"\']{20,}["\']'
                ]

                for pattern in hardcoded_patterns:
                    if re.search(pattern, line_stripped, re.IGNORECASE):
                        analysis['hardcoded_values'].append({
                            'line_number': i + 1,
                            'content': line_stripped[:50] + "...",
                            'file': str(file_path),
                            'type': 'sensitive_data'
                        })

            # Analisa imports não utilizados (análise básica)
            try:
                tree = ast.parse(content)
                imports = []
                used_names = set()

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.Name):
                        used_names.add(node.id)

                # Identifica imports não utilizados
                for imp in imports:
                    if imp not in used_names and imp not in ['sys', 'os', 'logging']:
                        analysis['unused_imports'].append({
                            'import': imp,
                            'file': str(file_path)
                        })

            except Exception as e:
                logger.debug(f"Erro na análise AST de {file_path}: {e}")

        except Exception as e:
            logger.warning(f"Erro na análise detalhada de {file_path}: {e}")

        return analysis

    def _find_duplicate_code(self, python_files: List[Path]) -> List[Dict[str, Any]]:
        """Encontra código duplicado"""

        duplicates = []

        try:
            code_blocks = {}

            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Divide em blocos de função/classe
                    tree = ast.parse(content)

                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                            # Extrai o código do nó
                            start_line = node.lineno - 1
                            end_line = getattr(node, 'end_lineno', start_line + 10) if hasattr(node, 'end_lineno') else start_line + 10

                            lines = content.split('\n')[start_line:end_line]
                            block_content = '\n'.join(lines)

                            # Normaliza o conteúdo (remove espaços extras)
                            normalized = re.sub(r'\s+', ' ', block_content).strip()

                            if len(normalized) > 100:  # Só analisa blocos significativos
                                if normalized in code_blocks:
                                    duplicates.append({
                                        'content_preview': normalized[:100] + "...",
                                        'files': [code_blocks[normalized], str(file_path)],
                                        'block_type': type(node).__name__,
                                        'estimated_lines': len(lines)
                                    })
                                else:
                                    code_blocks[normalized] = str(file_path)

                except Exception as e:
                    logger.debug(f"Erro ao analisar duplicatas em {file_path}: {e}")
                    continue

        except Exception as e:
            logger.warning(f"Erro na busca por código duplicado: {e}")

        return duplicates[:20]  # Limita a 20 duplicatas

    def _generate_cleanup_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Gera resumo da limpeza"""

        summary = {
            'total_disposable_files': len(analysis_results.get('disposable_files', [])),
            'total_unused_imports': len(analysis_results.get('unused_imports', [])),
            'total_debug_statements': len(analysis_results.get('debug_statements', [])),
            'total_mock_placeholders': len(analysis_results.get('mock_placeholders', [])),
            'total_hardcoded_values': len(analysis_results.get('hardcoded_values', [])),
            'total_duplicate_blocks': len(analysis_results.get('duplicate_code', [])),
            'estimated_cleanup_impact': {},
            'recommended_actions': []
        }

        # Calcula impacto estimado
        disposable_size = sum(file.get('size_bytes', 0) for file in analysis_results.get('disposable_files', []))
        summary['estimated_cleanup_impact'] = {
            'files_to_remove': summary['total_disposable_files'],
            'bytes_to_save': disposable_size,
            'kb_to_save': round(disposable_size / 1024, 2),
            'estimated_performance_gain': min(100, summary['total_unused_imports'] * 2),
            'code_maintainability_improvement': min(100, (summary['total_mock_placeholders'] + summary['total_debug_statements']) * 3)
        }

        # Gera recomendações
        if summary['total_disposable_files'] > 0:
            summary['recommended_actions'].append(f"Remover {summary['total_disposable_files']} arquivos descartáveis")

        if summary['total_unused_imports'] > 5:
            summary['recommended_actions'].append(f"Limpar {summary['total_unused_imports']} imports não utilizados")

        if summary['total_debug_statements'] > 0:
            summary['recommended_actions'].append(f"Remover {summary['total_debug_statements']} declarações de debug")

        if summary['total_hardcoded_values'] > 0:
            summary['recommended_actions'].append(f"Mover {summary['total_hardcoded_values']} valores hardcoded para configuração")

        if summary['total_duplicate_blocks'] > 0:
            summary['recommended_actions'].append(f"Refatorar {summary['total_duplicate_blocks']} blocos de código duplicado")

        return summary

    def execute_safe_cleanup(self, analysis_results: Dict[str, Any], session_id: str, dry_run: bool = True) -> Dict[str, Any]:
        """Executa limpeza segura do código"""

        try:
            logger.info(f"🧹 Executando limpeza {'(simulação)' if dry_run else '(real)'}...")

            cleanup_results = {
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'dry_run': dry_run,
                'actions_taken': [],
                'files_processed': 0,
                'cleanup_summary': {}
            }

            # Lista arquivos para remoção
            disposable_files = analysis_results.get('disposable_files', [])

            if disposable_files:
                logger.info(f"📋 ARQUIVOS MARCADOS PARA REMOÇÃO ({len(disposable_files)} itens):")
                for file_info in disposable_files:
                    logger.info(f"   - {file_info['path']} ({file_info['reason']})")

                    if not dry_run:
                        try:
                            file_path = Path(file_info['path'])
                            if file_path.exists():
                                # Move para pasta de backup antes de remover
                                backup_dir = Path("backup_removed_files")
                                backup_dir.mkdir(exist_ok=True)

                                backup_path = backup_dir / file_path.name
                                file_path.rename(backup_path)

                                cleanup_results['actions_taken'].append(f"Movido para backup: {file_info['path']}")
                                cleanup_results['files_processed'] += 1
                        except Exception as e:
                            logger.error(f"Erro ao processar {file_info['path']}: {e}")

            # Remove debug statements (apenas em dry_run por segurança)
            debug_statements = analysis_results.get('debug_statements', [])
            if debug_statements and dry_run:
                logger.info(f"🐛 DEBUG STATEMENTS ENCONTRADOS ({len(debug_statements)} itens):")
                for debug_info in debug_statements[:10]:  # Mostra apenas os primeiros 10
                    logger.info(f"   - {debug_info['file']}:{debug_info['line_number']} - {debug_info['content'][:50]}...")

            cleanup_results['cleanup_summary'] = {
                'disposable_files_processed': len(disposable_files),
                'debug_statements_found': len(debug_statements),
                'total_actions_planned': len(disposable_files) + len(debug_statements),
                'actions_executed': cleanup_results['files_processed']
            }

            # Salva resultados da limpeza
            salvar_etapa(
                "code_cleanup_execution",
                cleanup_results,
                session_id=session_id,
                categoria="code_cleanup"
            )

            logger.info(f"✅ Limpeza {'simulada' if dry_run else 'executada'} - {cleanup_results['files_processed']} arquivos processados")
            return cleanup_results

        except Exception as e:
            logger.error(f"❌ Erro na limpeza: {e}")
            return {
                'session_id': session_id,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _list_removable_files(self) -> List[Path]:
        """Lista todos os arquivos que são considerados removíveis"""
        removable_files = []
        try:
            # Adiciona padrões de nomenclatura de arquivos para considerar como removíveis
            disposable_file_patterns = ['test_', '_test', 'backup', 'copy', 'temp', 'tmp', 'old', '.pyc', '.log', '__pycache__']
            
            for pattern in disposable_file_patterns:
                # Procura por arquivos que correspondem aos padrões em todo o diretório do projeto
                removable_files.extend(self.project_root.rglob(f'*{pattern}*'))
                
                # Remove duplicatas
                removable_files = list(set(removable_files))

        except Exception as e:
            logger.warning(f"Erro ao listar arquivos removíveis: {e}")
        return removable_files

    def cleanup_temporary_files(self) -> Dict[str, Any]:
        """Remove arquivos temporários e desnecessários - LISTA ANTES DE REMOVER"""

        try:
            logger.info("🧹 Iniciando limpeza de arquivos temporários...")

            # LISTA TODOS OS ARQUIVOS ANTES DE REMOVER
            files_to_remove = self._list_removable_files()

            logger.info(f"📋 Arquivos identificados para remoção:")
            for file_path in files_to_remove:
                logger.info(f"  🗑️ {file_path}")

            # Confirma antes de remover
            if len(files_to_remove) > 0:
                logger.info(f"⚠️ {len(files_to_remove)} arquivos serão removidos...")

            cleanup_stats = {
                'files_to_remove': files_to_remove,
                'files_removed': 0,
                'space_freed': 0,
                'categories_cleaned': []
            }
            
            # Realiza a remoção dos arquivos
            for file_path in files_to_remove:
                try:
                    if file_path.is_file():
                        file_size = file_path.stat().st_size
                        file_path.unlink()
                        cleanup_stats['files_removed'] += 1
                        cleanup_stats['space_freed'] += file_size
                        logger.info(f"  ✅ Removido: {file_path} ({file_size} bytes)")
                    elif file_path.is_dir():
                        # Pode adicionar lógica para remover diretórios vazios se necessário
                        pass
                except Exception as e:
                    logger.warning(f"Erro ao remover {file_path}: {e}")

            # Calcula o espaço liberado em KB e MB
            cleanup_stats['space_freed_kb'] = round(cleanup_stats['space_freed'] / 1024, 2)
            cleanup_stats['space_freed_mb'] = round(cleanup_stats['space_freed'] / (1024 * 1024), 2)

            logger.info(f"✅ Limpeza de arquivos temporários concluída. {cleanup_stats['files_removed']} arquivos removidos, {cleanup_stats['space_freed_kb']:.2f} KB liberados.")

            return cleanup_stats

        except Exception as e:
            logger.error(f"❌ Erro na limpeza de arquivos temporários: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }


# Instância global
code_cleanup_manager = CodeCleanupManager()