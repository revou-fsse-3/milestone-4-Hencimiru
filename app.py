from flask import Flask
from dotenv import load_dotenv
from sql_connector.mysql_connector import engine
from sqlalchemy import text

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

# Authentication token
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

from models.users import User
import os
from flask import render_template

# Load Controller Files
from controllers.user_managements import user_management_routes
from controllers.accounts_managements import account_management_routes
from controllers.transaction_managements import transaction_routes

load_dotenv()

app = Flask(__name__)

# JWT Manager
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

jwt = JWTManager(app)
# --

# Login Manager --
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    # Menggunakan SQLAlchemy untuk menyimpan data
    session = Session()

    return session.query(User).get(int(user_id))

app.register_blueprint(user_management_routes)
app.register_blueprint(transaction_routes)
app.register_blueprint(account_management_routes)
# --

@app.route('/')
def my_app():

    # Fetch all Users
    user_query = select(User)
    connection = engine.connect()
    Session = sessionmaker(connection)
    with Session() as session:
        result = session.execute(user_query)
        for row in result.scalars():
            print(f'ID: {row.id}, Name: {row.username}')

    return "Congrats anda berhasil terkoneksi ke database"