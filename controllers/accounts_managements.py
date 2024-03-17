from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sql_connector.mysql_connector import engine
from models.accounts import Account
from sqlalchemy.orm.exc import NoResultFound
from DTO.api_response import api_response
import sys

account_management_routes = Blueprint('account_management_routes', __name__)

@account_management_routes.route("/accounts", methods=['GET'])
@jwt_required()
def get_accounts():
    try:
        response_data = dict()
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()

        current_user_id = get_jwt_identity()

        account_query = session.query(Account)


        search_query = request.args.get('query')
        if search_query:
            accounts = Account.query.filter_by(user_id=current_user_id).all()
        
        accounts = account_query.all()
        response_data['account'] = [account.serialize(full=False) for account in accounts]

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@account_management_routes.route("/accounts/<int:account_id>", methods=['GET'])
@jwt_required()
def get_account(account_id):
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()

        current_user_id = get_jwt_identity()
        # account = Account.query.get(account_id)
        account = session.query(Account).filter(Account.id == account_id).first()

        if not account:
            return jsonify({"message": "Account not found"}), 404

        # if account.user_id != current_user_id:
        #     return jsonify({"message": "Unauthorized"}), 401

        return jsonify(account.serialize()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@account_management_routes.route("/accounts", methods=['POST'])
@jwt_required()
def create_account():
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()

        current_user_id = get_jwt_identity()
        data = request.json

        account_type = data.get('account_type')
        account_number = data.get('account_number')
        balance = data.get('balance')

        if not account_type or not account_number or not balance:
            return jsonify({"message": "Incomplete data provided"}), 400

        new_account = Account(
            user_id=current_user_id,
            account_type=account_type,
            account_number=account_number,
            balance=balance
        )
        session.add(new_account)
        session.commit()

        return jsonify({"message": "Account created successfully", "account_id": new_account.id}), 201

    except IntegrityError:
        session.rollback()
        return jsonify({"message": "Account number must be unique"}), 400

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally: 
        session.close()

@account_management_routes.route("/accounts/<int:account_id>", methods=['PUT'])
@jwt_required()
def update_account(account_id):
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()
        account_to_update = session.query(Account).filter(Account.id == account_id).first()
        print(account_to_update, file=sys.stderr)

        if not account_to_update:
            return api_response(
                status_code=404,
                message="Account Not Found",
                data={}
            )

        account_to_update.account_type = request.form.get('account_type', account_to_update.account_type)
        account_to_update.account_number = request.form.get('account_number', account_to_update.account_number)
        account_to_update.balance = request.form.get('balance', account_to_update.balance)
     
        session.commit()
        
        return api_response(
            status_code=201,
            message="Account update succesful",
            data={
                "account_type": account_to_update.account_type,
                "account_number": account_to_update.account_number,
                "balance": account_to_update.balance
            }
        )    
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()


@account_management_routes.route("/accounts/<int:account_id>", methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()

        current_user_id = get_jwt_identity()
        account = session.query(Account).filter(Account.id == account_id).first()


        if not account:
            return jsonify({"message": "Account not found"}), 404

        session.delete(account)
        session.commit()

        return jsonify({"message": "Account deleted successfully"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
