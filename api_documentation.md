# API Documentation – BuySmart

This document describes all available API endpoints in the BuySmart backend project.

---

## Customers

| Method | Endpoint          | Description            | Request Body       | Response      |
|--------|------------------|------------------------|-------------------|--------------|
| POST   | /customers        | Create new customer    | JSON (CustomerCreate) | CustomerOut |
| GET    | /customers        | Get all customers      | None              | List[CustomerOut] |
| GET    | /customers/{id}   | Get customer by ID     | None              | CustomerOut  |

---

## Products

| Method | Endpoint           | Description            | Request Body       | Response      |
|--------|-------------------|------------------------|-------------------|--------------|
| POST   | /products          | Create new product     | JSON (ProductCreate) | ProductOut |
| GET    | /products          | Get all products       | None              | List[ProductOut] |
| GET    | /products/{id}     | Get product by ID      | None              | ProductOut |
| PUT    | /products/{id}     | Update product by ID   | JSON (ProductCreate) | ProductOut |
| DELETE | /products/{id}     | Delete product by ID   | None              | JSON message |

---

## Orders

| Method | Endpoint         | Description            | Request Body       | Response      |
|--------|-----------------|------------------------|-------------------|--------------|
| POST   | /orders          | Create new order       | JSON (OrderCreate) | Order |
| GET    | /orders          | Get all orders         | None              | List[Order] |
| GET    | /orders/{id}     | Get order by ID        | None              | Order |
| PUT    | /orders/{id}     | Update order by ID     | JSON (OrderCreate) | Order |
| DELETE | /orders/{id}     | Delete order by ID     | None              | JSON message |

---

## Payments

| Method | Endpoint         | Description            | Request Body       | Response      |
|--------|-----------------|------------------------|-------------------|--------------|
| POST   | /payments        | Create new payment     | JSON (PaymentCreate) | Payment |
| GET    | /payments        | Get all payments       | None              | List[Payment] |
| GET    | /payments/{id}   | Get payment by ID      | None              | Payment |
| PUT    | /payments/{id}   | Update payment by ID   | JSON (PaymentCreate) | Payment |
| DELETE | /payments/{id}   | Delete payment by ID   | None              | JSON message |

---

## User Wishlist

| Method | Endpoint            | Description               | Request Body       | Response      |
|--------|--------------------|---------------------------|-------------------|--------------|
| POST   | /wishlist           | Add product to wishlist   | JSON (UserWishlistCreate) | UserWishlist |
| GET    | /wishlist/{user_id} | Get wishlist by user ID   | None              | List[UserWishlist] |
| DELETE | /wishlist/{id}      | Remove from wishlist      | None              | JSON message |

---

## 🤖 GPT Assistant

| Method | Endpoint     | Description            | Request Body       | Response      |
|--------|-------------|------------------------|-------------------|--------------|
| POST   | /ask-gpt     | Ask GPT a question      | JSON { "prompt": "..." } | GPT Response |

---

### Authentication
Currently, routes like `/customers` and `/wishlist` are **not protected** by authentication. Future versions may require a token.

---

### Notes
- All endpoints return JSON responses.
- Error responses include `detail` field with the error description.
- All data must be sent in UTF-8 encoded JSON.
