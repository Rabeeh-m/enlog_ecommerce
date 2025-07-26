# E-commerce API

This is a Django REST API for a small e-commerce system built with Django, Django REST Framework, PostgreSQL, Redis, and Django Channels. It supports user authentication (JWT-based), product and category management, order processing, caching, pagination, filtering, and real-time order status notifications via WebSockets.

## Features
### User Authentication:
- Register and login with JWT (access and refresh tokens)
### Product Management:
- Create, update, delete categories and products (admin only)
- Browse products with pagination and filtering (by category, price range, stock availability)- File uploads for book PDFs and cover images
- Automatic stock updates on order placement
### Order System:
- Add products to cart and place orders
- Order status transitions (Pending → Shipped → Delivered)
### Caching & Optimization:
- Redis caching for products and categories (1-hour TTL)
- Cache invalidation on product/category updates
- Optimized queries with select_related and prefetch_related
### Pagination & Filtering:
- Paginated product lists (10 items per page)
- Filter by category, price range, and stock status
### Real-Time Notifications:
- WebSocket notifications for order status updates using Django Channels


## Tech Stack
- Backend: Django, Django REST Framework
- Authentication: Django REST Framework SimpleJWT
- Database: PostgreSQL
- Caching: Redis
- WebSockets: Django Channels with Redis backend
- ASGI Server: Uvicorn
- Testing: Postman (HTTP and WebSocket)


## Prerequisites
- Python 3.8+
- PostgreSQL
- Redis
- Postman (for testing)

## Setup Instructions

### 1. Clone the Repository
```bash
  git clone https://github.com/Rabeeh-m/enlog_ecommerce.git
  cd enlog_ecommerce
```

### 2. Create a Virtual Environment
```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
  pip install -r requirements.txt
```

### 4. Configure Environment Variables
```
  DEBUG=True
  SECRET_KEY=your-secret-key-here
  DATABASE_ENGINE=django.db.backends.postgresql
  DATABASE_NAME=your-database-name
  DATABASE_USER=your-your-database-username
  DATABASE_PASSWORD=your-database-password
  DATABASE_HOST=localhost
  DATABASE_PORT=5432
```

### 5. Apply Migrations
```bash
  python manage.py makemigrations
  python manage.py migrate
```

### 6. Create a Superuser (Optional)
```bash
  python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
  python manage.py runserver
```

### 8. Run Services:
```bash
  redis-server
  sudo service postgresql start
  uvicorn ecommerce.asgi:application --host 0.0.0.0 --port 8000
```


## API Endpoints

```
enlog_ecommerce/
├── enlog_ecommerce/
│   ├── asgi.py              # ASGI configuration for WebSockets
│   ├── settings.py          # Project settings (DB, cache, JWT, Channels)
│   ├── urls.py              # API routes
│   └── wsgi.py
├── store/
│   ├── migrations/          # Database migrations
│   ├── consumers.py         # WebSocket consumer for order notifications
│   ├── models.py            # Models (Category, Product, UserProfile, Order, OrderItem)
│   ├── serializers.py       # Serializers for API data
│   ├── views.py             # API views and endpoints
│   └── urls.py
├── manage.py                # Django management script
└── README.md
```

## API Endpoints
```
## API Endpoints

| Endpoint                    | Method                 | Description                | Authentication            |
|-----------------------------|------------------------|----------------------------|---------------------------|
| `/api/register/`            | POST                   | Register a new user        | None                      |
| `/api/token/`               | POST                   | Obtain JWT tokens          | None                      |
| `/api/token/refresh/`       | POST                   | Refresh access token       | None                      |
| `/api/profile/`             | GET, PUT               | Manage user profile        | JWT                       |
| `/api/categories/`          | GET, POST, PUT, DELETE | Manage categories          | Admin (POST, PUT, DELETE) |
| `/api/products/`            | GET, POST, PUT, DELETE | Manage products            | JWT, Admin (write ops)    |
| `/api/orders/`              | GET                    | View order history         | JWT                       |
| `/api/orders/create_order/` | POST                   | Create an order            | JWT                       |
| `/ws/orders/`               | WebSocket              | Order status notifications | JWT                       |

```


## Contributing
- Fork the repository.
- Create a feature branch (git checkout -b feature-name).
- Commit changes (git commit -m "Add feature").
- Push to the branch (git push origin feature-name).
- Open a pull request.
