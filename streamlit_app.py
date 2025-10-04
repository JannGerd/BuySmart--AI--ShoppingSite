import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests

# ==========================================
# Basic Configuration
# ==========================================
API_URL = "http://localhost:8000"
st.set_page_config(page_title="BuySmart", layout="wide")

# ==========================================
# Session Management
# ==========================================
if "token" not in st.session_state:
    st.session_state["token"] = None
if "chat_count" not in st.session_state:
    st.session_state["chat_count"] = 0


def get_headers():
    if st.session_state["token"]:
        return {"Authorization": f"Bearer {st.session_state['token']}"}
    return {}

# ==========================================
# Helper Functions
# ==========================================
def get_products():
    r = requests.get(f"{API_URL}/products", headers=get_headers())
    return pd.DataFrame(r.json()) if r.status_code == 200 else None


def get_orders():
    r = requests.get(f"{API_URL}/orders", headers=get_headers())
    return pd.DataFrame(r.json()) if r.status_code == 200 else None


def get_payments():
    r = requests.get(f"{API_URL}/payments", headers=get_headers())
    return pd.DataFrame(r.json()) if r.status_code == 200 else None


def get_wishlist():
    r = requests.get(f"{API_URL}/wishlist", headers=get_headers())
    return pd.DataFrame(r.json()) if r.status_code == 200 else None


def chat_with_assistant(message):
    r = requests.post(f"{API_URL}/chat", json={"message": message}, headers=get_headers())
    return r.json().get("answer") if r.status_code == 200 else "Error connecting to assistant."


# ==========================================
# Sidebar Navigation
# ==========================================
menu = [
    "Home",
    "Dashboard",
    "Products",
    "Orders",
    "Payments",
    "Wishlist",
    "Search Products",
    "Chat Assistant",
    "Login / Register"
]
choice = st.sidebar.radio("Navigate", menu)

# ==========================================
# Home Page
# ==========================================
if choice == "Home":
    st.markdown("<h1 style='text-align:center;'>Welcome to BuySmart </h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>Your personal AI-powered shopping assistant</h4>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081875.png", width=150)
    st.write("---")

    st.markdown(
        """
        <p style='text-align:center; font-size:18px;'>
        Discover products, manage orders, make secure payments, and chat with your smart assistant.
        </p>
        """, unsafe_allow_html=True)

    if st.button("Start Shopping"):
        st.session_state["page"] = "🛍 Products"
        st.success("Redirecting to products page...")

# ==========================================
# Dashboard Page
# ==========================================
elif choice == "Dashboard":
    st.subheader("Dashboard Overview")

    # Orders Chart
    df_orders = get_orders()
    if df_orders is not None and not df_orders.empty:
        df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])
        df_orders["month"] = df_orders["order_date"].dt.to_period("M")
        orders_per_month = df_orders.groupby("month").size()

        fig, ax = plt.subplots()
        orders_per_month.plot(kind="bar", ax=ax)
        ax.set_title("Number of Orders per Month")
        ax.set_ylabel("Orders Count")
        st.pyplot(fig)
    else:
        st.info("No order data available.")

    # ==========================================
    # Pie Chart: Orders by Status
    # ==========================================
    if df_orders is not None and not df_orders.empty and "status" in df_orders.columns:
        status_counts = df_orders["status"].value_counts()
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(
            status_counts.values,
            labels=status_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#1ABC9C", "#E74C3C"]
        )
        ax_pie.set_title("Order Status Distribution")
        st.pyplot(fig_pie)


    # Payments Chart
    df_payments = get_payments()
    if df_payments is not None and not df_payments.empty:
        payment_summary = df_payments.groupby("payment_method")["amount"].sum().reset_index()

        fig2, ax2 = plt.subplots()
        sns.barplot(data=payment_summary, x="payment_method", y="amount", ax=ax2)
        ax2.set_title("Sales by Payment Method")
        ax2.set_ylabel("Total Amount (₪)")
        st.pyplot(fig2)
    else:
        st.info("No payment data available.")

# ==========================================
# Products Page
# ==========================================
elif choice == "Products":
    st.subheader("Available Products")
    df = get_products()
    if df is not None and not df.empty:
        for _, row in df.iterrows():
            st.write(f"**{row['name']}** — ₪{row['price']} (Stock: {row['stock_amount']})")
            col1, col2 = st.columns(2)
            if col1.button("🛒 Add to Cart", key=f"order_{row['product_id']}"):
                r = requests.post(f"{API_URL}/orders/add_item/?product_id={row['product_id']}&quantity=1",
                                  headers=get_headers())
                st.success("Added to order!") if r.status_code == 200 else st.error("Failed to add item.")
            if col2.button("Add to Wishlist", key=f"fav_{row['product_id']}"):
                r = requests.post(f"{API_URL}/wishlist/",
                                  json={"product_id": row["product_id"], "customer_id": 1},
                                  headers=get_headers())
                st.success("Added to wishlist!") if r.status_code == 200 else st.error("Failed to add to wishlist.")
    else:
        st.warning("No products available.")

# ==========================================
# Orders Page
# ==========================================
elif choice == "Orders":
    st.subheader("My Orders")

    df = get_orders()
    if df is not None and not df.empty:
        temp_orders = df[df["status"] == "TEMP"]
        closed_orders = df[df["status"] == "CLOSE"]

        if not temp_orders.empty:
            st.markdown("### Current Cart (TEMP Orders)")
            st.dataframe(temp_orders)
            order_id = int(temp_orders.iloc[0]["order_id"])
            if st.button("Close Order"):
                r = requests.put(f"{API_URL}/orders/close/{order_id}", headers=get_headers())
                st.success("Order closed!") if r.status_code == 200 else st.error("Error closing order.")
        else:
            st.info("No open (TEMP) orders.")

        st.markdown("### Completed Orders (CLOSE)")
        st.dataframe(closed_orders) if not closed_orders.empty else st.info("No completed orders found.")
    else:
        st.warning("No orders found or unauthorized access.")


elif choice == "Payments":
    st.subheader("All Payments")
    df_payments = get_payments()

    if df_payments is not None and not df_payments.empty:
        st.dataframe(df_payments)

        # ==========================================
        # Pie Chart: Payment Methods Distribution
        # ==========================================
        method_counts = df_payments["payment_method"].value_counts()
        fig_pie_pay, ax_pie_pay = plt.subplots()
        ax_pie_pay.pie(
            method_counts.values,
            labels=method_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#3498DB", "#2ECC71", "#E67E22", "#E74C3C"]
        )
        ax_pie_pay.set_title("Payment Methods Distribution")
        st.pyplot(fig_pie_pay)

    else:
        st.warning("No payments found or unauthorized access.")

# ==========================================
# Wishlist Page
# ==========================================
elif choice == "Wishlist":
    st.subheader("My Wishlist")
    df = get_wishlist()
    if df is not None and not df.empty:
        st.dataframe(df)
    else:
        st.warning("Your wishlist is empty.")

# ==========================================
# Search Products
# ==========================================
elif choice == "Search Products":
    st.subheader("Search Products")
    name = st.text_input("Product Name (optional)")
    min_price = st.number_input("Min Price", 0.0, step=1.0)
    max_price = st.number_input("Max Price", 0.0, step=1.0)
    min_stock = st.number_input("Min Stock", 0, step=1)
    max_stock = st.number_input("Max Stock", 0, step=1)

    if st.button("Search"):
        params = {"name": name, "min_price": min_price, "max_price": max_price,
                  "min_stock": min_stock, "max_stock": max_stock}
        response = requests.get(f"{API_URL}/products/search/", params=params, headers=get_headers())
        if response.status_code == 200:
            results = response.json()
            if results:
                st.dataframe(pd.DataFrame(results))
            else:
                st.info("No matching products found.")
        else:
            st.error("Error searching products.")

# ==========================================
# Chat Assistant
# ==========================================
elif choice == "Chat Assistant":
    st.subheader("AI Chat Assistant")
    if st.session_state["chat_count"] >= 5:
        st.warning("You have reached the maximum of 5 questions.")
    else:
        msg = st.text_input("Ask a question:")
        if st.button("Send"):
            answer = chat_with_assistant(msg)
            st.write("**Assistant:**", answer)
            st.session_state["chat_count"] += 1

# ==========================================
# Login / Register
# ==========================================
elif choice == "Login / Register":
    st.subheader("Login or Register")
    action = st.radio("Choose action:", ["Login", "Register", "Logout"])

    if action == "Register":
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        city = st.text_input("City")
        country = st.text_input("Country")
        phone = st.text_input("Phone")

        if st.button("Register"):
            data = {"first_name": first_name, "last_name": last_name, "email": email,
                    "username": username, "password": password, "city": city,
                    "country": country, "phone": phone}
            r = requests.post(f"{API_URL}/auth/register", json=data)
            st.success("Registered successfully!") if r.status_code in (200, 201) else st.error("Registration failed.")

    elif action == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            r = requests.post(f"{API_URL}/auth/login", data={"username": username, "password": password})
            if r.status_code == 200:
                st.session_state["token"] = r.json()["access_token"]
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password.")

    elif action == "Logout":
        st.session_state["token"] = None
        st.info("You have been logged out.")
