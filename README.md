# FastAPI + HTMX Todo App

A simple Todo application built with FastAPI, HTMX, and Jinja2 templates. This app allows users to create, update, toggle, and delete todo items. It also incorporates modern styling for a simple, clean and visually appealing user interface.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Directory Structure](#directory-structure)
- [File Descriptions](#file-descriptions)
- [Usage](#usage)


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

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .`venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install fastapi uvicorn jinja2
    ```

### Running the App

1. Start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. Open your browser and go to `http://127.0.0.1:8000` to view the app.


## File Descriptions

- `main.py`: The main application file where FastAPI routes are defined.
- `templates/index.html`: The main HTML file for rendering the todo list.
- `static/styles.css`: The CSS file for styling the app.

## Usage

- **Create a Todo**: Enter a task in the input field and click the "Create" button.
- **Update a Todo**: Edit the text directly in the list and it will be updated automatically.
- **Toggle a Todo**: Click the checkbox to mark a task as completed or not completed.
- **Delete a Todo**: Click the "❌" button to remove a task from the list.


