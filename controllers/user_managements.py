from flask import Blueprint, request, redirect, jsonify
from flask_login import login_required, login_user, logout_user
from flask_jwt_extended import create_access_token,jwt_required
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sql_connector.mysql_connector import engine
from models.users import User
from DTO.api_response import api_response

user_management_routes = Blueprint('user_management_routes', __name__)

@user_management_routes.route("/users", methods=['POST'])
def do_registration():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            raise ValueError("Username, email, atau password tidak boleh kosong")

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()
        session.add(new_user)
        session.commit()

        return api_response(
            status_code=201,
            message="Pembuatan data user baru berhasil diinput",
            data={
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            }
        )    
    
    except Exception as e:
        session.rollback()
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )

@user_management_routes.route("/userlogin", methods=['POST'])
def do_user_login():

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return {"message": "Username atau password tidak boleh kosong"}

        user = session.query(User).filter(User.username == username).first()

        if not user:
            return {"message": "Username anda belum terdaftar"}
        
        if not user.check_password(password):
            return {"message": "Password salah"}
        
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
       
    except Exception as e:
        return {"message": "Login belum berhasil "+ str(e)}

@user_management_routes.route("/users", methods=['GET'])
@jwt_required()
def users_home():
    response_data = dict()
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        user_query = session.query(User)


        search_query = request.args.get('query')
        if search_query:
            user_query = user_query.filter(User.username.like(f'%{search_query}%'))

        users = user_query.all()
        response_data['users'] = [user.serialize(full=False) for user in users]
        return jsonify(response_data)

    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    finally:
        session.close()

@user_management_routes.route("/users/<int:user_id>", methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return jsonify(user.serialize(full=True))
        else:
            return jsonify({
                'message': 'User belum terdaftar'
            }), 404
        
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    
    finally:
        session.close()


@user_management_routes.route("/users/<int:user_id>", methods=['PUT'])
@jwt_required()
def update_user_by_id(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        user_to_update = session.query(User).filter(User.id == user_id).first()

        if not user_to_update:
            return api_response(
                status_code=404,
                message="User tidak ditemukan",
                data={}
            )

        user_to_update.username = request.form.get('username', user_to_update.username)
        user_to_update.email = request.form.get('email', user_to_update.email)
        new_password = request.form.get('password')
        if new_password:
            user_to_update.set_password(new_password)
        user_to_update.updated_at = func.now()

        session.commit()
        
        return api_response(
            status_code=201,
            message="Data user berhasil diperbarui",
            data={
                "username": user_to_update.username,
                "email": user_to_update.email,
                "password": new_password
            }
        )    
    except Exception as e:
        session.rollback()
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    
    finally:
        session.close()


@user_management_routes.route("/userlogout", methods=['GET'])
def do_user_logout():
    logout_user()
    return redirect('/')
