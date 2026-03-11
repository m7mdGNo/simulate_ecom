# Frontend API Documentation

## Base URLs
- API base: `http://localhost:8001/api/`
- Swagger UI: `http://localhost:8001/api/swagger/`
- ReDoc: `http://localhost:8001/api/redoc/`

## Authentication
The API uses DRF token auth.

### Login
- `POST /api/accounts/login/`
- Body:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
- Success response:
```json
{
  "id": 1,
  "token": "<TOKEN>"
}
```

### Auth Header
Send this header for protected endpoints:
- `Authorization: Token <TOKEN>`

## Permission Rules Summary
- Accounts:
  - Register is public.
  - Authenticated users can only read/update their own account.
  - Admin can read/update all users.
- Products:
  - `GET` is public.
  - `POST/PUT/PATCH/DELETE` is admin only.
- Cart:
  - Auth required.
  - Non-admin sees only own cart rows.
  - Admin sees all rows.
- Orders + Order Items:
  - Auth required.
  - Non-admin sees only own orders/order items.
  - Admin sees all.
- Blogs:
  - Auth required.
  - Non-admin sees only own blogs.
  - Admin sees all.

---

## Accounts API

### Register User
- `POST /api/accounts/`
- Content type: `multipart/form-data` (because of image support)
- Fields:
  - `first_name` (string)
  - `last_name` (string)
  - `email` (string, unique)
  - `phone_number` (string)
  - `country` (string, optional)
  - `image` (file, optional)
  - `password` (string)
- Response includes created user fields and `token`.

### List Users
- `GET /api/accounts/`
- Non-admin: returns only current user in array.
- Admin: returns all users.

### Get User
- `GET /api/accounts/{id}/`

### Update User
- `PUT /api/accounts/{id}/`
- `PATCH /api/accounts/{id}/`

### Delete User
- `DELETE /api/accounts/{id}/`

---

## Products API

### List Products (Public)
- `GET /api/products/`

### Get Product (Public)
- `GET /api/products/{id}/`

### Create Product (Admin only)
- `POST /api/products/`
- Body example:
```json
{
  "name": "Tomato",
  "category": "Vegetables",
  "description": "Fresh tomato"
}
```
- Optional: `image` (file)

### Update Product (Admin only)
- `PUT /api/products/{id}/`
- `PATCH /api/products/{id}/`

### Delete Product (Admin only)
- `DELETE /api/products/{id}/`

---

## Cart API
Model shape: `user`, `product`, `quantity`, `created_at`, `updated_at`.

### List Cart Rows
- `GET /api/cart/`

### Create Cart Row
- `POST /api/cart/`
- Body example:
```json
{
  "product": 1,
  "quantity": 2
}
```
- Note: backend always assigns `user` from auth token.

### Get Cart Row
- `GET /api/cart/{id}/`

### Update Cart Row
- `PUT /api/cart/{id}/`
- `PATCH /api/cart/{id}/`

### Delete Cart Row
- `DELETE /api/cart/{id}/`

---

## Orders API
Order shape: `user`, `address`, `created_at`, `updated_at`.

### List Orders
- `GET /api/orders/`

### Create Order
- `POST /api/orders/`
- Body example:
```json
{
  "address": "123 Main St"
}
```
- Note: backend always assigns `user` from auth token.

### Get Order
- `GET /api/orders/{id}/`

### Update Order
- `PUT /api/orders/{id}/`
- `PATCH /api/orders/{id}/`

### Delete Order
- `DELETE /api/orders/{id}/`

---

## Order Items API
OrderItem shape: `order`, `product`, `quantity`.

### List Order Items
- `GET /api/orders/items/`

### Create Order Item
- `POST /api/orders/items/`
- Body example:
```json
{
  "order": 1,
  "product": 1,
  "quantity": 3
}
```

### Get Order Item
- `GET /api/orders/items/{id}/`

### Update Order Item
- `PUT /api/orders/items/{id}/`
- `PATCH /api/orders/items/{id}/`

### Delete Order Item
- `DELETE /api/orders/items/{id}/`

---

## Blogs API
Blog shape: `user`, `name`, `content`, `thumbnail`, `created_at`, `updated_at`.

### List Blogs
- `GET /api/blogs/`

### Create Blog
- `POST /api/blogs/`
- Body example:
```json
{
  "name": "My First Blog",
  "content": "Blog content here"
}
```
- Optional: `thumbnail` (file)
- Note: backend always assigns `user` from auth token.

### Get Blog
- `GET /api/blogs/{id}/`

### Update Blog
- `PUT /api/blogs/{id}/`
- `PATCH /api/blogs/{id}/`

### Delete Blog
- `DELETE /api/blogs/{id}/`

---

## Frontend Integration Notes
- For file uploads (`image`, `thumbnail`), use `multipart/form-data`.
- For JSON endpoints, use `application/json`.
- On 401 responses, redirect user to login and clear local token.
- Keep token in a secure client store and attach to all protected requests.
