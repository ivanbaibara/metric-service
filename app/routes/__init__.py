from flask import Flask

from .data import data_bp
from .login import login_bp


def register_routes(app: Flask):
    app.register_blueprint(login_bp)
    app.register_blueprint(data_bp)