# TicketFlow: Event Ticketing Platform

## Development Environment Setup

### Prerequisites
* Python 3.9+
* Docker
* Docker Compose
* VS Code or PyCharm

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
   docker-compose --version
   ```

3. **IDE**
   - Install VS Code or PyCharm
   - Install Python extension

### Local Development

1. Clone Repository
   ```bash
   git clone https://github.com/tsotetsi/ticketflow.git
   cd ticketflow
   ```

2. Create Virtual Environment
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Running Services

```bash
docker-compose up --build
```

## Architecture
- Event-Driven Architecture
- Microservices Architecture
- Python-based Services