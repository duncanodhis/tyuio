from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import config
from flask_cors import CORS
from datetime import timedelta
import secrets
secret_key = secrets.token_hex(32)  # Generate a 256-bit (32-byte) key

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
from flask_jwt_extended import JWTManager
def create_app(config_name='default'):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Register blueprints
    from views.user_view import user_view
    from views.product_view import product_view
    from views.order_view import order_view
    from views.address_view import  address_view
    from views.dispute_view import dispute_view
    from views.newsletter_view import newsletter_view
    from views.review_view import review_view
    from views.payment_view import payment_view
    from views.customer_view import customer_view
    from views.statistics_view import statistics_view
    from views.category_view import category_view
    from views.package_view import package_view
    from routes.user_route import user_routes
    from routes.courier_route import courier_routes
    from routes.task_route import task_routes
    from routes.product_route import product_routes
    from routes.order_route import order_routes
    from routes.address_route import address_routes
    from routes.customer_route import customer_routes
    from routes.category_route import category_routes
    from routes.package_route import package_routes
    from routes.dispute_route import dispute_routes
    from routes.newsletter_route import newsletter_routes
    from routes.botmanagement_route import botmanagement_route
    from routes.payment_route import payment_routes
    from routes.review_route import review_routes
    from routes.statistics_route import statistics_routes
    from routes.bot_router import bot_routes
    from routes.treasure_route import treasure_routes
    from routes.metric_route import metric_routes
    app.register_blueprint(user_view)
    app.register_blueprint(product_view)
    app.register_blueprint(package_view)
    app.register_blueprint(order_view)
    app.register_blueprint(address_view)
    app.register_blueprint(customer_view)
    app.register_blueprint(dispute_view)
    app.register_blueprint(newsletter_view)
    app.register_blueprint(review_view)
    app.register_blueprint(payment_view)
    app.register_blueprint(statistics_view)
    app.register_blueprint(category_view)
    app.register_blueprint(user_routes)
    app.register_blueprint(product_routes)
    app.register_blueprint(task_routes)
    app.register_blueprint(package_routes)
    app.register_blueprint(order_routes)
    app.register_blueprint(courier_routes)
    app.register_blueprint(address_routes)
    app.register_blueprint(customer_routes)
    app.register_blueprint(dispute_routes)
    app.register_blueprint(category_routes)
    app.register_blueprint(newsletter_routes)
    app.register_blueprint(payment_routes)
    app.register_blueprint(review_routes)
    app.register_blueprint(statistics_routes)
    app.register_blueprint(bot_routes)
    app.register_blueprint(botmanagement_route)
    app.register_blueprint(treasure_routes)
    app.register_blueprint(metric_routes)
    app.config['UPLOAD_FOLDER'] = config[config_name].UPLOAD_FOLDER
    app.config['JWT_SECRET_KEY'] = str(secret_key)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    jwt = JWTManager(app)

    return app
