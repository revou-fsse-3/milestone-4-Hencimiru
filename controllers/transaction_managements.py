from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Transaction, Account
from datetime import datetime

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route("/transactions", methods=['GET'])
@jwt_required()
def get_transactions():
    try:
        current_user_id = get_jwt_identity()
        account_id = request.args.get('account_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        transactions_query = Transaction.query.filter_by(user_id=current_user_id)

        if account_id:
            transactions_query = transactions_query.filter_by(account_id=account_id)

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            transactions_query = transactions_query.filter(Transaction.date >= start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            transactions_query = transactions_query.filter(Transaction.date <= end_date)

        transactions = transactions_query.all()

        return jsonify([transaction.serialize() for transaction in transactions]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@transaction_routes.route("/transactions/<int:transaction_id>", methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    try:
        current_user_id = get_jwt_identity()
        transaction = Transaction.query.get(transaction_id)

        if not transaction:
            return jsonify({"message": "Transaction not found"}), 404

        if transaction.user_id != current_user_id:
            return jsonify({"message": "Unauthorized"}), 401

        return jsonify(transaction.serialize()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@transaction_routes.route("/transactions", methods=['POST'])
@jwt_required()
def create_transaction():
    try:
        current_user_id = get_jwt_identity()
        data = request.json

        transaction_type = data.get('type')
        amount = data.get('amount')
        account_id = data.get('account_id')

        if not transaction_type or not amount or not account_id:
            return jsonify({"message": "Incomplete data provided"}), 400

        # Cek apakah akun milik pengguna
        account = Account.query.filter_by(id=account_id, user_id=current_user_id).first()
        if not account:
            return jsonify({"message": "Account not found or does not belong to the user"}), 404

        # Initiate transaction
        new_transaction = Transaction(
            type=transaction_type,
            amount=amount,
            account_id=account_id
        )
        new_transaction.save()

        return jsonify({"message": "Transaction created successfully", "transaction_id": new_transaction.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
