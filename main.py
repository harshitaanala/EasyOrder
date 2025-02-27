import json

# Café Menu with Sections
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

# User authentication with phone number
def user_login():
    print("\n--- Welcome to EasyOrder ---")
    name = input("Enter your name: ")
    
    # Ensure valid 10-digit phone number
    while True:
        phone = input("Enter your phone number (10 digits): ")
        if phone.isdigit() and len(phone) == 10:
            break
        print("Invalid phone number! Please enter a 10-digit number.")

    print(f"\nHello {name}! Let's take your order.")
    return {"name": name, "phone": phone}

# Display menu in sections
def display_menu():
    print("\n------ Café Menu ------")
    for category, items in menu.items():
        print(f"\n📌 {category}:")
        for item_id, details in items.items():
            print(f"{item_id}. {details['name']: <15} | ${details['price']: >5.2f}")
    print()

# Take an order with quantity selection
def take_order():
    display_menu()
    order = []
    while True:
        try:
            item_id = int(input("Enter item number (or 0 to finish): "))
            if item_id == 0:
                break

            for category, items in menu.items():
                if item_id in items:
                    quantity = int(input(f"Enter quantity for {items[item_id]['name']}: "))
                    order.append({"name": items[item_id]["name"], "price": items[item_id]["price"], "quantity": quantity})
                    break
            else:
                print("Invalid item. Try again.")

        except ValueError:
            print("Invalid input. Please enter numbers only.")

    return order

# Update current order (not the total menu)
def update_order(order):
    while True:
        print("\n--- Modify Your Order ---")
        print("1. Add more items")
        print("2. Remove an item")
        print("3. Change item quantity")
        print("4. Done with updates")

        choice = input("Choose an option: ")

        if choice == "1":
            additional_order = take_order()
            order.extend(additional_order)
            print("New items added!")

        elif choice == "2":
            print("\nCurrent Order:")
            for idx, item in enumerate(order, start=1):
                print(f"{idx}. {item['quantity']}x {item['name']}")

            try:
                remove_idx = int(input("Enter the number of the item to remove: ")) - 1
                if 0 <= remove_idx < len(order):
                    removed_item = order.pop(remove_idx)
                    print(f"{removed_item['name']} removed!")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Invalid input. Try again.")

        elif choice == "3":
            print("\nCurrent Order:")
            for idx, item in enumerate(order, start=1):
                print(f"{idx}. {item['quantity']}x {item['name']}")

            try:
                update_idx = int(input("Enter the number of the item to update quantity: ")) - 1
                if 0 <= update_idx < len(order):
                    new_qty = int(input("Enter new quantity: "))
                    order[update_idx]["quantity"] = new_qty
                    print("Quantity updated!")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Invalid input. Try again.")

        elif choice == "4":
            break

        else:
            print("Invalid choice. Try again.")

    return order

# Calculate subtotal
def calculate_subtotal(order):
    return round(sum(item["price"] * item["quantity"] for item in order), 2)

# Calculate tax (15%)
def calculate_tax(subtotal):
    return round(subtotal * 0.15, 2)

# Payment module
def payment(total):
    print("\n--- Payment ---")
    print("1. Cash")
    print("2. Card")
    while True:
        choice = input("Select payment method: ")
        if choice == "1":
            print(f"Payment of ${total:.2f} received in cash.")
            break
        elif choice == "2":
            print(f"Payment of ${total:.2f} processed via card.")
            break
        else:
            print("Invalid choice. Try again.")

# Generate receipt
def generate_receipt(user, order, subtotal, tax, total):
    receipt = {
        "Customer": user["name"],
        "Phone": user["phone"],
        "Order": order,
        "Subtotal": subtotal,
        "Tax": tax,
        "Total": total
    }

    print("\n--- Receipt ---")
    print(f"Customer: {user['name']} (Phone: {user['phone']})")
    for item in order:
        print(f"{item['quantity']}x {item['name']} - ${item['price']:.2f} each")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax: ${tax:.2f}")
    print(f"Total: ${total:.2f}")

    with open("receipt.json", "w") as file:
        json.dump(receipt, file, indent=4)
    print("Receipt saved to receipt.json!")

# Main function
def main():
    user = user_login()

    while True:
        print("\n1. Place an order")
        print("2. Modify your order")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            order = take_order()
            order = update_order(order)  # Allow modifications before checkout

            subtotal = calculate_subtotal(order)
            tax = calculate_tax(subtotal)
            total = round(subtotal + tax, 2)

            payment(total)
            generate_receipt(user, order, subtotal, tax, total)

        elif choice == "2":
            update_order(order)

        elif choice == "3":
            print("Thank you for using EasyOrder! Goodbye.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
