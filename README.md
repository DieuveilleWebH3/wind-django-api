# WindForLife

---

## Overview

The **WindForLife API** is a **Django REST Framework (DRF)** based API for collecting and analyzing wind data from anemometers.
The API allows authenticated users to:

- Manage **anemometers** (CRUD operations).
- Submit **wind speed readings** for anemometers.
- Retrieve **statistics** (min, max, mean wind speed) within a specified geographic area.
- Filter anemometer readings based on **tags**.
- View the **latest wind speed readings** for each anemometer.
- Secure authentication using **JWT tokens**.
- API documentation via **Swagger UI (drf-spectacular)**.

## Features

- **RESTful API**: Built using Django REST Framework (DRF).
- **Authentication**: Secure access via **JWT authentication**.
- **Filtering & Pagination**: Supports **Django Filters** for anemometer readings.
- **Logging**: Integrated **logging system** to track API requests and debugging.
- **Swagger Documentation**: API documentation accessible via Swagger UI.
- **Docker Support**: Easily deployable with Docker.

---

## API Endpoints

### **Authentication**

- `POST /api/token/` - Obtain JWT access token.
- `POST /api/token/refresh/` - Refresh JWT token.

### **Anemometers**

- `GET /api/anemometers/` - List all anemometers (paginated).
- `POST /api/anemometers/` - Create a new anemometer.
- `GET /api/anemometers/{id}/` - Retrieve a single anemometer.
- `PUT /api/anemometers/{id}/` - Update an anemometer.
- `DELETE /api/anemometers/{id}/` - Delete an anemometer.

### **Wind Speed Readings**

- `POST /api/readings/` - Submit a wind speed reading.
- `GET /api/readings/` - List all readings (filterable by tags).

### **Statistics**

- `GET /api/stats/?latitude=34.0522&longitude=-118.2437&radius=10` - Retrieve wind speed statistics within a radius.

---

## Architecture

### Project Structure

```
WIND-DJANGO-API/
├── api/
│   ├── fixtures/
│   │   ├── seed.json
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── factories.py
│   ├── filter.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── windforlife/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── prod.py
│   ├── wsgi/
│   │   ├── dev.py
│   │   ├── prod.py
│   ├── asgi.py
│   ├── urls.py
├── .env
├── .gitignore
├── Dockerfile.dev
├── Dockerfile.prod
├── example.env
├── manage.py
├── pytest.ini
├── README.md
├── requirements.dev.txt
├── requirements.prod.txt
├── requirements.txt
```

---

## Prerequisites

### Technologies Used

- **Python 3.12**
- **Django 4.2**
- **Django REST Framework**
- **PostgreSQL / SQLite**
- **Docker**

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/DieuveilleWebH3/wind-django-api.git
   cd wind-django-api
   ```

   Or via SSH

   ```bash
   git clone git@github.com:DieuveilleWebH3/wind-django-api.git
   cd wind-django-api
   ```

2. **Create a `.env` file**

   ```bash
   cp example.env .env
   ```

   Replace the values in the `.env` file with the right and appropriate values.

---

#### Virtual Environment Setup

##### Using Poetry: Activate a virtual environment

   1. **Install Poetry if not already installed**

      ```bash
      curl -sSL https://install.python-poetry.org | python3 -
      ```

   2. **Ensure Poetry is in your PATH**

      ```bash
      export PATH="$HOME/.local/bin:$PATH"
      ```

   3. **Install dependencies**

      ```bash
      poetry install
      ```

   4. **Activate the virtual environment**

      ```bash
      poetry shell
      ```

##### Using Pip: Activate a virtual environment

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

1. **Install dependencies**

   **Dev Environment**

      ```bash
      pip install -r requirements.dev.txt
      ```

   **Prod Environment**

      ```bash
      pip install -r requirements.prod.txt
      ```

##### Run Project

1. **Run the migrations**

   **Dev Environment**

      ```bash
      python manage.py migrate --settings=windforlife.settings.dev
      ```

   **Prod Environment**

      ```bash
      python manage.py migrate --settings=windforlife.settings.prod
      ```

2. **Run the server for dev environment**

   **Create superuser**

      ```bash
      python manage.py createsuperuser --settings=windforlife.settings.dev
      ```

   ```bash
   python manage.py runserver --settings=windforlife.settings.dev
   ```

3. **Run the server for prod environment**

   **Create superuser**

      ```bash
      python manage.py createsuperuser --settings=windforlife.settings.prod
      ```

   ```bash
   python manage.py runserver --settings=windforlife.settings.prod
   ```

#### Docker Setup

1. **Build & Run Docker Container For Dev**

   ```bash
   docker build -f Dockerfile.dev -t windforlife-dev .

   docker run --rm -p 8000:8000 -v $(pwd):/app windforlife-dev
   ```

2. **Build & Run Docker Container for Prod**

   ```bash
   docker build -f Dockerfile.prod -t windforlife-prod .

   docker run --rm -p 8000:8000 windforlife-prod
   ```

3. **Running Commands Inside Container**

   ```bash
   docker exec -it {CONTAINER_ID} bash
   ```

---

### Testing Setup

1. **Add dummy data to test locally**

   ```bash
   python manage.py loaddata api/fixtures/seed.json
   ```

2. **Run unit tests**

   ```bash
   pytest
   ```

    **Run pytest with coverage**

    ```bash
    pytest --cov=api --cov-report=term-missing
    ```

    **OR**

    ```bash
    pytest --cov=api --cov-report=html
    ```

---

### Common Issues

#### Docker cannot access local host PostgreSQL Database

1. **Verify PostgreSQL Host**

   The localhost in your Docker container refers to the container itself, not your host machine.
   If PostgreSQL is running on your host machine, you need to use the host's IP address or host.docker.internal (on Docker Desktop for Windows/Mac).

   <br>

   Update your .env file to use host.docker.internal for DB_HOST:

   ```bash
   DB_HOST=host.docker.internal
   ```

2. **Expose PostgreSQL to the Docker Container**

   Ensure PostgreSQL is configured to accept connections from the Docker container.

   <br>

   Edit pg_hba.conf: Locate the pg_hba.conf file (usually in the PostgreSQL data directory) and add the following line:

   ```bash
   host    all             all             0.0.0.0/0            md5
   ```

   Edit postgresql.conf: Locate the postgresql.conf file and ensure the listen_addresses setting includes *:

   ```bash
   listen_addresses = '*'
   ```

   Restart PostgreSQL: Restart the PostgreSQL service to apply the changes:

   ```bash
   sudo systemctl restart postgresql
   ```

---
