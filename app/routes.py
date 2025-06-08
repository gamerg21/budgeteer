from flask import Blueprint, jsonify
from .models import Account

api = Blueprint('api', __name__)

@api.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"}), 200


@api.route('/accounts', methods=['GET'])
def get_accounts():
    """Return list of accounts with balance."""
    accounts = Account.query.all()
    data = []
    for account in accounts:
        balance = sum(t.amount for t in account.transactions)
        data.append({
            "name": account.name,
            "type": account.account_type,
            "last4": account.last4,
            "balance": balance,
        })
    return jsonify(data), 200
