# WindForLife

---

## Overview

The **WindForLife API** is a **Django REST Framework (DRF)** based API for collecting and analyzing wind data from anemometers.

---

## Architecture

### Project Structure

```
WIND-DJANGO-API/
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

---

#### Virtual Environment Setup

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

2. **Create a `.env` file**

   ```bash
   cp example.env .env
   ```

   Replace the values in the `.env` file with the right values.

   <br>

3. **Run the migrations**

   **Dev Environment**

      ```bash
      python manage.py migrate --settings=windforlife.settings.dev
      ```

   **Prod Environment**

      ```bash
      python manage.py migrate --settings=windforlife.settings.prod
      ```

4. **Run the server for dev environment**

   **Create superuser**

      ```bash
      python manage.py createsuperuser --settings=windforlife.settings.dev
      ```

   ```bash
   python manage.py runserver --settings=windforlife.settings.dev
   ```

5. **Run the server for prod environment**

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

1. **Run unit tests**

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
