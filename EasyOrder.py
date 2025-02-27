import streamlit as st
import time

# 📝 Menu Categories
menu = {
    "Hot Beverages": {
        1: {"name": "Espresso", "price": 150},
        2: {"name": "Cappuccino", "price": 250},
        3: {"name": "Latte", "price": 200},
        4: {"name": "Masala Chai", "price": 120}
    },
    "Cold Beverages": {
        5: {"name": "Iced Coffee", "price": 200},
        6: {"name": "Cold Brew", "price": 100},
        7: {"name": "Milkshake", "price": 250},
        8: {"name": "Lemonade", "price": 80}
    },
    "Veg Snacks": {
        9: {"name": "Grilled Cheese", "price": 86},
        10: {"name": "Paneer Wrap", "price": 300},
        11: {"name": "French Fries", "price": 150},
        12: {"name": "Garlic Bread", "price": 120}
    },
    "Non-Veg Snacks": {
        13: {"name": "Chicken Sandwich", "price": 400},
        14: {"name": "BBQ Wings", "price": 350},
        15: {"name": "Pepperoni Pizza", "price": 280},
        16: {"name": "Chicken Wrap", "price": 300}
    },
    "Desserts": {
        17: {"name": "Chocolate Cake", "price": 120},
        18: {"name": "Brownie", "price": 90},
        19: {"name": "Ice Cream", "price": 110},
        20: {"name": "Cheesecake", "price": 250}
    }
}

# 📌 Calculate subtotal
def calculate_subtotal(order):
    return round(sum(item["price"] * item["quantity"] for item in order), 2)

# 📌 Calculate tax (15%)
def calculate_tax(subtotal):
    return round(subtotal * 0.15, 2)

# 📌 Apply Discounts
def apply_discount(subtotal):
    if subtotal > 15:
        return round(subtotal * 0.10, 2)  # 10% discount on orders above ₹15
    return 0

# 🌟 Streamlit App
def main():
    st.set_page_config(page_title="EasyOrder - Cafe", page_icon="🍽️")

    st.title("🍽️ HappySouls Cafe")
    st.sidebar.header("🛒 Order Summary")

    # Session state initialization
    if "order" not in st.session_state:
        st.session_state["order"] = []
    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "phone" not in st.session_state:
        st.session_state["phone"] = ""
    if "instructions" not in st.session_state:
        st.session_state["instructions"] = ""

    # 👤 User Information Form
    with st.form("user_info"):
        st.subheader("👤 Enter Your Details")
        name = st.text_input("Name", st.session_state["name"])
        phone = st.text_input("Phone Number", st.session_state["phone"])
        order_type = st.radio("Order Type", ["Dine-in", "Takeaway"])
        instructions = st.text_area("📜 Special Instructions (Optional)", st.session_state["instructions"])

        submitted = st.form_submit_button("Proceed to Menu")

        if submitted:
            if not name or not phone:
                st.warning("⚠️ Please enter both name and phone number.")
            else:
                st.session_state["name"] = name
                st.session_state["phone"] = phone
                st.session_state["order_type"] = order_type
                st.session_state["instructions"] = instructions
                st.session_state["order"] = []  # Reset order if restarting
                st.session_state["step"] = "menu"  # Go to the next step

    # 📋 Menu Selection
    if st.session_state.get("step") == "menu" and st.session_state["name"] and st.session_state["phone"]:
        st.subheader("📋 Select Your Items")
        order = []

        for category, items in menu.items():
            st.markdown(f"### 🍽️ {category}")
            for item_id, item in items.items():
                quantity = st.number_input(f"{item['name']} - ₹{item['price']}", min_value=0, max_value=10, key=f"q_{item_id}")
                if quantity > 0:
                    order.append({"name": item["name"], "price": item["price"], "quantity": quantity})

        if st.button("📦 Place Order"):
            if not order:
                st.warning("⚠️ Please select at least one item.")
            else:
                st.session_state["order"] = order
                st.session_state["step"] = "receipt"  # Go to the receipt step

    # 🧾 Order Summary & Receipt
    if st.session_state.get("step") == "receipt" and st.session_state["order"]:
        st.sidebar.success(f"✅ Order by {st.session_state['name']} ({st.session_state['phone']})")
        st.sidebar.subheader("🧾 Receipt")

        order = st.session_state["order"]
        subtotal = calculate_subtotal(order)
        tax = calculate_tax(subtotal)
        discount = apply_discount(subtotal)
        total = round(subtotal + tax - discount, 2)

        for item in order:
            st.sidebar.write(f"🍽️ {item['name']} × {item['quantity']} - ₹{item['price'] * item['quantity']}")

        st.sidebar.write(f"**Subtotal:** ₹{subtotal}")
        st.sidebar.write(f"**Discount (-10% on ₹15+ orders):** ₹{discount}")
        st.sidebar.write(f"**Tax (15%):** ₹{tax}")
        st.sidebar.write(f"**Total:** ₹{total}")

        st.success(f"🧾 Your Total Bill: ₹{total}")

        # 🚀 Estimated Order Preparation & Delivery Time
        with st.spinner("⏳ Preparing your order..."):
            time.sleep(2)  # Simulate processing time
        st.success("✅ Your order is being prepared!")
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.1)
            progress.progress(i + 1)
        st.success("🚀 Your order is ready for pickup/delivery!")

        # ⭐ Feedback & Rating
        st.subheader("🌟 Rate Your Experience")
        rating = st.slider("Rate your order experience (1-5 stars)", 1, 5, 5)
        review = st.text_area("Any suggestions or feedback?")
        if st.button("Submit Feedback"):
            st.success("✅ Thank you for your feedback!")

if __name__ == "__main__":
    main()
