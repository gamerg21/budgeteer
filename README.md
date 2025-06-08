# 💸 Budgeteer

**Budgeteer** is a self-hosted, mobile-friendly, web-based expense tracker designed for power users who want full control over how they track expenses, credit card balances, and monthly statements. It is inspired by a spreadsheet-first workflow and built using Python (Flask), SQLAlchemy, and SQLite/PostgreSQL.

---

## 🚀 Features

- Monthly tracking of expenses, balances, and payments
- Credit card-level breakdowns
- Statement due dates and payment records
- Mobile-friendly UI (coming soon)
- Fully self-hosted with Docker support
- Extensible and privacy-respecting — your data, your server

---

## 🧱 Tech Stack

- **Backend:** Flask + SQLAlchemy
- **Database:** SQLite (default) or PostgreSQL
- **Frontend:** React (WIP)
- **Containerized:** Docker / Docker Compose ready

---

## 📂 Project Structure
<pre><code>
budgeteer/
├── app/
│   ├── __init__.py       # App factory
│   ├── models.py         # SQLAlchemy models
│   ├── routes.py         # RESTful API routes
│   ├── db.sqlite3        # Local dev database
├── run.py                # Main app runner
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker build
├── .gitignore
└── README.md
</code> </pre>
---

## 🧮 Database Schema

### `months`
| Field        | Type    | Description               |
|--------------|---------|---------------------------|
| id           | INTEGER | Primary key               |
| name         | TEXT    | e.g., January             |
| year         | INTEGER | e.g., 2025                |
| start_date   | DATE    | Month start               |
| end_date     | DATE    | Month end                 |

---

### `credit_cards`
| Field         | Type    | Description               |
|---------------|---------|---------------------------|
| id            | INTEGER | Primary key               |
| name          | TEXT    | e.g., "Amex Gold"         |
| issuer        | TEXT    | e.g., "American Express"  |
| last4         | TEXT    | Last 4 digits of card     |
| credit_limit  | REAL    | Optional limit            |

---

### `expenses`
| Field        | Type    | Description                            |
|--------------|---------|----------------------------------------|
| id           | INTEGER | Primary key                            |
| month_id     | INTEGER | Foreign key to `months`                |
| card_id      | INTEGER | Foreign key to `credit_cards`          |
| date         | DATE    | Expense date                           |
| description  | TEXT    | Merchant or label                      |
| amount       | REAL    | Expense amount                         |
| category     | TEXT    | Optional tag (e.g., groceries, fuel)   |

---

### `statements`
| Field             | Type    | Description                      |
|-------------------|---------|----------------------------------|
| id                | INTEGER | Primary key                      |
| card_id           | INTEGER | Foreign key to `credit_cards`    |
| month_id          | INTEGER | Foreign key to `months`          |
| statement_balance | REAL    | Closing balance for the period   |
| due_date          | DATE    | Due date for that month’s bill   |
| payment_made      | REAL    | Amount paid                      |

---

## 🐳 Docker Quick Start

```bash
# Build the container
docker build -t budgeteer .

# Run the app on port 5000
docker run -p 5000:5000 budgeteer


✅ TODO
 Build React frontend
 Add user authentication
 Export reports to CSV
 Add recurring expense logic
 Make UI PWA/mobile-installable