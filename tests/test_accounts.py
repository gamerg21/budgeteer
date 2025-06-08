import datetime
import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Month, Account, Transaction

@pytest.fixture
def client():
    app = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        month = Month(
            name='January',
            year=2023,
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2023, 1, 31),
        )
        db.session.add(month)
        db.session.commit()

        account = Account(name='Checking', account_type='bank', last4='0001')
        db.session.add(account)
        db.session.commit()

        t1 = Transaction(
            month_id=month.id,
            account_id=account.id,
            date=datetime.date(2023, 1, 5),
            description='Deposit',
            amount=200.0,
        )
        t2 = Transaction(
            month_id=month.id,
            account_id=account.id,
            date=datetime.date(2023, 1, 6),
            description='Withdrawal',
            amount=-50.0,
        )
        db.session.add_all([t1, t2])
        db.session.commit()

    with app.test_client() as client:
        yield client


def test_get_accounts(client):
    resp = client.get('/accounts')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    acct = data[0]
    assert acct['name'] == 'Checking'
    assert acct['type'] == 'bank'
    assert acct['last4'] == '0001'
    assert acct['balance'] == 150.0
