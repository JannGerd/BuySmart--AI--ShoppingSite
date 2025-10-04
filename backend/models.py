from sqlalchemy import Column, Integer, String, Float, Enum
import enum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Date, ForeignKey
from sqlalchemy import DateTime
from datetime import datetime
from backend.database import Base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(100))
    username = Column(String(100))
    password = Column(String(100))


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    stock_amount = Column(Integer, nullable=False)



class OrderStatus(enum.Enum):
    TEMP = "TEMP"
    CLOSE = "CLOSE"


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.TEMP)
    order_date = Column(Date, default=datetime.utcnow)
    shipping_address = Column(String(255))
    total_price = Column(Float, default=0.0)


    items = relationship("OrderItem", back_populates="order")
    user = relationship("User", back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    payment_method = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    paid_at = Column(DateTime, nullable=False)


class UserWishlist(Base):
    __tablename__ = "user_wishlist"

    wishlist_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    added_at = Column(Date)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    city = Column(String(100))
    country = Column(String(100))
    phone = Column(String(50))


