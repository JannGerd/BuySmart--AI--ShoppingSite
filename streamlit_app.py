import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import requests

st.set_page_config(page_title="BuySmart Dashboard", layout="wide")
st.title("BuySmart 📊 Dashboard")

st.subheader("Wellcome")
response = requests.get("http://localhost:8000/")
if response.status_code == 200:
    st.success(response.json()["message"])
else:
    st.error("😕 Could not connect to the server")


response = requests.get("http://localhost:8000/orders")
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



response_payments = requests.get("http://localhost:8000/payments")
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