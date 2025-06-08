# 💸 Budgeteer

**Budgeteer** is a self-hosted, mobile-friendly, web-based expense tracker designed for power users who want full control over how they track expenses, credit card balances, and monthly statements. It is inspired by a spreadsheet-first workflow and built using Python (Flask), SQLAlchemy, and SQLite/PostgreSQL.

---

## 🚀 Features

- Monthly tracking of expenses, balances, and payments
- Account-level breakdowns (credit cards and bank accounts)
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

### `accounts`
| Field        | Type    | Description                              |
|--------------|---------|------------------------------------------|
| id           | INTEGER | Primary key                              |
| name         | TEXT    | Account name                             |
| account_type | TEXT    | `bank` or `credit_card`                  |
| issuer       | TEXT    | Bank or card issuer                      |
| last4        | TEXT    | Last 4 digits (if applicable)            |
| credit_limit | REAL    | Optional limit for credit card accounts  |

---

### `transactions`
| Field            | Type    | Description                                          |
|------------------|---------|------------------------------------------------------|
| id               | INTEGER | Primary key                                          |
| month_id         | INTEGER | Foreign key to `months`                              |
| account_id       | INTEGER | Foreign key to `accounts`                            |
| date             | DATE    | Transaction date                                     |
| description      | TEXT    | Merchant or label                                    |
| amount           | REAL    | Transaction amount (positive or negative)            |
| category         | TEXT    | Optional tag (e.g., groceries, fuel)                 |
| transaction_type | TEXT    | Optional indicator like `debit` or `credit`          |

---

### `statements`
| Field             | Type    | Description                               |
|-------------------|---------|-------------------------------------------|
| id                | INTEGER | Primary key                               |
| account_id        | INTEGER | Foreign key to `accounts` (credit cards)  |
| month_id          | INTEGER | Foreign key to `months`                   |
| statement_balance | REAL    | Closing balance for the period            |
| due_date          | DATE    | Due date for that month’s bill            |
| payment_made      | REAL    | Amount paid                               |

---

## 🐳 Docker Quick Start

```bash
# Build the container
docker build -t budgeteer .

# Run the app on port 5000
docker run -p 5000:5000 budgeteer
```

✅ TODO
 Build React frontend
 Add user authentication
 Export reports to CSV
 Add recurring expense logic
 Make UI PWA/mobile-installable

## 🖥 Frontend Quick Start

A basic HTML frontend is available in the `frontend/` directory. Start a small
static server there so the page can query the API running on port `5000`:

```bash
cd frontend
python -m http.server 3000
```

Then open <http://localhost:3000> in your browser. The page will display months
and accounts from the test database. The `script.js` file fetches this data and
renders it inside a `<div id="data"></div>` element. If nothing renders, open the
browser console to check for JavaScript errors.
