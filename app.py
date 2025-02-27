from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for session management

# Categorized menu
menu = {
    "Hot Beverages": {
        1: {"name": "Espresso", "price": 1.99},
        2: {"name": "Cappuccino", "price": 3.50},
        3: {"name": "Latte", "price": 3.99},
        4: {"name": "Masala Chai", "price": 2.50}
    },
    "Cold Beverages": {
        5: {"name": "Iced Coffee", "price": 3.50},
        6: {"name": "Cold Brew", "price": 4.00},
        7: {"name": "Milkshake", "price": 4.99},
        8: {"name": "Lemonade", "price": 2.99}
    },
    "Veg Snacks": {
        9: {"name": "Grilled Cheese", "price": 4.99},
        10: {"name": "Paneer Wrap", "price": 5.50},
        11: {"name": "French Fries", "price": 3.50},
        12: {"name": "Garlic Bread", "price": 3.99}
    },
    "Non-Veg Snacks": {
        13: {"name": "Chicken Sandwich", "price": 5.99},
        14: {"name": "BBQ Wings", "price": 6.99},
        15: {"name": "Pepperoni Pizza", "price": 8.99},
        16: {"name": "Chicken Wrap", "price": 6.50}
    },
    "Desserts": {
        17: {"name": "Chocolate Cake", "price": 4.50},
        18: {"name": "Brownie", "price": 3.99},
        19: {"name": "Ice Cream", "price": 2.99},
        20: {"name": "Cheesecake", "price": 5.50}
    }
}

# Function to calculate subtotal
def calculate_subtotal(order):
    return round(sum(item["price"] * item["quantity"] for item in order), 2)

# Function to calculate tax (15%)
def calculate_tax(subtotal):
    return round(subtotal * 0.15, 2)

# Home page - User enters name & email
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session["name"] = request.form.get("name", "").strip()
        session["email"] = request.form.get("email", "").strip()

        if not session["name"] or not session["email"]:
            return render_template("home.html", error="Please enter both name and email.")

        return redirect(url_for("menu_page"))
    return render_template("home.html")

# Menu page - Display categorized menu
@app.route("/menu", methods=["GET", "POST"])
def menu_page():
    if "name" not in session or "email" not in session:
        return redirect(url_for("home"))  # Prevent direct access without login

    if request.method == "POST":
        session["order"] = []
        for category, items in menu.items():
            for item_id, item in items.items():
                quantity = request.form.get(str(item_id), "").strip()
                if quantity.isdigit() and int(quantity) > 0:
                    session["order"].append({
                        "name": item["name"],
                        "price": item["price"],
                        "quantity": int(quantity)
                    })

        if not session["order"]:  # Ensure at least one item is selected
            return render_template("menu.html", menu=menu, error="Please select at least one item.")
        
        return redirect(url_for("receipt"))

    return render_template("menu.html", menu=menu)

# Receipt page - Display order summary
@app.route("/receipt")
def receipt():
    if "name" not in session or "email" not in session or "order" not in session:
        return redirect(url_for("home"))  # Prevent direct access

    order = session["order"]
    subtotal = calculate_subtotal(order)
    tax = calculate_tax(subtotal)
    total = round(subtotal + tax, 2)

    return render_template("receipt.html", name=session["name"], email=session["email"], order=order, subtotal=subtotal, tax=tax, total=total)

if __name__ == "__main__":
    app.run(debug=True)
