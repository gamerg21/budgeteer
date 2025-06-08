from flask import Blueprint, jsonify
from datetime import date

from . import db
from .models import Account, Month, Transaction

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
