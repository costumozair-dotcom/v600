#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Aplicação Principal
Servidor Flask para análise de mercado ultra-detalhada
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_cors import CORS

# CONFIGURAÇÃO DE PRODUÇÃO
os.environ["FLASK_ENV"] = "production"
os.environ["DEBUG"] = "False"
os.environ["FORCE_REAL_DATA"] = "True"
os.environ["DISABLE_FALLBACKS"] = "True"
os.environ["RESILIENT_MODE"] = "True"
os.environ["ULTRA_DETAILED_MODE"] = "True"

# Adiciona src ao path se necessário
if "src" not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configuração de logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/arqv30.log", encoding="utf-8")
    ]
)

logger = logging.getLogger(__name__)

def create_app():
    """Cria e configura a aplicação Flask"""

    # Carrega variáveis de ambiente
    from services.environment_loader import environment_loader

    app = Flask(__name__)

    # CONFIGURAÇÃO CRÍTICA DE PRODUÇÃO - ULTRA SEGURA
    # Força ambiente de produção - NUNCA debug em produção
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    debug = False  # SEMPRE False em produção - HARDCODED
    app.config["DEBUG"] = False  # FORÇA False
    app.config["TESTING"] = False
    app.config["PRODUCTION"] = True
    
    # Remove qualquer possibilidade de debug
    os.environ["FLASK_DEBUG"] = "0"
    os.environ["WERKZEUG_DEBUG_PIN"] = "off"

    # Configuração de logging OTIMIZADA para produção
    if FLASK_ENV == "production":
        # Logging WARNING em produção para performance
        logging.basicConfig(
            level=logging.WARNING,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("logs/production.log", encoding="utf-8")
            ]
        )
        # Remove logs verbosos
        logging.getLogger("urllib3").setLevel(logging.ERROR)
        logging.getLogger("requests").setLevel(logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)

    # Configuração CORS para produção
    cors_origins = os.getenv("CORS_ORIGINS", "*")
    if FLASK_ENV == "production" and cors_origins == "*":
        # Em produção, CORS deve ser restritivo
        cors_origins = ["https://yourdomain.com"]  # Configurar domínio real

    CORS(app, resources={
        r"/api/*": {
            "origins": cors_origins.split(",") if isinstance(cors_origins, str) else cors_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Chave secreta ULTRA SEGURA carregada do ambiente
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key and FLASK_ENV == "production":
        raise ValueError("SECRET_KEY OBRIGATÓRIA em produção - Configure nas variáveis de ambiente")
    
    app.secret_key = secret_key or "arqv30-enhanced-ultra-secure-key-2024"
    
    # Valida chaves críticas em produção
    if FLASK_ENV == "production":
        required_keys = ["GEMINI_API_KEY", "OPENAI_API_KEY", "GROQ_API_KEY"]
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        if missing_keys:
            logger.warning(f"Chaves API ausentes em produção: {missing_keys}")
            # Não falha, mas avisa - permite fallbacks

    # Registrar rotas
    from routes.analysis import analysis_bp
    from routes.enhanced_analysis import enhanced_analysis_bp
    from routes.progress import progress_bp
    from routes.user import user_bp
    from routes.files import files_bp
    from routes.pdf_generator import pdf_bp
    from routes.forensic_analysis import forensic_bp
    from routes.monitoring import monitoring_bp
    from routes.html_report_generator import html_report_bp

    app.register_blueprint(analysis_bp, url_prefix="/api")
    app.register_blueprint(enhanced_analysis_bp, url_prefix="/api")
    app.register_blueprint(progress_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(files_bp, url_prefix="/api")
    app.register_blueprint(pdf_bp, url_prefix="/api")
    app.register_blueprint(forensic_bp, url_prefix="/api")
    app.register_blueprint(monitoring_bp, url_prefix="/api")
    app.register_blueprint(html_report_bp, url_prefix="/api")

    # Registrar rotas de debug
    try:
        from routes.debug import debug_bp
        app.register_blueprint(debug_bp)
        logger.info("✅ Rotas de debug registradas")
    except ImportError as e:
        logger.warning(f"⚠️ Erro ao registrar rotas de debug: {e}")

    @app.route("/")
    def index():
        """Página principal"""
        return render_template("enhanced_index.html")

    @app.route("/archaeological")
    def archaeological():
        """Interface arqueológica"""
        return render_template("enhanced_interface.html")

    @app.route("/forensic")
    def forensic():
        """Interface forense"""
        return render_template("forensic_interface.html")

    @app.route("/unified")
    def unified():
        """Interface unificada"""
        return render_template("unified_interface.html")

    @app.route("/api/app_status")
    def app_status():
        """Status da aplicação"""
        try:
            from services.ai_manager import ai_manager
            from services.production_search_manager import production_search_manager
            from database import db_manager

            ai_status = ai_manager.get_provider_status()
            search_status = production_search_manager.get_provider_status()
            db_status = db_manager.test_connection()

            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "2.0.0",
                "services": {
                    "ai_providers": {
                        "available": len([p for p in ai_status.values() if p["available"]]),
                        "total": len(ai_status),
                        "providers": ai_status
                    },
                    "search_providers": {
                        "available": len([p for p in search_status.values() if p["available"]]),
                        "total": len(search_status),
                        "providers": search_status
                    },
                    "database": {
                        "connected": db_status
                    }
                }
            })
        except Exception as e:
            logger.error(f"Error in app_status: {e}")
            return jsonify({
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint não encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({"error": "Erro interno do servidor"}), 500

    return app

def main():
    """Função principal"""

    print("🚀 ARQV30 Enhanced v2.0 - Iniciando aplicação...")

    try:
        # Cria aplicação
        app = create_app()

        # Configurações do servidor
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", 5000))
        debug = os.getenv("FLASK_ENV", "production") == "development" # This line is kept for clarity in main, but app.config["DEBUG"] is set in create_app

        print(f"🌐 Servidor: http://{host}:{port}")
        print(f"📊 Interface: Análise Ultra-Detalhada de Mercado")
        print(f"🤖 IA: Gemini 2.5 Pro + Groq + Fallbacks")
        print(f"🔍 Pesquisa: WebSailor + Google + Múltiplos Engines")
        print(f"💾 Banco: Supabase + Arquivos Locais")
        print(f"🛡️ Sistema: Ultra-Robusto com Salvamento Automático")

        print("\n" + "=" * 60)
        print("✅ ARQV30 Enhanced v2.0 PRONTO!")
        print("=" * 60)
        print("Pressione Ctrl+C para parar o servidor")
        print("=" * 60)

        # Inicia servidor
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )

    except KeyboardInterrupt:
        print("\n\n✅ Servidor encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        logger.critical(f"Critical error during server startup: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

