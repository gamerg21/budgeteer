// Fetch months, accounts, and transactions from the Flask API
const apiBase = 'http://localhost:5000';

let months = [];
let accounts = [];
let currentMonthId = null;

async function fetchData(endpoint) {
    const resp = await fetch(`${apiBase}/${endpoint}`);
    if (!resp.ok) {
        throw new Error(`Failed to fetch ${endpoint}`);
    }
    return resp.json();
}

async function loadData() {
    try {
        // get months and accounts
        [months, accounts] = await Promise.all([
            fetchData('months'),
            fetchData('accounts')
        ]);

        currentMonthId = months.length ? months[0].id : null;

        populateSelects();

        // Build months table
        let html = '<h2>Months</h2><table><tr><th>Name</th><th>Year</th></tr>';
        months.forEach(m => {
            html += `<tr><td>${m.name}</td><td>${m.year}</td></tr>`;
        });
        html += '</table>';

        // Build accounts table
        html += '<h2>Accounts</h2><table><tr><th>Name</th><th>Type</th><th>Balance</th></tr>';
        accounts.forEach(a => {
            html += `<tr><td>${a.name}</td><td>${a.type}</td><td>${a.balance}</td></tr>`;
        });
        html += '</table>';

        document.getElementById('data').innerHTML = html;

        if (currentMonthId) {
            await loadTransactions(currentMonthId);
        }
    } catch (err) {
        document.getElementById('data').textContent = err.message;
    }
}

function populateSelects() {
    const monthSel = document.getElementById('tx-month');
    const acctSel = document.getElementById('tx-account');
    monthSel.innerHTML = '';
    acctSel.innerHTML = '';
    months.forEach(m => {
        const opt = new Option(`${m.name} ${m.year}`, m.id);
        monthSel.add(opt);
    });
    accounts.forEach(a => {
        const opt = new Option(a.name, a.id);
        acctSel.add(opt);
    });
    monthSel.value = currentMonthId;
}

async function loadTransactions(monthId) {
    const txs = await fetchData(`transactions?month_id=${monthId}`);
    let html = '<table><tr><th>Date</th><th>Account</th><th>Description</th><th>Category</th><th>Amount</th></tr>';
    txs.forEach(tx => {
        html += `<tr><td>${tx.date}</td><td>${tx.account}</td><td>${tx.description}</td><td>${tx.category}</td><td>${tx.amount}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('transactions').innerHTML = html;
}

document.getElementById('tx-month').addEventListener('change', (e) => {
    currentMonthId = parseInt(e.target.value, 10);
    loadTransactions(currentMonthId);
});

document.getElementById('tx-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        month_id: parseInt(document.getElementById('tx-month').value, 10),
        account_id: parseInt(document.getElementById('tx-account').value, 10),
        date: document.getElementById('tx-date').value,
        description: document.getElementById('tx-desc').value,
        amount: parseFloat(document.getElementById('tx-amount').value),
        category: document.getElementById('tx-category').value
    };

    const resp = await fetch(`${apiBase}/transactions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (resp.ok) {
        await loadTransactions(payload.month_id);
        document.getElementById('tx-form').reset();
    } else {
        const err = await resp.json();
        alert(err.error || 'Failed to create transaction');
    }
});

loadData();
