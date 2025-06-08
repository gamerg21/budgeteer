from . import db

class Month(db.Model):
    __tablename__ = 'months'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    transactions = db.relationship(
        "Transaction", back_populates="month", cascade="all, delete-orphan"
    )
    statements = db.relationship("Statement", back_populates="month", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Month {self.name} {self.year}>'


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(20))  # 'bank' or 'credit_card'
    issuer = db.Column(db.String(100))
    last4 = db.Column(db.String(4))
    credit_limit = db.Column(db.Float)

    transactions = db.relationship(
        "Transaction", back_populates="account", cascade="all, delete-orphan"
    )
    statements = db.relationship(
        "Statement", back_populates="account", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Account {self.name}>"


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    month_id = db.Column(db.Integer, db.ForeignKey("months.id"), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100))
    transaction_type = db.Column(db.String(10))

    month = db.relationship("Month", back_populates="transactions")
    account = db.relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.description} {self.amount}>"


class Statement(db.Model):
    __tablename__ = "statements"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    month_id = db.Column(db.Integer, db.ForeignKey("months.id"), nullable=False)
    statement_balance = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_made = db.Column(db.Float, default=0.0)

    account = db.relationship("Account", back_populates="statements")
    month = db.relationship("Month", back_populates="statements")

    def __repr__(self):
        return f"<Statement account={self.account_id} month={self.month_id}>"
