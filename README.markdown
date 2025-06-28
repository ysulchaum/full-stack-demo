# Click Counter Full Stack Demo

This is a full-stack web application that implements a simple click counter. Users can click a button to increment a counter, which is stored in a MySQL database. The application is containerized using Docker and orchestrated with Docker Compose, with a reverse proxy handled by Caddy.

## Table of Contents
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [Accessing the Application](#accessing-the-application)
- [Troubleshooting](#troubleshooting)
- [Directory Structure](#directory-structure)

## Architecture
The application consists of the following components:
- **Frontend**: A React application built with Vite, served on port 3000.
- **Backend**: A Flask API running on Gunicorn, served on port 8000.
- **Database**: A MySQL 8.0 database for persistent storage of the counter value.
- **Reverse Proxy**: Caddy handles HTTP/HTTPS traffic and routes requests to the frontend or backend based on the domain.

The components are connected via a Docker network (`app-network`) and orchestrated using Docker Compose.

## Prerequisites
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed.
- A Cloudflare account and API token for DNS-based TLS configuration (optional for local development).
- Basic knowledge of Docker, React, Flask, and MySQL.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create Directory Structure**:
   Ensure the following directories exist:
   - `backend/`: Contains the Flask backend code and `Dockerfile`.
   - `frontend/`: Contains the React frontend code and `Dockerfile`.
   - `caddy/`: Contains the Caddy configuration and `Dockerfile`.

3. **Prepare Configuration Files**:
   - Update `frontend/src/App.tsx` with the correct backend URL:
     ```tsx
     const API_BASE_URL = 'http://api.yourdomain.com';
     ```
   - Update `frontend/vite.config.ts` with the correct backend URL:
     ```ts
     server: {
       allowedHosts: ['api.yourdomain.com'],
     }
     ```
   - Update `caddy/Caddyfile` with your domain and Cloudflare API token:
     ```text
     yourdomain.com {
         reverse_proxy frontend:3000
     }
     api.yourdomain.com {
         tls {
             dns cloudflare your_cloudflare_api_token
         }
         reverse_proxy backend:8000
     }
     ```

4. **Set Environment Variables**:
   Create a `.env` file in the root directory with the following:
   ```bash
   CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
   ```

## Environment Configuration
The application uses the following environment variables:
- **Backend** (set in `docker-compose.yml`):
  - `MYSQL_HOST`: Database host (default: `mysql`).
  - `MYSQL_USER`: Database user (default: `user`).
  - `MYSQL_PASSWORD`: Database password (default: `password`).
  - `MYSQL_DB`: Database name (default: `counter_db`).
- **MySQL** (set in `docker-compose.yml`):
  - `MYSQL_ROOT_PASSWORD`: Root password for MySQL (default: `root_password`).
  - `MYSQL_DATABASE`: Database name (default: `counter_db`).
  - `MYSQL_USER`: Database user (default: `user`).
  - `MYSQL_PASSWORD`: Database password (default: `password`).
- **Caddy**:
  - `CLOUDFLARE_API_TOKEN`: Cloudflare API token for TLS (set in `.env`).

## Running the Application
1. **Build and Start Containers**:
   ```bash
   docker-compose up --build
   ```
   This command builds the Docker images and starts the services (`mysql`, `backend`, `frontend`, `caddy`).

2. **Verify Services**:
   - MySQL: Runs on port `3307` (mapped to `3306` in the container).
   - Backend: Exposed on port `8000` (accessible via `api.yourdomain.com`).
   - Frontend: Exposed on port `3000` (accessible via `yourdomain.com`).
   - Caddy: Listens on ports `80` and `443` for HTTP/HTTPS traffic.

3. **Initialize Database**:
   The `counter_db.sql` script is automatically executed during MySQL container startup, creating the `counter` table and inserting an initial count of `5`.

## Accessing the Application
- **Frontend**: Open `http://yourdomain.com` (or `http://localhost` for local development) in a browser to view the React app.
- **Backend API**:
  - GET `/api/count`: Retrieve the current counter value.
  - POST `/api/click`: Increment the counter and return the updated value.
- **MySQL**: Connect to the database using a MySQL client:
  ```bash
  mysql -h localhost -P 3307 -u user -p
  ```
  Enter the password (`password`) when prompted.

## Troubleshooting
- **Database Connection Issues**:
  - Ensure the MySQL container is healthy (`docker ps` should show `healthy` for the `mysql` service).
  - Verify environment variables in `docker-compose.yml` match those in `app.py`.
- **Caddy TLS Errors**:
  - Ensure the `CLOUDFLARE_API_TOKEN` is valid and has DNS edit permissions.
  - For local development, replace the `tls` directive in `Caddyfile` with `tls internal` to use a self-signed certificate.
- **Frontend Fetch Errors**:
  - Check that `API_BASE_URL` in `App.tsx` matches the backend URL (`api.yourdomain.com`).
  - Ensure CORS is properly configured in `app.py` (already enabled via `Flask-CORS`).
- **Logs**:
  - View container logs for debugging:
    ```bash
    docker logs backend
    docker logs frontend
    docker logs caddy
    docker logs mysql
    ```

## Directory Structure
```
.
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── App.tsx
│   ├── vite.config.ts
│   └── Dockerfile
├── caddy/
│   ├── Caddyfile
│   └── Dockerfile
├── counter_db.sql
├── docker-compose.yml
└── README.md
```