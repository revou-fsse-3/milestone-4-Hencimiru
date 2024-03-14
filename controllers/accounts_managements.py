from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models import Account, User, db
from sqlalchemy.orm.exc import NoResultFound

account_management_routes = Blueprint('account_management_routes', __name__)

@account_management_routes.route("/accounts", methods=['GET'])
@jwt_required()
def get_accounts():
    try:
        current_user_id = get_jwt_identity()
        accounts = Account.query.filter_by(user_id=current_user_id).all()

        return jsonify([account.serialize() for account in accounts]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@account_management_routes.route("/accounts/<int:account_id>", methods=['GET'])
@jwt_required()
def get_account(account_id):
    try:
        current_user_id = get_jwt_identity()
        account = Account.query.get(account_id)

        if not account:
            return jsonify({"message": "Account not found"}), 404

        if account.user_id != current_user_id:
            return jsonify({"message": "Unauthorized"}), 401

        return jsonify(account.serialize()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@account_management_routes.route("/accounts", methods=['POST'])
@jwt_required()
def create_account():
    try:
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
        db.session.add(new_account)
        db.session.commit()

        return jsonify({"message": "Account created successfully", "account_id": new_account.id}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Account number must be unique"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@account_management_routes.route("/accounts/<int:account_id>", methods=['PUT'])
@jwt_required()
def update_account(account_id):
    try:
        current_user_id = get_jwt_identity()
        data = request.json

        account = Account.query.get(account_id)

        if not account:
            return jsonify({"message": "Account not found"}), 404

        if account.user_id != current_user_id:
            return jsonify({"message": "Unauthorized"}), 401

        account.account_type = data.get('account_type', account.account_type)
        account.account_number = data.get('account_number', account.account_number)
        account.balance = data.get('balance', account.balance)

        db.session.commit()

        return jsonify({"message": "Account updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@account_management_routes.route("/accounts/<int:account_id>", methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    try:
        current_user_id = get_jwt_identity()
        account = Account.query.get(account_id)

        if not account:
            return jsonify({"message": "Account not found"}), 404

        if account.user_id != current_user_id:
            return jsonify({"message": "Unauthorized"}), 401

        db.session.delete(account)
        db.session.commit()

        return jsonify({"message": "Account deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
