# FastAPI E-commerce API

This project provides a RESTful API for an e-commerce platform built with FastAPI, PostgreSQL (managed locally with Docker Compose), and tested with Pytest. GitHub Actions handle CI/CD.

## Setup

1.  **Clone the repository.**

2.  **Create a Virtual Environment:**  Isolate project dependencies:

    ```bash
    python3 -m venv venv
    venv\Scripts\activate  # Windows
    # source venv/bin/activate  # Linux/macOS
    ```

3.  **Install Dependencies:** Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Docker Compose:** Initialize the PostgreSQL database using Docker Compose:

    ```bash
    docker-compose up --build
    ```

5.  **Environment Variables:** Create a `.env` file based on `.env.example`.  **Replace the placeholders with your actual values, especially `YOUR_SECRET_KEY_HERE`!**

6.  **Database Migrations:** Apply database migrations using either:

    ```bash
    alembic upgrade head
    ```

    or

    ```bash
    python migrate.py
    ```

7.  **Run the API:** Start the FastAPI application:

    ```bash
    python run.py
    ```

## Testing

1.  **Ensure your environment variables are set correctly.**
2.  **Run Pytest:**

    ```bash
    pytest
    ```

## Key Technologies

*   FastAPI: High-performance Python web framework.
*   PostgreSQL: Relational database (managed locally with Docker).
*   Docker Compose: Container orchestration for local development.
*   Pytest: Testing framework.
*   GitHub Actions: Continuous integration and continuous deployment.