# Eclipse Software Help Desk

The Eclipse Software Help Desk is a lightweight web application that enables users to create, view, update, and manage support tickets in an organised and efficient manner. Designed with responsiveness and usability in mind, the system is best suited for customer-facing environments.

## Features

- Create, view, edit, and delete tickets
- Facilitate communication between users with comments
- Secure registration and login with password hashing and two-factor authentication (2FA)
- Role-base access control (RBAC) to enhance security by enforcing the principle of least privilege
- User management allowing for the promotion/demotion of administrative status
- Responsive and accessible user interface designed with CSS, HTML, and JavaScript
- Flash alerts for real-time feedback on user actions
- Dynamic ticket forms with input validation
- Modular and maintainable codebase using Flask blueprints
- Built-in SQLite database managed via SQLAlchemy ORM
- Clean separation of concerns between models, routes, and templates
- Integration tests covering core functionality developed using Pytest

## Getting Started

### Prerequisites

Ensure Python 3 is installed (https://www.python.org/downloads/). 

### Repository

Clone the repository which is located at: 

https://github.com/rcsgrv/EclipseSoftwareHelpDesk.git

### Virtual Environment

Create a virtual environment by running the following in the terminal: 

py -m venv venv

To activate the virtual environment run the following in the terminal: 

venv\Scripts\activate

### Install Dependencies

Install required packages by running the following in the terminal: 

pip install --upgrade pip
pip install -r requirements.txt

### Environment Configuration

For security purposes, the .env file has not been committed. A copy of .env.example will need to be created and placed in a .env file by running the following in the terminal:

copy .env.example .env

Once the .env file is created, open it and verify that it contains:

SECRET_KEY=developmentsecretkey123
DATABASE_URL=sqlite:///developmentdatabase.db

This ensures that the application has a secret key and a database to connect to.

### Running the Application Locally

To start the Flask development server run the following in the terminal: 

py main.py

This will launch the application at:

http://127.0.0.1:5000/.

### Running the Application with Docker

If Docker Desktop is installed, run the following in the terminal:

docker build -t eclipsesoftwarehelpdesk .
docker run -p 5000:5000 eclipsesoftwarehelpdesk

This will launch the application at:

http://localhost:5000/

### Deployed Application

The application is currently hosted on Render and can be accessed via the following URL: 

https://eclipsesoftwarehelpdesk.onrender.com

### Seed Data

When the application is ran for the first time, seed data will be generated. This seed data consists of 10 users, 10 tickets, and 10 comments. 

- The first 2 users have administrative access and will have the following credentials:
- - Email Address: user{n}@recruitment-software.co.uk
- - Password: Password{n}!

Where {n} ranges from 1 to 2 (e.g. user1@test.com / Password1! and user2@test.com / Password2!).

- The remaining 9 users have non-administrative access and will have the following credentials:
- - Email: user{n}@recruitment-software.co.uk
- - Password: Password{n}!

Where {n} ranges from 3 to 10 (e.g. user3@test.com / Password3!, user4@test.com / Password4!, etc.).

### Two-Factor Authentication

To improve security, two-factor authentication has been implemented. Upon registration, users will be prompted to scan a QR code using Google Authenticator. Google Authenticator will provide a 6 digit code that should be inputted when a user logs in to the system.

The seed data user accounts will be required to setup two-factor authentication before they can log in to the system. 

## Testing

### Integration Testing

The Eclipse Software Help Desk includes comprehensive integration tests covering ticket management and user management, in addition to application security features. 

To run these tests locally, ensure that your virtual environment is activated and dependencies are installed, then run the following in the terminal: 

$env:PYTHONPATH = "."

pytest -v

This will discover and run all tests in the `tests/` directory and provide a detailed report of the results.

### Manual Testing

The application has been manually tested to ensure that all user interactions, including registration, login, ticket management, user management, and permissions, function as expected across typical use cases.