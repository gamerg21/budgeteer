const apiBase = 'http://localhost:5000';

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
        const [months, accounts] = await Promise.all([
            fetchData('months'),
            fetchData('accounts')
        ]);

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
    } catch (err) {
        document.getElementById('data').textContent = err.message;
    }
}

loadData();
