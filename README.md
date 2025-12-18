# ALXBECAPSTONE

## PROJECT DESCRIPTION
- This is for the capstone project of my AlxBE COURSE.
- The project is DRF API for crypto portfolio management.

## PROJECT TOOLS AND TECH STACK
- **DRF** (Django REST Framework)
- **MySQL** (Database)
- **HTML** (Frontend markup)
- **CSS** (Styling)
- **Python** (Backend language)
- **Django** (Web framework)

## FEATURES
- User Registration and Authentication
- Portfolio Management
- Asset Tracking
- Transaction History
- Real-time Cryptocurrency Data Integration
- Responsive Design

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
- Asset Tracking: `/api/assets/`
- Transaction History: `/api/transactions/`
- Real-time Cryptocurrency Data: `/api/crypto-data/`







