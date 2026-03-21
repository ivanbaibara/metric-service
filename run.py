from flask import Flask
from app.routes import register_routes
from config import DB_FULL_PATH
from pathlib import Path
from app.database.data_flt_db import data_flt_create
from app.database.metric_owners_db import metric_owners_create
from app.database.users_db import users_create, users_add, User
from app.database.token_db import tokens_create
from app.database.metrics_db import metrics_create


def setup_database():
    db_file = Path(DB_FULL_PATH)

    if not db_file.exists():
        print("Init db")

        data_flt_create()
        metric_owners_create()
        metrics_create()
        users_create()
        tokens_create()

        user = User()
        user.role = 0
        user.login = 'admin'
        user.password = 'admin'

        users_add(user)

app = Flask(__name__)

app.secret_key = b'_1#y2L"F4Q7z\n\xec]/'

register_routes(app)


if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=5000, debug=True)