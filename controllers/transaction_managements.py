from flask import Blueprint, jsonify
from flask_login import login_required
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sql_connector.mysql_connector import engine
from models.transactions import Transaction
from DTO.api_response import api_response

transactions_management_routes = Blueprint('transactions_management_routes', __name__)

@transactions_management_routes.route("/transactions", methods=['GET'])
@login_required
def get_transactions():
    response_data = dict()
    try:

        Session = sessionmaker(bind=engine)
        with Session() as session:
            transactions = session.query(Transaction).all()
            serialized_transactions = [transaction.serialize(full=False) for transaction in transactions]
            response_data['transactions'] = serialized_transactions
            return jsonify(response_data)

    except SQLAlchemyError as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
