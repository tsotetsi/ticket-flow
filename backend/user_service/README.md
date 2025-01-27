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
   docker compose -f docker-compose.local.yml build
   ```

2. Run User-Service
   ```bash
   docker compose -f docker-compose.local.yml up
   ```
3.  Accessing User-Service

   Visit your localhost om port 8000: [http://127.0.0.1:8000](http://127.0.0.1:8000)


## Architecture
- Event-Driven Architecture
- Microservices Architecture
- Python-based User Service