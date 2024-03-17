from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.transactions import Transaction
from models.accounts import Account
from datetime import datetime
from sql_connector.mysql_connector import engine
from sqlalchemy.orm import sessionmaker
import sys


transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route("/transactions", methods=['GET'])
@jwt_required()
def get_transactions():
    try:
        response_data = dict()
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()

        current_user_id = get_jwt_identity()

        transactions_query = session.query(Transaction)


        transactions = transactions_query.all()

        response_data['transactions'] = [transaction.serialize(full=False) for transaction in transactions]

        # return jsonify([transaction.serialize() for transaction in transactions]), 200

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@transaction_routes.route("/transactions/<int:transaction_id>", methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    try:
        response_data = dict()
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()
        current_user_id = get_jwt_identity()
        transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()

        print(transaction , file=sys.stderr)

        if not transaction:
            return jsonify({"message": "Transaction not found"}), 404

        return jsonify(transaction.serialize()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@transaction_routes.route("/transactions", methods=['POST'])
@jwt_required()
def create_transaction():
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()
        current_user_id = get_jwt_identity()
        data = request.json

        transaction_type = data.get('type')
        amount = data.get('amount')
        from_account_id = data.get('account_id_from')
        to_account_id = data.get('account_id_to')
        description = data.get('description')

        print(data , file=sys.stderr)

        if not transaction_type or not amount or not from_account_id or not to_account_id:
            return jsonify({"message": "Incomplete data provided"}), 400

        account = session.query(Account).filter(Account.id==to_account_id).first()
        if not account:
            return jsonify({"message": "Account Receive not found or does not belong to the user"}), 404
        
        account = session.query(Account).filter(Account.id==from_account_id).first()
        if not account:
            return jsonify({"message": "Account Sender not found or does not belong to the user"}), 404

        new_transaction = Transaction(
            to_account_id = to_account_id, from_account_id = from_account_id,amount = amount,type = transaction_type, description = description
        )

        session.add(new_transaction)
        session.commit()

        return jsonify({"message": "Transaction created successfully", "transaction_id": new_transaction.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
