# Investment Management API

This Django REST Framework application manages investment accounts, user permissions, and transactions. It includes authentication, CRUD operations for investment accounts, and admin features for assigning permissions.

## Features

- User authentication with JWT tokens
- CRUD operations for investment accounts
- Assign user permissions to investment accounts
- Manage and track transactions
- Admin-only endpoints for user management and transactions

## Setup

### Prerequisites

- Python 3.8 or later
- Pip

### Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd investment_management
   ```

Install Dependencies

### Set Up PostgreSQL Database

Install PostgreSQL if you don't have it already.

Create a database

```
psql
CREATE DATABASE investment_db;
```

### Update `settings.py` with your PostgreSQL credentials:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'investment_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Apply Migrations

```
python manage.py migrate

```

### Run the Development Server

```
python manage.py runserver
```

## API Endpoints

##### Authentication

* **User Registration** : `POST /api/signup/`
* **Admin Registration** : `POST /api/admin/signup/`
* **User Login** : `POST /api/login/`
* **Admin Login** : `POST /api/admin/login/`

### Investment Accounts

* **List All Accounts (Admin Only)** : `GET /api/investment-accounts/`
* **Create Account (Admin Only)** : `POST /api/investment-accounts/`
* **Retrieve Account** : `GET /api/investment-accounts/<int:pk>/`
* **Update Account (Admin Only)** : `PUT /api/investment-accounts/<int:pk>/`
* **Delete Account (Admin Only)** : `DELETE /api/investment-accounts/<int:pk>/`

### User Permissions

* **Assign User to Account (Admin Only)** : `POST /api/investment-accounts/<int:account_id>/assign-user/`
* **List Permissions (Admin Only)** : `GET /api/permissions/`
* **Modify Permissions** : `PUT /api/permissions/<int:pk>/`
* **Delete Permissions** : `DELETE /api/permissions/<int:pk>/`

### Transactions

* **List Transactions for an Account** : `GET /api/investment-accounts/<int:pk>/transactions/`
* **Create a Transaction** : `POST /api/investment-accounts/<int:pk>/transactions/`
* **Retrieve Transactions for a User** : `GET /users/<str:username>/transactions/`
* **Admin View of User Transactions** : `GET /users/<str:username>/transactions/?start=<YYYY-MM-DD>&end=<YYYY-MM-DD>`

### Permissions System

* **View Permission** : Users with this permission can view account details.
* **CRUD Permission** : Users with this permission can modify account details.
* **Post Permission** : Users with this permission can post new transactions.

### Custom Permission Classes:

1. **IsAccountOwnerOrAdmin** : Grants access if the user is the owner of the account or an admin.
2. **IsAccountViewer** : Grants access if the user has view permission on the account.
3. **IsAccountCRUDUser** : Grants access if the user has CRUD permission on the account.
4. **IsTransactionPoster** : Grants access if the user has post permission for transactions.

## Running Unit Tests

To run the test suite, use:

```
python manage.py test

```

## Contact

For any questions or feedback, please contact **Ian Chemweno** at [chemwenokibet11@gmail.com]().
