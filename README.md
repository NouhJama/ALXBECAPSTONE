# ALXBECAPSTONE

## PROJECT DESCRIPTION
- This is for the capstone project of my AlxBE COURSE.
- The project is DRF API for crypto portfolio management.

## PROJECT TOOLS AND TECH STACK
- **DRF** (Django REST Framework)
- **MySQL** (Database)
- **Python** (Backend language)
- **Django** (Web framework)
- **CoinGecko API** (For real-time cryptocurrency data)
- **DRF Token Authentication** (For secure API access)
- **DRF Nested Routers** (For nested resource routing)
- **Python Decouple** (For environment variable management)
- **Pillow** (For image handling, if needed)
- **Render or Heroku** (For deployment)


## FEATURES
- User Registration and Authentication.✅
- Portfolio Management✅
- Asset Tracking.✅
- Transaction History.✅
- Real-time Cryptocurrency Data Integration.✅
- Admin Interface for Managing Users and Portfolios.✅
- CRUD Operations for Portfolios, Assets, and Transactions.✅
- Token-based Authentication.✅
- Secure API Endpoints with Permissions.✅
- Data Validation and Error Handling.✅
- External API Integration with CoinGecko for live.cryptocurrency prices.✅
- Price snapshots per transaction to maintain historical accuracy
- Caching of cryptocurrency data to reduce API calls and improve performance.✅
- Pagination for large datasets.
- Portfolio performance analytics (e.g., total value, profit/loss calculations).✅
- Comprehensive API documentation using tools like Swagger or DRF's built-in documentation features.
- Unit and integration tests to ensure code quality and reliability.
- RENDER deployment for easy access and scalability.

## SETUP AND INSTALLATION
1. Clone the repository:
   ```bash
   git clone    

## Authentication
- Token-based authentication using DRF's built-in token authentication system.
- Default permission classes set to IsAuthenticated to ensure secure access to API endpoints.   
2. Navigate to the project directory:
   ```bash
   cd crypto_api_project
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
    ```

5. Apply migrations to set up the database:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Endpoints
- User Registration: `/api/register/`
- User Login: `/api/login/`
- Portfolio Management: `/api/portfolios/`
- Asset Tracking: `/api/portfolios/<portfolio_pk>/assets/`
- Transaction History per Asset: `/api/portfolios/<portfolio_pk>/assets/<asset_pk>/transactions/`
- All Transactions per Portfolio: `/api/portfolios/<portfolio_pk>/transactions/`

## NB
- Transaction deletion is not allowed to maintain data integrity and accurate portfolio tracking.







