# Eclipse Software Help Desk

The Eclipse Software Help Desk is a lightweight web application built with Flask, SQLAlchemy, SCSS, and HTML. The application enables users to create, view, update, and manage support tickets in an organised and efficient way. Designed with responsiveness and usability in mind, the system is best suited for customer-facing environments.

## Features

- Create, view, edit, and delete tickets
- Facilitate communication between users with comments
- Secure registration and login with password hashing
- Responsive and accessible user interface styled with CSS and HTML
- Flash alerts for real-time feedback on user actions (success/error)
- Paginated ticket listings 
- Dynamic ticket forms with input validation
- Modular and maintainable codebase using Flask blueprints
- Built-in SQLite database managed via SQLAlchemy ORM (Object Relational Mapper)
- Clean separation of concerns between models, routes, and templates

## Technologies Used

- **Python 3** with **Flask**
- **SQLAlchemy** ORM with **SQLite**
- **Jinja2** 
- **CSS** 
- **HTML5**
- **JavaScript**

## Database
The system uses SQLAlchemy for ORM and SQLite as the default local database. 

## Architecture

This project follows the Model-View-Controller (MVC) design pattern:

- **Model**: Managed by SQLAlchemy in the `models/` directory, handling database schema and interactions.
- **View**: HTML templates rendered using Jinja2, located in the `templates/` directory.
- **Controller**: Flask route logic located in the `views/` directory, managing requests, input validation, and responses.

This separation of concerns ensures modularity, scalability, and ease of maintenance.

## Getting Started

### Prerequisites

Ensure Python 3 is installed. It is also recommended to use a virtual environment.

To create the virtual environment run the following in the terminal: 

py -m venv venv

To activate the virtual environment run the following in the terminal: 

venv\Scripts\activate

### Repository

Clone the repository which is located at: 

https://github.com/rcsgrv/EclipseSoftwareHelpDesk.git

### Install Dependencies

To install required packages run the following in the terminal: 

pip install --upgrade pip
pip install -r requirements.txt

### Environment Configuration

For security purposes, the .env file has not been committed.

1. Create a copy of the example file:

copy .env.example .env

2. Open .env and ensure that it contains:

SECRET_KEY=developmentsecretkey123
DATABASE_URL=sqlite:///EclipseSoftwareHelpDesk.db

This ensures that the application has a secret key and a database to connect to.

### Running the Application Locally

To start the Flask development server run the following in the terminal: 

py main.py

This will launch the application at:

http://127.0.0.1:5000/.

### Running the Application with Docker

If Docker is installed, run the following in the terminal:

docker build -t eclipsesoftwarehelpdesk .
docker run -p 5000:5000 eclipsesoftwarehelpdesk

This will launch the application at:

http://localhost:5000/

### Deployed Application

The application is currently hosted on Render and can be accessed via the following URL: 

### Seed Data

When the application is ran for the first time, seed data will be generated. This seed data consists of 10 users and 10 tickets. 

- The first 2 users have administrative access and will have the following credentials:
- - Email Address: user1@test.com
- - Password: Password1!

- The remaining 9 users have non-administrative access, following the same pattern:
- - Email: user{n}@test.com
- - Password: Password{n}!

Where {n} ranges from 3 to 10 (e.g. user3@test.com / Password3!, user4@test.com / Password4!, etc.).

### Two-Factor Authentication

To improve security, two-factor authentication has been implemented. Upon registration, users will be prompted to scan a QR code using Google Authenticator. Google Authenticator will provide a 6 digit code that should be inputted when a user logs in to the system.

The seed data user accounts will need to setup two-factor authentication before they can log in to the system. 

## Testing

The Eclipse Software Help Desk includes comprehensive integration tests covering key functionality such as user authentication, ticket creation, viewing, editing, deletion, and security features.

To run the tests locally, ensure your virtual environment is activated and dependencies are installed, then run the following in the terminal: 

$env:PYTHONPATH = "."
pytest tests

This will discover and run all tests in the `tests` directory and provide a detailed report of the results.

## Manual Testing

The application has been manually tested to ensure that all user interactions, including registration, login, ticket management, user management, and permissions, function as expected across typical use cases.

## Continuous Integration / Continous Deployment (CI/CD)

- Continuous Integration: Every push or pull request to main triggers GitHub Actions. This runs tests using Pytest, with coverage reports generated in XML format.
- Continuous Deployment: Upon successful tests, the pipeline automatically deploys the Dockerised application to Render.
- Docker: The application is containerised to ensure consistency between local and production environments.