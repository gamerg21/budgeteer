from flask import Blueprint, jsonify, request
from datetime import date, datetime

from . import db
from .models import Account, Month, Transaction, Statement

api = Blueprint('api', __name__)

@api.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"}), 200


@api.route('/seed', methods=['GET'])
def seed_db():
    """Seed the database with some test data. For development only."""

    # Drop and recreate tables to ensure a clean slate
    db.drop_all()
    db.create_all()

    # Create accounts
    credit_card = Account(
        name='Test Credit Card',
        account_type='credit_card',
        issuer='TestBank',
        last4='1111',
        credit_limit=5000.0,
    )
    bank_account = Account(
        name='Test Bank Account',
        account_type='bank',
        issuer='TestBank',
    )

    # Create months
    may_2025 = Month(
        name='May',
        year=2025,
        start_date=date(2025, 5, 1),
        end_date=date(2025, 5, 31),
    )
    june_2025 = Month(
        name='June',
        year=2025,
        start_date=date(2025, 6, 1),
        end_date=date(2025, 6, 30),
    )

    db.session.add_all([credit_card, bank_account, may_2025, june_2025])
    db.session.flush()  # Get IDs for FK relationships

    # Create transactions
    transactions = [
        Transaction(
            month_id=may_2025.id,
            account_id=credit_card.id,
            date=date(2025, 5, 10),
            description='Grocery Store',
            amount=-50.25,
            category='groceries',
        ),
        Transaction(
            month_id=may_2025.id,
            account_id=bank_account.id,
            date=date(2025, 5, 15),
            description='Salary',
            amount=2000.00,
            category='income',
        ),
        Transaction(
            month_id=june_2025.id,
            account_id=credit_card.id,
            date=date(2025, 6, 2),
            description='Gas Station',
            amount=-35.00,
            category='fuel',
        ),
        Transaction(
            month_id=june_2025.id,
            account_id=bank_account.id,
            date=date(2025, 6, 3),
            description='Rent',
            amount=-1000.00,
            category='housing',
        ),
    ]

    db.session.add_all(transactions)
    db.session.commit()

    return jsonify({'message': 'Database seeded with test data'}), 200


@api.route('/accounts', methods=['GET'])
def get_accounts():
    """Return all accounts with basic info and balance."""
    accounts = Account.query.all()
    result = []
    for account in accounts:
        balance = sum(t.amount for t in account.transactions)
        result.append(
            {
                'name': account.name,
                'type': account.account_type,
                'last4': account.last4,
                'balance': balance,
            }
        )

    return jsonify(result), 200


@api.route('/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction."""
    data = request.get_json() or {}

    required_fields = [
        'account_id',
        'month_id',
        'date',
        'amount',
        'description',
        'category',
    ]

    missing = [field for field in required_fields if field not in data]
    if missing:
        return (
            jsonify({'error': f"Missing fields: {', '.join(missing)}"}),
            400,
        )

    try:
        tx_date = (
            datetime.strptime(data['date'], '%Y-%m-%d').date()
            if isinstance(data['date'], str)
            else data['date']
        )
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid date format, expected YYYY-MM-DD'}), 400

    transaction = Transaction(
        account_id=data['account_id'],
        month_id=data['month_id'],
        date=tx_date,
        amount=data['amount'],
        description=data['description'],
        category=data['category'],
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({'id': transaction.id, 'message': 'Transaction created'}), 201


@api.route('/transactions', methods=['GET'])
def get_transactions():
    """Return transactions for a given month, optionally filtered by account."""
    month_id = request.args.get('month_id', type=int)
    if not month_id:
        return jsonify({'error': 'month_id query parameter is required'}), 400

    account_id = request.args.get('account_id', type=int)

    query = Transaction.query.join(Account).filter(Transaction.month_id == month_id)
    if account_id:
        query = query.filter(Transaction.account_id == account_id)

    transactions = query.order_by(Transaction.date).all()

    result = [
        {
            'account': tx.account.name,
            'category': tx.category,
            'date': tx.date.isoformat(),
            'description': tx.description,
            'amount': tx.amount,
        }
        for tx in transactions
    ]

    return jsonify(result), 200


@api.route('/statements', methods=['GET'])
def get_statements():
    """Return statements for a given month."""
    month_id = request.args.get('month_id', type=int)
    if not month_id:
        return jsonify({'error': 'month_id query parameter is required'}), 400

    statements = (
        Statement.query.join(Account)
        .filter(Statement.month_id == month_id)
        .order_by(Statement.due_date)
        .all()
    )

    result = [
        {
            'account_id': stmt.account_id,
            'account_name': stmt.account.name,
            'statement_balance': stmt.statement_balance,
            'due_date': stmt.due_date.isoformat(),
            'payment_made': stmt.payment_made,
        }
        for stmt in statements
    ]

    return jsonify(result), 200
