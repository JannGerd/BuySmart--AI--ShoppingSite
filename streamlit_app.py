import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="BuySmart", layout="wide")
st.title("🛒 BuySmart Website")


if "token" not in st.session_state:
    st.session_state["token"] = None


def get_headers():
    if st.session_state["token"]:
        return {"Authorization": f"Bearer {st.session_state['token']}"}
    return {}


def get_products():
    r = requests.get(f"{API_URL}/products", headers=get_headers())
    return pd.DataFrame(r.json()) if r.status_code == 200 else None

def get_orders():
    r = requests.get(f"{API_URL}/orders", headers=get_headers())
    return pd.DataFrame(r.json()) if r.status_code == 200 else None

def get_favorites():
    r = requests.get(f"{API_URL}/favorites", headers=get_headers())
    return pd.DataFrame(r.json()) if r.status_code == 200 else None

def chat_with_assistant(message):
    r = requests.post(f"{API_URL}/chat", json={"message": message}, headers=get_headers())
    return r.json().get("answer") if r.status_code == 200 else "Error"


menu = ["Dashboard", "Products", "Orders", "Favorites", "Chat Assistant", "Login/Register"]
choice = st.sidebar.radio("Navigate", menu)


if choice == "Dashboard":
    st.subheader("📊 Dashboard")

    response = requests.get(API_URL + "/", headers=get_headers())
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Could not connect to the server")

    response = requests.get(API_URL + "/orders", headers=get_headers())
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        df['order_date'] = pd.to_datetime(df['order_date'])
        df['month'] = df['order_date'].dt.to_period('M')
        orders_per_month = df.groupby('month').size()

        fig, ax = plt.subplots()
        orders_per_month.plot(kind='bar', ax=ax)
        ax.set_title("Number of Orders by Month")
        ax.set_ylabel("Order Count")
        st.pyplot(fig)
    else:
        st.error("Failed to fetch order data")

    response_payments = requests.get(API_URL + "/payments", headers=get_headers())
    if response_payments.status_code == 200:
        data_payments = response_payments.json()
        df_payments = pd.DataFrame(data_payments)

        payment_totals = df_payments.groupby("payment_method")["amount"].sum().reset_index()

        fig2, ax2 = plt.subplots()
        sns.barplot(data=payment_totals, x="payment_method", y="amount", ax=ax2)
        ax2.set_title("Sales by Payment Method")
        ax2.set_ylabel("Total Amount (₪)")
        st.pyplot(fig2)
    else:
        st.error("Oops! Failed to load payment data")


elif choice == "Products":
    st.subheader("🛍️ Products")
    df = get_products()
    if df is not None:
        for _, row in df.iterrows():
            st.write(f"{row['name']} – ₪{row['price']} (Stock: {row['stock']})")
            col1, col2 = st.columns(2)
            if col1.button(f"Add to Order", key=f"order_{row['id']}"):
                r = requests.post(API_URL + "/orders/add_item",
                                  json={"product_id": row['id']}, headers=get_headers())
                if r.status_code == 200:
                    st.success("Added to order")
                else:
                    st.error("Failed to add to order")
            if col2.button(f"Add to Favorites", key=f"fav_{row['id']}"):
                r = requests.post(API_URL + "/favorites/add",
                                  json={"product_id": row['id']}, headers=get_headers())
                if r.status_code == 200:
                    st.success("Added to favorites")
                else:
                    st.error("Failed to add to favorites")
    else:
        st.warning("No products found")


elif choice == "Orders":
    st.subheader("📦 Orders")
    df = get_orders()
    if df is not None:
        st.dataframe(df)
    else:
        st.warning("No orders found or unauthorized")


elif choice == "Favorites":
    st.subheader("⭐ Favorites")
    df = get_favorites()
    if df is not None:
        st.dataframe(df)
    else:
        st.warning("No favorites found or unauthorized")


elif choice == "Chat Assistant":
    st.subheader("🤖 Chat Assistant")
    if "chat_count" not in st.session_state:
        st.session_state["chat_count"] = 0

    if st.session_state["chat_count"] >= 5:
        st.warning("You reached the maximum of 5 questions.")
    else:
        user_msg = st.text_input("Your question:")
        if st.button("Send"):
            answer = chat_with_assistant(user_msg)
            st.write("**Assistant:**", answer)
            st.session_state["chat_count"] += 1


elif choice == "Login/Register":
    st.subheader("🔐 Login / Register")

    action = st.radio("Select action:", ["Register", "Login", "Logout"])

    if action == "Register":
        st.write("Create a new account:")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        city = st.text_input("City")
        country = st.text_input("Country")
        phone = st.text_input("Phone")

        if st.button("Register"):
            payload = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "username": username,
                "password": password,
                "city": city,
                "country": country,
                "phone": phone,
            }
            r = requests.post(API_URL + "/auth/register", json=payload)
            if r.status_code in (200, 201):
                st.success("Registration successful! Now you can log in.")
            else:
                st.error(r.json().get("detail", "Registration failed."))

    elif action == "Login":
        st.write("Login to your account:")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            r = requests.post(API_URL + "/auth/login",
                              data={"username": username, "password": password})
            if r.status_code == 200:
                token = r.json()["access_token"]
                st.session_state["token"] = token
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

    elif action == "Logout":
        if st.session_state["token"]:
            st.session_state["token"] = None
            st.success("You have been logged out.")
        else:
            st.info("You are not logged in.")