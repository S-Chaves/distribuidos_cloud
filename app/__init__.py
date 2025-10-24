from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
swagger = Swagger()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    swagger_config = {
        "securityDefinitions": {
            "bearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Token de acceso JWT. Escribe: **'Bearer {tu_token}'**"
            }
        }
    }
    app.config['SWAGGER'] = swagger_config
    swagger.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .routes import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    from .models import ONG, ProjectDefinition, WorkPlan, CoveragePlan, PedidoColaboracion, Compromiso
    
    from seed import seed_db_command
    app.cli.add_command(seed_db_command)

    return app