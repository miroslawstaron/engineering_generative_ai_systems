## Running the Project with Docker

This project is containerized using Docker and Docker Compose for easy setup and deployment.

### Project-Specific Docker Details
- **Python Version:** 3.9 (as specified in the Dockerfile)
- **Dependencies:** Installed from `requirements.txt` during the build process
- **No required environment variables** are specified in the Dockerfile or compose file by default. (If you need to use environment variables, uncomment the `env_file` line in `docker-compose.yml` and provide a `.env` file.)
- **User:** The application runs as a non-root user (`appuser`) inside the container for improved security.

### Build and Run Instructions
1. **Build and start the service:**
   ```sh
   docker compose up --build
   ```
   This will build the Docker image and start the `python-app` service.

2. **Accessing the Application:**
   - The application will be available on your host at [http://localhost:5000](http://localhost:5000) (port 5000 is exposed).

### Ports
- **5000:** Exposed by the container and mapped to the host (as per `docker-compose.yml` and Dockerfile).

### Special Configuration
- No external services, volumes, or persistent data are required for this project based on the provided files.
- If you need to set environment variables, create a `.env` file in the project root and uncomment the `env_file` line in `docker-compose.yml`.

---

_These instructions are specific to the current project structure and Docker setup. Update as needed if project requirements change._