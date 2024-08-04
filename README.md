# FastAPI + HTMX Todo App

A simple Todo application built with FastAPI, HTMX, and Jinja2 templates. This app allows users to create, update, toggle, and delete todo items. It also incorporates modern styling for a simple, clean, and visually appealing user interface.

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

## Unique Approach

This project demonstrates a unique approach to building web applications by combining FastAPI with HTMX. By leveraging HTMX, the app provides a highly dynamic user experience with real-time updates directly in the browser without requiring full page reloads. This approach showcases how modern libraries can be integrated to create responsive and efficient web applications, even for seemingly simple tasks like managing a Todo list.

## Features

- Create new todo items.
- Update the title of existing todo items.
- Toggle the completion status of todo items.
- Delete todo items.
- Real-time updates with HTMX.

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

2. Run the tests using Docker Compose:

    ```bash
    docker-compose exec app pytest
    ```

## File Descriptions

- `app/main.py`: The main application file where FastAPI routes are defined.
- `Dockerfile`: The Dockerfile for building the FastAPI app image.
- `docker-compose.yml`: Docker Compose configuration file.
- `app/templates/index.html`: The main HTML file for rendering the todo list.
- `app/static/styles.css`: The CSS file for styling the app.

## Usage

- **Create a Todo**: Enter a task in the input field and click the "Create" button.
- **Update a Todo**: Edit the text directly in the list and it will be updated automatically.
- **Toggle a Todo**: Click the checkbox to mark a task as completed or not completed.
- **Delete a Todo**: Click the "❌" button to remove a task from the list.
