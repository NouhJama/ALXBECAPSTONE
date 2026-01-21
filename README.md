# ALXBECAPSTONE


## PROJECT TITLE
- Crypto Portfolio Management API🌐

## 📽️AUTHOR
- Nouh Ali
-GitHub: https://github.com/NouhJama/ALXBECAPSTONE

## PROJECT DESCRIPTION
-# Crypto Portfolio Management API
- This is for the capstone project of my AlxBE COURSE.
- The project is DRF API for crypto portfolio management.
- It allows users to register, create and manage their cryptocurrency portfolios, track assets, and record transactions.
- The API integrates with the CoinGecko API to fetch real-time cryptocurrency data.

## PROJECT TOOLS AND TECH STACK
- **DRF** (Django REST Framework)
- **MySQL** (Local dev Database)
- **PostgreSQL** (Production Database)
- **Python** (Backend language)
- **Django** (Web framework)
- **CoinGecko API** (For real-time cryptocurrency data)
- **DRF Token Authentication** (For secure API access)
- **DRF Nested Routers** (For nested resource routing)
- **Python Decouple** (For environment variable management)
- **Pillow** (For image handling, if needed)
- **Docker & Docker Compose** (For containerization)
- **Render or Heroku** (For deployment)
- **Render Redis** (For caching, optional)


## FEATURES
- User Registration and Authentication.✅
- Portfolio Management✅
- Asset Tracking.✅
- Transaction History.✅
- Real-time Cryptocurrency Data Integration.✅
- Admin Interface for Managing Users and Portfolios.✅
- CRUD Operations for Portfolios, Assets, and Transactions.✅
- Secure API Endpoints with  custom Permissions.✅
- Data Validation and Error Handling.✅
- External API Integration with CoinGecko for live.cryptocurrency prices.✅
- Price snapshots per transaction to maintain historical accuracy
- Caching of cryptocurrency data to reduce API calls and improve performance.✅
- JWT Authentication for enhanced security.✅
- Throttling to prevent abuse of API endpoints.✅
- Pagination for large datasets.✅
- Portfolio performance analytics (e.g., total value, profit/loss calculations).✅
- Unit and integration tests to ensure code quality and reliability.✅
- Dockerized application for easy deployment.✅
- Render deployment for easy access and scalability.✅

<!-- ## 🚀SETUP AND INSTALLATION -->
### PRE-REQUISITES
- Python 3.11 or higher
- pip (Python package installer)
- Git
- Docker and Docker Compose (for containerization, optional)
- PostgreSQL database (for production)
- CoinGecko API key (if required for higher rate limits)
### SETUP AND INSTALLATION
1. Clone the repository:
   ```bash
   git clone https://github.com/NouhJama/ALXBECAPSTONE.git
   cd ALXBECAPSTONE
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create environment variables:
   - Create a `.env` file in the project root and add the necessary environment variables (e.g., SECRET_KEY, DATABASE settings).
5. Start the docker containers:
   ```bash
   docker-compose up --build -d
   ```
**What does this do?**
- ✅Builds the Docker images and starts the containers for the application and database.
- ✅Runs database migrations to set up the database schema.
- ✅Creates a superuser for accessing the Django admin interface.
- ✅Collects static files for production use.

========================================
Starting the Gunicorn server...
========================================
[info] Listening on: http://0.0.0.0:8000
========================================

### AUTHENTICAITON AND API Access
 - The API endpoints are secured using token-based authentication.
 - Users must register and obtain an authentication token to access the API.
 - Include the token in the `Authorization` header of your requests as follows:
 - If you visit the base URL in browser or incognito mode you may see a response like this:
   ```json
   {
     "detail": "Authentication credentials were not provided."
   }
 - This is a normal a normal and expected behavior since the API requires authentication for access.

   ```
   Authorization

## Endpoints
- User Registration: `/api/register/`
- User Login: `/api/login/`
- Portfolio Management: `/api/portfolios/`
- Asset Tracking: `/api/portfolios/<portfolio_pk>/assets/`
- Transaction History per Asset: `/api/portfolios/<portfolio_pk>/assets/<asset_pk>/transactions/`
- All Transactions per Portfolio: `/api/portfolios/<portfolio_pk>/transactions/`

## NB
- Transaction deletion is not allowed to maintain data integrity and accurate portfolio tracking.

## TESTING
- To run the tests, use the following command:
   ```bash
   python manage.py test
   ```

## CONTRIBUTING
- Contributions are welcome! Please fork the repository and create a pull request with your changes.

## FUTURE ENHANCEMENTS
- Implement advanced analytics and reporting features.
- Enhance security measures, such as two-factor authentication.
- Improve the user interface for better usability.
- Portfolio level analytics and reporting.
- Frontend integration using React or Vue.js.
- Mobile app integration for on-the-go portfolio management.
- Python Unittest and integration tests to ensure code quality and reliability.
- CI/CD pipeline setup for automated testing and deployment.
- Detailed API documentation using Swagger or ReDoc.











