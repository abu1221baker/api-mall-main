# API Mall - Django REST API

A complete e-commerce REST API built with Django and Django REST Framework, featuring JWT authentication, product management, order processing, and wishlist functionality.

## 🚀 Features

- **User Authentication**: JWT-based authentication with registration and login
- **Profile Management**: User profile CRUD operations with security controls
- **Product Catalog**: Full product management (CRUD operations)
- **Order System**: Order creation with automatic stock management and status tracking
- **Wishlist**: Add/remove products to/from wishlist
- **API Documentation**: Interactive HTML documentation page

## 📋 API Endpoints

### Authentication
- `POST /api/accounts/login/` - Login and get JWT tokens
- `POST /api/accounts/profiles/` - Register new user

### Profiles
- `GET /api/accounts/profiles/` - Get current user profile
- `GET /api/accounts/profiles/{id}/` - Get profile by ID (own only)
- `PUT /api/accounts/profiles/{id}/` - Update profile (own only)
- `DELETE /api/accounts/profiles/{id}/` - Delete profile (own only)

### Products
- `GET /api/products/products/` - List all products
- `POST /api/products/products/` - Create product
- `GET /api/products/products/{id}/` - Get product details
- `PUT /api/products/products/{id}/` - Update product
- `DELETE /api/products/products/{id}/` - Delete product

### Orders
- `GET /api/products/orders/` - List user's orders
- `POST /api/products/orders/` - Create order (auto stock decrement)
- `GET /api/products/orders/{id}/` - Get order details
- `PUT /api/products/orders/{id}/` - Update order status
- `DELETE /api/products/orders/{id}/` - Cancel order

### Wishlist
- `GET /api/products/wishlist/` - List wishlist items
- `POST /api/products/wishlist/` - Add to wishlist
- `GET /api/products/wishlist/{id}/` - Get wishlist item
- `DELETE /api/products/wishlist/{id}/` - Remove from wishlist

## 🛠️ Tech Stack

- **Framework**: Django 5.0.1
- **API**: Django REST Framework 3.14.0
- **Authentication**: djangorestframework-simplejwt 5.3.1
- **CORS**: django-cors-headers 4.3.1
- **Database**: PostgreSQL (production) / SQLite (development)
- **Server**: Gunicorn 21.2.0
- **Static Files**: WhiteNoise 6.6.0

## 📦 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/api-mall.git
   cd api-mall/newproject
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the API**
   - API Documentation: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/

## 🌐 Deployment

See [deployment_guide.md](deployment_guide.md) for detailed instructions on deploying to Render.

### Quick Deploy to Render

1. Push code to GitHub
2. Create PostgreSQL database on Render
3. Create Web Service on Render
4. Set environment variables:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS`
   - `DATABASE_URL`
5. Deploy!

## 🔐 Security Features

- JWT token authentication
- Password hashing with Django's built-in system
- User ownership validation on resources
- CORS protection
- HTTPS enforcement in production
- Secure cookie settings
- XSS and CSRF protection

## 📝 Environment Variables

Create a `.env` file based on `.env.example`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost
DATABASE_URL=postgresql://user:pass@host:port/db
```

## 🧪 Testing

```bash
python manage.py test
```

## 📄 License

This project is open source and available under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Django**
