# Configuration Guide

This guide explains how to configure your application to connect to Weaviate and PostgreSQL in different environments, such as Docker Compose, local development, and Docker without Compose.

## Weaviate Configuration

### URL Settings

- **`URL = "http://weaviate:8080"`**  
  Use this URL when Weaviate is running as a Docker container and accessible via the hostname `weaviate`. This is typically the case when using Docker Compose.

- **`URL = "http://localhost:8080"`**  
  Use this URL if you are running Weaviate locally on your machine (outside of Docker) or if Weaviate is accessible through `localhost` from the host machine.

Make sure the Weaviate instance is running on the correct port (default is `8080`).

## PostgreSQL Configuration

### Database Credentials

- **`USER`**: The username for the PostgreSQL database.
- **`PASSWORD`**: The password for the PostgreSQL database.
- **`NAME`**: The name of the PostgreSQL database.
- **`PORT`**: The port used by PostgreSQL, typically `5432`.

### Host Options

- **`HOST = "db"`**  
  Use this when PostgreSQL is running as a Docker service named `db` in a Docker Compose setup. The service name should match the one defined in your `docker-compose.yml` file.

- **`HOST = "localhost"`**  
  Use this when PostgreSQL is running locally on your machine, outside of Docker. This setting assumes the PostgreSQL service is accessible via `localhost`.

- **`HOST = "<custom-container-name>"`**  
  Use this when PostgreSQL is running as a Docker container with a custom name. Replace `<custom-container-name>` with the actual container name (e.g., `my-postgres-db`). This is suitable for Docker setups not using Compose but with custom configurations.

## Example Configuration

### Docker Compose Setup

Use this configuration when running both Weaviate and PostgreSQL as services in a Docker Compose setup.

```bash
[WEAVIATE]
URL = "http://weaviate:8080"  # Weaviate service name in docker-compose

[DB]
USER = "your_db_user"
PASSWORD = "your_db_password"
NAME = "your_db_name"
PORT = "5432"
HOST = "db"  # PostgreSQL service name in docker-compose


```
## Local Development (No Docker)
Use this configuration when running Weaviate and PostgreSQL directly on your local machine.

```bash
[WEAVIATE]
URL = "http://localhost:8080"  # Weaviate running locally

[DB]
USER = "your_db_user"
PASSWORD = "your_db_password"
NAME = "your_db_name"
PORT = "5432"
HOST = "localhost"  # PostgreSQL running locally

```

## Docker Without Compose
Use this configuration when running Weaviate and PostgreSQL as individual Docker containers without using Docker Compose.

```bash
[WEAVIATE]
URL = "http://weaviate:8080"  # Weaviate container

[DB]
USER = "your_db_user"
PASSWORD = "your_db_password"
NAME = "your_db_name"
PORT = "5432"
HOST = "your_postgres_container_name"  # Replace with the actual PostgreSQL container name
```
### Additional Notes
- When using Docker Compose, ensure the docker-compose.yml file defines services with matching names for the host configurations above.
- If using a .env file for environment variables, make sure to load them in your code using a library like python-dotenv to avoid hardcoding sensitive information.
- Always keep sensitive details like passwords and API keys secure and out of version control.

### Troubleshooting
- Connection Issues: Double-check the hostnames and ports. Make sure the services are up and accessible.
- Environment Variables: If using environment variables, ensure they are properly set and accessible by your application.
---

This `config.md` provides a general guide for configuring the application in different deployment scenarios. Adjust the values as needed for your specific environment.
