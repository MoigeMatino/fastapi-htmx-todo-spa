# FastAPI + HTMX Task Management SPA

A simple Todo application built with FastAPI, HTMX, and Jinja2 templates. This app allows users to create, update, toggle, and delete todo items. It also incorporates JWT authentication to secure access and modern styling for a simple, clean, and visually appealing user interface.

## Table of Contents

- [Unique Approach](#unique-approach)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
  - [Stopping the App](#stopping-the-app)
  - [Testing the App](#testing-the-app)
- [File Descriptions](#file-descriptions)
- [Usage](#usage)
- [API Documentation](#api-documentation)

## Unique Approach

This project demonstrates a unique approach to building web applications by combining FastAPI with HTMX. By leveraging HTMX, the app provides a highly dynamic user experience with real-time updates directly in the browser without requiring full page reloads. Additionally, JWT (JSON Web Token) authentication is integrated to manage user sessions securely. This approach showcases how modern libraries can be integrated to create responsive, efficient, and secure web applications, even for seemingly simple tasks like managing a Todo list.

## Features

- Create new todo items.
- Update the title of existing todo items.
- Toggle the completion status of todo items.
- Delete todo items.
- Real-time updates with HTMX.
- JWT authentication for secure access.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **HTMX**: A library that allows you to access modern browser features directly from HTML.
- **Jinja2**: A templating engine for Python.
- **Simple.css**: A classless CSS framework.
- **Docker**: A platform for developing, shipping, and running applications in containers.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. Create a `.env` file in the root directory with the following content:

    ```plaintext
    POSTGRES_DB=your_db_name
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_db_password
    DB_HOST=db
    DB_PORT=5432
    ```

### Running the App

1. Build and start the Docker containers:

    ```bash
    docker-compose up --build
    ```

2. Open your browser and go to `http://127.0.0.1:8000` to view the app.

### Stopping the App

1. To stop the containers:

    ```bash
    docker-compose down
    ```

### Testing the App

1. Make sure your Docker containers are running:

    ```bash
    docker-compose up -d
    ```

2. Make the `run_tests.sh` script executable:

    ```bash
    chmod +x scripts/run_tests.sh
    ```

3. Run the tests using the `run_tests.sh` script:

    ```bash
    ./scripts/run_tests.sh
    ```

## File Descriptions

- `app/main.py`: The main application file where FastAPI routes are defined.
- `Dockerfile`: The Dockerfile for building the FastAPI app image.
- `docker-compose.yml`: Docker Compose configuration file.
- `app/templates/index.html`: The main HTML file for rendering the todo list.
- `app/static/styles.css`: The main CSS file for styling the app.
- `scripts/run_tests.sh`: Script for running tests with Docker Compose.

## Usage

- **Create a Todo**: Enter a task in the input field and click the "Create" button.
- **Update a Todo**: Edit the text directly in the list and it will be updated automatically.
- **Toggle a Todo**: Click the checkbox to mark a task as completed or not completed.
- **Delete a Todo**: Click the "❌" button to remove a task from the list.

### Authentication

- **Sign Up**: Go to the sign-up page at `auth/signup-login` to create a new account. Fill in the required details and submit the form to create a new user.
- **Log In**: Go to the login page at `auth/signup-login` to sign in. Enter your credentials and submit the form. Upon successful login, you will be redirected to the todo list page.
- **Log Out**: Click the "Log out" option in the dropdown menu to end your session and return to the login page.

## API Documentation

The FastAPI application automatically generates API documentation using Swagger UI and ReDoc. You can access these by visiting the following URLs in your browser:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project url
- https://roadmap.sh/projects/todo-list-api
