# TicketFlow: Event Ticketing Platform

## Development Environment Setup

### Prerequisites
* [Python 3.9+](https://www.python.org/downloads/)
* [Docker](https://docs.docker.com/engine/install/ubuntu/)
* [Docker Compose](https://docs.docker.com/desktop/setup/install/linux/)
* [VS Code](https://code.visualstudio.com/download) or [PyCharm](https://www.jetbrains.com/pycharm/download/?section=linux)

### Installation Steps

1. **Python**
   ```bash
   # Verify Python version
   python3 --version
   ```

2. **Docker**
   - Download from official Docker website
   - Install Docker Desktop
   ```bash
   # Verify Docker installation
   docker --version
   docker compose --version
   ```

3. **IDE**
   - Install VS Code or PyCharm
   - Install Python extension

4. **PostgreSQL**
   - Install PostgreSQL from official site
   - Create user and set the password
   ```bash
   # Use postgres user to create new user, depending on your setup.
   psql -U postgres -h localhost
   ```
   ```sql
   CREATE USER user_dev_local WITH PASSWORD 'your_password';
   ALTER ROLE user_dev_local CREATEDB; -- Optional: Use can create databases.
   CREATE DATABASE user_dev_local;
   GRANT ALL PRIVILEGES ON DATABASE user_dev_local TO user_dev_local;
   psql -U user_dev_local -d your_password -h localhost
   ```
5. **Redis**
   - Install redis from official [site]()https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/.
### Local Development

1. Clone Repository
   ```bash
   git clone https://github.com/tsotetsi/ticketflow.git
   cd ticketflow/backend
   ```

2. Create Virtual Environment
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Dependencies
   ```bash
   pip install -r requirements/local.txt
   ```
### Running User-Service

1. Build User-Service first
   ```bash
   docker compose -f  docker-compose.local.yml build --no-cache
   ```

2. Run User-Service(locally)
   ```bash
   docker compose -f docker-compose.local.yml up
   ```
3.  Accessing User-Service

   Visit your localhost om port 8000: [http://127.0.0.1:8000](http://127.0.0.1:8000)


### Running tests and test coverage

1. Run tests with pytest.
   ```bash
   pytest
   ```
2. Run tests, check your test coverage, and generate HTML coverage report.
   ```bash
   coverage run --source=. -m pytest
   coverage html
   open htmlcov/index.html
   ```

### Build User-Service docker image and publish to registry.

1. Tag(e.g. v1, latest) built image from the previous step.
   ```bash
    docker tag tsotetsi/ticketflow-user-service:v1.0.0.alpha tsotetsi/ticketflow-user-service:v1.0.0.alpha
   ```
2. Push docker image to a Registry(docker).
   You need to push your image to a container registry so that Kubernetes can access it.
   ```bash
   docker login
   docker tag your-image-name:your-tag your-dockerhub-username/your-image-name:your-tag
   docker push your-dockerhub-username/your-image-name:your-tag
   ------
   e.g.: docker push tsotetsi/ticketflow-user-service:v1.0.0.alpha
   ```

### Deploy to kubernetes(minikube).

1. Apply deployment configuration files.
   ```bash
   kubectl apply -f /k8s
   ```
2. Check if the pods were created successfully.
   ```bash
   kubectl get pods
   ```
3. Check the logs if there are any issues.
   ```bash
   kubectl logs <pod-name>
   ```
4. To restart deployment after updating files(no downtime)
   ```bash
   kubectl rollout restart
   ```
5. Connect to PostGreSQL inside the Pod
   ```bash
   kubectl exec -it postgres-c8c4f79bf-jkgbz -- /bin/bash
   root@postgres-c8c4f79bf-jkgbz:/#  # No you are inside postgresql.
   psql -U user_dev_local -d user_service_db
   psql (14.15 (Debian 14.15-1.pgdg120+1)) # This means the instance is working.
   ...
   ```
6. Other ways to check for services.
   ```bash
   apt update && apt install -y iputils-ping
   ping postgres
   telnet postgres 5432
   nc -vz postgres 5432
   ```
7. Accessing the API UI.
   - [swagger-ui](http://127.0.0.1:8000/api/schema/swagger-ui/)
   - [redo](http://127.0.0.1:8000/api/schema/redoc/)

### Prometheus and Grafana.
1. Access Prometheus at http://localhost:9090 and check 
   the "Targets" section to ensure your Django application is being scraped.

2. Access Grafana at http://localhost:3000 and set up Prometheus as a data source to visualize metrics.

## Architecture
- Event-Driven Architecture
- Microservices Architecture
- Python-based User Services
- Canary Deployments
- API Gateway(MicroService)