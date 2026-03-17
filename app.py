from flask import Flask, jsonify, request, session
from app.routes import register_routes


app = Flask(__name__)

app.secret_key = b'_1#y2L"F4Q7z\n\xec]/'

register_routes(app)


if __name__ == '__main__':
    app.run(debug=True)