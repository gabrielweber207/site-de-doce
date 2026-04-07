from flask import Flask, session
import os
from models.db import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'docemagia_secret_key_2026' # Chave secreta para sessões

    # Garantir que o banco de dados seja inicializado
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'database.db')):
        init_db()

    # Registro de Blueprints
    from controllers.auth import auth_bp
    from controllers.shop import shop_bp
    from controllers.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(admin_bp)

    # Injetar o carrinho em todos os contextos de template
    @app.context_processor
    def inject_cart():
        return dict(session=session)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
