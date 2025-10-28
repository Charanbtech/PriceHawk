# 🦅 PriceHawk - Smart Price Tracking Platform

PriceHawk is a full-stack web application that helps users track product prices across multiple e-commerce platforms, get notified when prices drop, and make informed purchasing decisions.

## 🚀 Features

- **Smart Product Search**: Search products across multiple platforms
- **Price Tracking**: Track your favorite products and set target prices
- **Price Drop Alerts**: Get notified via email when prices drop
- **Historical Analysis**: View price history and trends
- **Price Forecasting**: AI-powered price predictions using Prophet
- **User Dashboard**: Comprehensive overview of tracked products and savings
- **Responsive Design**: Works seamlessly on desktop and mobile

## 🏗️ Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: MongoDB Atlas
- **Authentication**: JWT with Flask-JWT-Extended
- **Background Jobs**: APScheduler
- **Price Forecasting**: Prophet (Facebook's time series forecasting)
- **Server**: Gunicorn (production)

### Frontend
- **Framework**: React.js
- **Routing**: React Router
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Icons**: Lucide React
- **Server**: Nginx (production)

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: MongoDB Atlas (cloud)
- **Email**: SMTP (Gmail)

## 📦 Installation & Setup

### Prerequisites
- Docker & Docker Compose
- MongoDB Atlas account (or local MongoDB)
- Gmail account for email notifications

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pricehawk
```

### 2. Environment Configuration

#### Backend Configuration
Copy the example environment file and configure:
```bash
cp backend/.env.example .env
```

Edit `.env` with your configuration:
```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here
JWT_SECRET=your-jwt-secret-key-here
PORT=5000

# MongoDB Configuration
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/pricehawk

# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_EMAIL_PASSWORD=your-gmail-app-password
```

#### Frontend Configuration
The frontend is already configured to connect to `http://localhost:5000/api`. If you need to change this, edit `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:5000/api
```

### 3. Run with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/health

## 🔧 Development Setup

### Backend Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/verify` - Verify JWT token

### Product Search
- `POST /api/search` - Search products across platforms

### Product Tracking
- `GET /api/tracking/products` - Get tracked products
- `POST /api/tracking/track` - Start tracking a product
- `DELETE /api/tracking/untrack/{id}` - Stop tracking a product
- `PATCH /api/tracking/preferences/{id}` - Update tracking preferences

### Notifications
- `GET /api/notifications` - Get user notifications
- `GET /api/notifications/unread_count` - Get unread count
- `PATCH /api/notifications/{id}/read` - Mark as read
- `DELETE /api/notifications/{id}` - Delete notification

### Price History & Forecasting
- `GET /api/tracking/history/{id}` - Get price history
- `GET /api/tracking/forecast/{id}` - Get price forecast
- `GET /api/tracking/analysis/{id}` - Get price analysis

## 🎯 Usage Guide

### 1. Register/Login
- Create an account or login with existing credentials
- JWT tokens are used for authentication

### 2. Search Products
- Use the search page to find products
- Currently uses mock data for demonstration
- Real adapters can be integrated for Amazon, Flipkart, etc.

### 3. Track Products
- Click "Track Price" on any search result
- Set your target price
- Enable notifications for price drops

### 4. Monitor Dashboard
- View your tracked products
- See price drop alerts
- Monitor total savings

### 5. Manage Notifications
- Check notifications for price drops
- Mark as read or delete
- Send test email notifications

## 🔌 Extending PriceHawk

### Adding New E-commerce Adapters

1. Create a new adapter in `backend/adapters/`:
```python
from .base import BaseAdapter

class AmazonAdapter(BaseAdapter):
    def search(self, query: str, max_results: int = 10):
        # Implement Amazon product search
        pass
    
    def fetch_product(self, url: str):
        # Implement single product fetch
        pass
```

2. Register the adapter in `backend/api/search.py`:
```python
ADAPTERS = {
    "mock": DevMockAdapter(),
    "amazon": AmazonAdapter(),
    # Add your new adapter
}
```

### Adding New Notification Channels

1. Extend the notification service in `backend/services/notifications.py`
2. Add new notification types in the schemas
3. Implement the delivery mechanism (SMS, Push, etc.)

## 🚀 Deployment

### Production Deployment with Docker

1. Update environment variables for production
2. Use production MongoDB Atlas cluster
3. Configure proper email credentials
4. Deploy using Docker Compose:

```bash
# Production deployment
docker-compose -f docker-compose.yml up -d --build
```

### Environment Variables for Production
```env
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
JWT_SECRET=your-production-jwt-secret
MONGO_URI=mongodb+srv://prod-user:password@prod-cluster.mongodb.net/pricehawk
SENDER_EMAIL=notifications@yourdomain.com
SENDER_EMAIL_PASSWORD=your-production-email-password
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Monitoring & Logging

- Application logs are available via Docker logs
- MongoDB Atlas provides database monitoring
- Health check endpoint: `/health`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check your MONGO_URI in .env
   - Ensure MongoDB Atlas allows connections from your IP
   - Verify username/password

2. **Email Notifications Not Working**
   - Use Gmail App Passwords, not regular password
   - Enable 2FA on Gmail account
   - Check SENDER_EMAIL and SENDER_EMAIL_PASSWORD

3. **Frontend Can't Connect to Backend**
   - Ensure backend is running on port 5000
   - Check REACT_APP_API_URL in frontend/.env
   - Verify CORS configuration

4. **Docker Build Issues**
   - Clear Docker cache: `docker system prune -a`
   - Rebuild without cache: `docker-compose build --no-cache`

### Getting Help

- Check the logs: `docker-compose logs backend` or `docker-compose logs frontend`
- Ensure all environment variables are set correctly
- Verify all services are running: `docker-compose ps`

## 🔮 Future Enhancements

- [ ] Real-time price updates with WebSockets
- [ ] Mobile app (React Native)
- [ ] Advanced price prediction models
- [ ] Social features (share deals, wishlists)
- [ ] Browser extension for quick price tracking
- [ ] Integration with more e-commerce platforms
- [ ] Advanced analytics and reporting
- [ ] Price comparison charts
- [ ] Deal recommendations based on user preferences

---

**Happy Price Tracking! 🦅💰**