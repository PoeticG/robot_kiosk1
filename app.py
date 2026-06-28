# Modified Flask routes to allow adding more drinks/food without losing previous selections and removing duplicates

from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_PATH = 'orders.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

if not os.path.exists(DB_PATH):
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            drinks TEXT,
            food TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def main_menu():
    return render_template('main_menu.html')

@app.route('/drinks', methods=['GET', 'POST'])
def drinks():
    coffees = [
        {"name": "Espresso", "options": ["hot"], "image_url": "/static/images/espresso.PNG"},
        {"name": "Americano", "options": ["hot", "iced"], "image_url": "/static/images/americano.PNG"},
        {"name": "Paik's Original Coffee", "options": ["hot", "iced"], "image_url": "/static/images/paiks.PNG"},
        {"name": "Cafe Latte", "options": ["hot", "iced"], "image_url": "/static/images/latte.PNG"},
        {"name": "Caramel Macchiato", "options": ["hot", "iced"], "image_url": "/static/images/macchiato.PNG"},
        {"name": "Cafe Mocha", "options": ["hot", "iced"], "image_url": "/static/images/mocha.PNG"},
        {"name": "Condensed Milk Latte", "options": ["hot", "iced"], "image_url": "/static/images/condensed.PNG"},
        {"name": "Chocolate Latte", "options": ["hot", "iced"], "image_url": "/static/images/chocolate.PNG"},
        {"name": "Green Tea Latte", "options": ["hot", "iced"], "image_url": "/static/images/greentea.PNG"},
        {"name": "Mint Choco Latte", "options": ["hot", "iced"], "image_url": "/static/images/mintchoco.PNG"},
        {"name": "Milk Tea", "options": ["hot", "iced"], "image_url": "/static/images/milktea.PNG"},
    ]

    if request.method == 'POST':
        selected_coffee = []
        for i, coffee in enumerate(coffees, start=1):
            val = request.form.get(f'drinks_{i}')
            if val:
                variant = val.split(" - ")[-1]
                selected_coffee.append({
                    "name": coffee["name"],
                    "variant": variant,
                    "image_url": coffee["image_url"]
                })

        previous = session.get('drinks', [])
        combined = previous + selected_coffee
        # Remove duplicates by converting list of dicts to set of tuples then back
        unique = list({(item['name'], item['variant'], item['image_url']) for item in combined})
        session['drinks'] = [
            {"name": name, "variant": variant, "image_url": image_url} for name, variant, image_url in unique
        ]

        return redirect('/food')

    return render_template('drinks.html', coffees=coffees)

@app.route('/food')
def food():
    pastries = [
        {"name": "Redbean", "image_url": "/static/images/redbean.PNG"},
        {"name": "Walnut", "image_url": "/static/images/walnut.PNG"},
        {"name": "Chocochip Cookie", "image_url": "/static/images/chocochip.PNG"},
        {"name": "Bagel", "image_url": "/static/images/bagel.PNG"},
        {"name": "Mango Bagel", "image_url": "/static/images/mango bagel.PNG"},
        {"name": "Onion Cheese Bagel", "image_url": "/static/images/onion cheese bagel.PNG"},
        {"name": "Egg Bagel", "image_url": "/static/images/egg bagel.PNG"},
        {"name": "Whoopi Pie", "image_url": "/static/images/whoopie pie.PNG"},
        {"name": "Baby Mammot", "image_url": "/static/images/baby mammoth.PNG"},
        {"name": "Pizza Bread", "image_url": "/static/images/pizza bread.PNG"},
        {"name": "Snow Bun Bread", "image_url": "/static/images/snow bun bread.PNG"},
        {"name": "Long Choux", "image_url": "/static/images/long choux.PNG"},
        {"name": "Garlic Baguette", "image_url": "/static/images/garlic baguette.PNG"},
        {"name": "Salted Bread", "image_url": "/static/images/salted bread.PNG"},
        {"name": "Choco Sora", "image_url": "/static/images/choco sora.PNG"},
        {"name": "Salted Caramel", "image_url": "/static/images/salted caramel.PNG"},
        {"name": "Raspberry Butter Bar", "image_url": "/static/images/raspberry butter bar.PNG"},
    ]
    return render_template('food.html', pastries=pastries)

@app.route('/select_food', methods=['POST'])
def select_food():
    selected_names = request.form.getlist('food')
    all_pastries = [
        {"name": "Redbean", "image_url": "/static/images/redbean.PNG"},
        {"name": "Walnut", "image_url": "/static/images/walnut.PNG"},
        {"name": "Chocochip Cookie", "image_url": "/static/images/chocochip.PNG"},
        {"name": "Bagel", "image_url": "/static/images/bagel.PNG"},
        {"name": "Mango Bagel", "image_url": "/static/images/mango bagel.PNG"},
        {"name": "Onion Cheese Bagel", "image_url": "/static/images/onion cheese bagel.PNG"},
        {"name": "Egg Bagel", "image_url": "/static/images/egg bagel.PNG"},
        {"name": "Whoopi Pie", "image_url": "/static/images/whoopie pie.PNG"},
        {"name": "Baby Mammot", "image_url": "/static/images/baby mammoth.PNG"},
        {"name": "Pizza Bread", "image_url": "/static/images/pizza bread.PNG"},
        {"name": "Snow Bun Bread", "image_url": "/static/images/snow bun bread.PNG"},
        {"name": "Long Choux", "image_url": "/static/images/long choux.PNG"},
        {"name": "Garlic Baguette", "image_url": "/static/images/garlic baguette.PNG"},
        {"name": "Salted Bread", "image_url": "/static/images/salted bread.PNG"},
        {"name": "Choco Sora", "image_url": "/static/images/choco sora.PNG"},
        {"name": "Salted Caramel", "image_url": "/static/images/salted caramel.PNG"},
        {"name": "Raspberry Butter Bar", "image_url": "/static/images/raspberry butter bar.PNG"},
    ]
    selected = [item for item in all_pastries if item['name'] in selected_names]

    previous = session.get('food', [])
    combined = previous + selected
    unique = list({(item['name'], item['image_url']) for item in combined})
    session['food'] = [
        {"name": name, "image_url": image_url} for name, image_url in unique
    ]

    return redirect('/summary')

@app.route('/summary')
def summary():
    drinks = session.get('drinks', [])
    food = session.get('food', [])
    return render_template('summary.html', drinks=drinks, food=food)

@app.route('/finish_order', methods=['POST'])
def finish_order():
    drinks = []
    i = 1
    while True:
        name_key = f'drink_item_{i}'
        qty_key = f'drink_qty_{i}'
        if name_key not in request.form:
            break
        item = request.form[name_key]
        qty = request.form.get(qty_key, '1')
        drinks.append(f"{item} (x{qty})")
        i += 1

    food = []
    i = 1
    while True:
        name_key = f'food_item_{i}'
        qty_key = f'food_qty_{i}'
        if name_key not in request.form:
            break
        item = request.form[name_key]
        qty = request.form.get(qty_key, '1')
        food.append(f"{item} (x{qty})")
        i += 1

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    conn.execute('INSERT INTO orders (timestamp, drinks, food) VALUES (?, ?, ?)',
                 (timestamp, ', '.join(drinks), ', '.join(food)))
    conn.commit()
    conn.close()

    print(f"[ORDER RECEIVED] {timestamp}: Drinks={drinks}, Food={food}")
    session.clear()
    return render_template('thank_you.html')

@app.route('/admin')
def admin():
    sort = request.args.get('sort', 'newest')   # 'newest' or 'oldest'
    filter_type = request.args.get('filter', 'all')  # 'all', 'drinks', 'food'

    conn = get_db_connection()

    # Base query
    query = 'SELECT * FROM orders'
    conditions = []

    # Filter conditions (adjust keywords based on your menu items)
    if filter_type == 'drinks':
        conditions.append("drinks IS NOT NULL AND drinks != ''")
    elif filter_type == 'food':
        conditions.append("food IS NOT NULL AND food != ''")

    # Append WHERE clause if any conditions
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    # Sorting
    if sort == 'oldest':
        query += ' ORDER BY timestamp ASC'
    else:
        query += ' ORDER BY timestamp DESC'

    orders = conn.execute(query).fetchall()
    conn.close()

    return render_template('admin.html', orders=orders, sort=sort, filter=filter_type)

@app.route('/clear_orders', methods=['POST'])
def clear_orders():
    conn = get_db_connection()
    conn.execute('DELETE FROM orders')
    conn.commit()
    conn.close()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
