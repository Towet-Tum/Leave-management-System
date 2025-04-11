# Leave-management-System
## This is a wep application for Leave Management System for corporate offices.
## Features


- **Employee Management**
  - **Register:** Create a new employee account.
  - **Login:** Authenticate using JWT (SimpleJWT).
  - **Logout:** Securely log out by invalidating tokens.

- **Leave Application**
  - **Leave Credit:** Each employee is credited 2 day leave by default each month
  - **Apply Leave:** Authenticated employee can apply for a leave.
  - **Leave Type:** Leave type should be available for employees to choose from.
  - **Approval:** Each applied leave should be approved by the supervisor.
  - **Automatic Approval:** Automatic approval should be provided on applied leave it is not disapproved by the supervisor before 24 hours of leave date.
  - **Days Conversion:** After every year if employe has more than 22 left. All leave above 22 days should  be converted into money and employee should be able to claim that money into
    their saving account.
   



- **Background Processing & Caching**
  - **Celery:** Handle asynchronous tasks such as schedulling credit awards, credit convertion and automatic aproval.
  - **Redis:** Used as a message broker for Celery and for caching purposes.

## Tech Stack

- **Backend Framework:** Django, Django REST Framework
- **Authentication:** SimpleJWT
- **Asynchronous Tasks:** Celery
- **Caching & Messaging:** Redis
- **Database:** PostgreSQL 

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- Redis
- Virtual environment tool (e.g., `venv` or `pipenv`)

### Clone the Repository

```bash
git clone https://github.com/Towet-Tum/Leave-Management-System
cd Leave-Management-System
```

### Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```


### Environment Configuration

Create a .env file in the project root and configure the following variables:
```bash 
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres url
REDIS_URL=redis port
```

### Database Setup

Run the migrations to create the database schema:
```bash 
python manage.py makemigrations
python manage.py migrate
```

### Create an Admin User

Create a superuser account for administrative tasks 
```bash 
python manage.py createsupueruser
```

### Running the Application
Start the Django Server
```bash 
python manage.py runserver
``` 

### Start the Celery Worker and Celery Beat

In a separate terminal, run:
```bash
celery -A leave_service worker -l info
```
In a separate terminal, run:
```bash 
celery -A leave_service beat --loglevel=info
```

## API Endpoints
### Employee Endpoints

Register:

Create a new employee account.

    POST /api/register/



Login:

Authenticate and receive a JWT access token.

    POST /api/login/



Logout:

Invalidate the JWT token to log out.

    POST /api/logout/

Profile:

Views your profile.

    GET /api/employee/id/


### Leave Application Endpoints


Apply for a leave:

Enable employee to apply for a leave if they have not exahusted the available leave credits

Apply for leave:

    POST /api/leave/

Fetch Your leave applications:

    GET /api/leave/id/

Update your leave application if not approved:

    PUT /api/leave/id/

Delete your leave application if not approved:

    DELETE api/leave/id/


### Testing

Run the test suite to verify the functionality of the API:
```bash
python manage.py test
```

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss what you would like to change.
License

#### This project is licensed under the MIT License. See the LICENSE file for details.