# ALXBECAPSTONE


## PROJECT TITLE
- Crypto Portfolio Management API

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
- Pagination for large datasets.✅
- Portfolio performance analytics (e.g., total value, profit/loss calculations).✅
- Unit and integration tests to ensure code quality and reliability.✅

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

7. Configure environment variables:
   - Create a `.env` file in the project root and add the necessary environment variables (e.g., SECRET_KEY, DATABASE settings). 

9. Obtain a CoinGecko API key (if required) and add it to your environment variables.

10. (Optional) Configure caching settings in `settings.py` if using caching.

8. Run the development server:
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
- Upgrade to use JWT authentication for better security.
- Portfolio level analytics and reporting.
- Frontend integration using React or Vue.js.
- Mobile app integration for on-the-go portfolio management.
- Python Unittest and integration tests to ensure code quality and reliability.
- Redis caching for improved performance.
- Dockerize the application for easier deployment and scalability.
- CI/CD pipeline setup for automated testing and deployment.
- API rate limiting to prevent abuse.
- Detailed API documentation using Swagger or ReDoc.
- AWS or GCP deployment for better scalability and reliability.










