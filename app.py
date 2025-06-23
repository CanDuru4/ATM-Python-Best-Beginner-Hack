from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

# HTML template for the ATM web interface
TEMPLATE = '''
<!doctype html>
<title>ATM Web App</title>
<h2>Welcome to the Bank ATM Web App</h2>
<p><b>Balance:</b> ${{ balance }}</p>
<form method="post" action="/deposit">
    <input type="number" step="0.01" name="amount" placeholder="Deposit Amount" required>
    <button type="submit">Deposit</button>
</form>
<form method="post" action="/withdraw">
    <input type="number" step="0.01" name="amount" placeholder="Withdraw Amount" required>
    <button type="submit">Withdraw</button>
</form>
<h3>Pay Bills</h3>
<form method="post" action="/paybill">
    <select name="bill">
        <option value="electric">Electric (${{ electric }})</option>
        <option value="gas">Gas (${{ gas }})</option>
        <option value="water">Water (${{ water }})</option>
    </select>
    <button type="submit">Pay Bill</button>
</form>
{% if message %}<p style="color:blue;">{{ message }}</p>{% endif %}
'''

def get_account():
    if 'balance' not in session:
        session['balance'] = 250.00
        session['electric'] = 270.00
        session['gas'] = 30.00
        session['water'] = 100.00
    return session

@app.route('/', methods=['GET'])
def home():
    acc = get_account()
    return render_template_string(TEMPLATE, balance=acc['balance'], electric=acc['electric'], gas=acc['gas'], water=acc['water'], message=None)

@app.route('/deposit', methods=['POST'])
def deposit():
    acc = get_account()
    try:
        amount = float(request.form['amount'])
        acc['balance'] += amount
        session.update(acc)
        msg = f"Deposited ${amount:.2f} successfully."
    except Exception:
        msg = "Invalid deposit amount."
    return render_template_string(TEMPLATE, balance=acc['balance'], electric=acc['electric'], gas=acc['gas'], water=acc['water'], message=msg)

@app.route('/withdraw', methods=['POST'])
def withdraw():
    acc = get_account()
    try:
        amount = float(request.form['amount'])
        if acc['balance'] >= amount:
            acc['balance'] -= amount
            session.update(acc)
            msg = f"Withdrew ${amount:.2f} successfully."
        else:
            msg = "Insufficient balance."
    except Exception:
        msg = "Invalid withdraw amount."
    return render_template_string(TEMPLATE, balance=acc['balance'], electric=acc['electric'], gas=acc['gas'], water=acc['water'], message=msg)

@app.route('/paybill', methods=['POST'])
def paybill():
    acc = get_account()
    bill = request.form['bill']
    bill_names = {'electric': 'electric', 'gas': 'gas', 'water': 'water'}
    bill_amount = acc[bill]
    if acc['balance'] >= bill_amount and bill_amount > 0:
        acc['balance'] -= bill_amount
        acc[bill] = 0.0
        session.update(acc)
        msg = f"Paid {bill} bill of ${bill_amount:.2f}."
    elif bill_amount == 0:
        msg = f"{bill.capitalize()} bill already paid."
    else:
        msg = "Insufficient balance to pay bill."
    return render_template_string(TEMPLATE, balance=acc['balance'], electric=acc['electric'], gas=acc['gas'], water=acc['water'], message=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 