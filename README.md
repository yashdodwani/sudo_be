# OpenClaw Backend

Production-ready FastAPI backend service for the OpenClaw AI agent system.

This backend serves as the single source of truth for tasks and reminders, used by:
- Telegram/WhatsApp AI agents
- Web UI dashboard
- Future integrations

## Tech Stack

- **Python 3.11+**
- **FastAPI** - Modern, high-performance web framework
- **SQLAlchemy 2.0** - Async ORM
- **PostgreSQL** - Primary database
- **Alembic** - Database migrations
- **Pydantic v2** - Data validation
- **Uvicorn** - ASGI server
- **APScheduler** - Task scheduling

## Project Structure

```
openclaw_backend/
│
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── database.py        # Database engine and session
│   │
│   ├── models/                # SQLAlchemy ORM models
│   │   ├── task.py
│   │   └── reminder.py
│   │
│   ├── schemas/               # Pydantic schemas
│   │   ├── task.py
│   │   └── reminder.py
│   │
│   ├── crud/                  # Database operations
│   │   ├── task.py
│   │   └── reminder.py
│   │
│   ├── api/
│   │   ├── deps.py           # FastAPI dependencies
│   │   └── routes/           # API endpoints
│   │       ├── tasks.py
│   │       └── reminders.py
│   │
│   └── services/
│       └── scheduler.py       # Background scheduler service
│
├── alembic/                   # Database migrations
│   ├── env.py
│   ├── versions/
│   └── script.py.mako
│
├── alembic.ini
├── .env.example
├── requirements.txt
└── README.md
```

## Database Schema

### Tasks Table
- `id` - UUID primary key
- `title` - String (required)
- `description` - Text (optional)
- `status` - Enum: pending, completed, cancelled
- `due_time` - DateTime (nullable)
- `source` - Enum: telegram, whatsapp, ui, system
- `created_at` - Timestamp
- `updated_at` - Timestamp (auto-update)

### Reminders Table
- `id` - UUID primary key
- `task_id` - Foreign key → tasks.id (cascade delete)
- `remind_at` - DateTime
- `channel` - Enum: telegram, whatsapp, ui
- `sent` - Boolean (default: false)
- `created_at` - Timestamp

## API Endpoints

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | List all tasks (with filtering) |
| GET | `/tasks/{task_id}` | Get specific task |
| PATCH | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

### Reminders

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/reminders` | Create a new reminder |
| GET | `/reminders` | List all reminders (with filtering) |
| DELETE | `/reminders/{id}` | Delete a reminder |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health check |

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Setup PostgreSQL

#### Option A: Using Docker

```bash
docker run -d \
  --name openclaw-postgres \
  -e POSTGRES_USER=openclaw \
  -e POSTGRES_PASSWORD=openclaw_password \
  -e POSTGRES_DB=openclaw_db \
  -p 5432:5432 \
  postgres:15-alpine
```

#### Option B: Local PostgreSQL

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE USER openclaw WITH PASSWORD 'openclaw_password';
CREATE DATABASE openclaw_db OWNER openclaw;
GRANT ALL PRIVILEGES ON DATABASE openclaw_db TO openclaw;
\q
```

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
nano .env
```

Example `.env`:
```env
APP_NAME=OpenClaw Backend
APP_ENV=development

DATABASE_URL=postgresql+asyncpg://openclaw:openclaw_password@localhost:5432/openclaw_db

HOST=0.0.0.0
PORT=8000

LOG_LEVEL=INFO
```

### 4. Run Database Migrations

```bash
# Run Alembic migrations
alembic upgrade head
```

### 5. Start the Server

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the main.py directly
python app/main.py

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Usage Examples

### Create a Task

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review pull requests",
    "description": "Check and merge pending PRs",
    "status": "pending",
    "source": "ui",
    "due_time": "2026-03-01T10:00:00Z"
  }'
```

### Get All Tasks

```bash
curl "http://localhost:8000/tasks"

# With filters
curl "http://localhost:8000/tasks?status=pending&limit=10"
```

### Update a Task

```bash
curl -X PATCH "http://localhost:8000/tasks/{task_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### Create a Reminder

```bash
curl -X POST "http://localhost:8000/reminders" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "uuid-here",
    "remind_at": "2026-03-01T09:00:00Z",
    "channel": "telegram"
  }'
```

## Interactive API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Background Services

### Reminder Scheduler

The application includes a background scheduler that:
- Runs every minute
- Fetches unsent reminders that are due
- Logs them for processing

**Current Status**: The scheduler logs pending reminders. Integration with messaging services (Telegram/WhatsApp) is ready for implementation.

## Development

### Creating New Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests (when test suite is added)
pytest
```

## Production Considerations

### Security
- Use environment variables for sensitive data
- Configure CORS appropriately in `app/main.py`
- Implement authentication/authorization
- Use HTTPS in production

### Performance
- Increase worker count based on CPU cores
- Use connection pooling (already configured)
- Add caching layer (Redis) if needed
- Monitor database query performance

### Monitoring
- Add application monitoring (e.g., Sentry)
- Set up logging aggregation
- Monitor database connections
- Track API metrics

### Deployment
- Use process manager (systemd, supervisord)
- Deploy behind reverse proxy (Nginx)
- Use container orchestration (Kubernetes, Docker Swarm)
- Set up CI/CD pipeline

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | OpenClaw Backend |
| `APP_ENV` | Environment (development/production) | development |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `LOG_LEVEL` | Logging level | INFO |

## Architecture Decisions

### Async Everywhere
- All database operations use async SQLAlchemy
- FastAPI endpoints are async
- Enables high concurrency and performance

### Separation of Concerns
- **Models**: Database table definitions
- **Schemas**: API request/response validation
- **CRUD**: Database operations logic
- **Routes**: HTTP endpoint handlers
- **Services**: Background tasks and business logic

### Type Safety
- Full type hints throughout codebase
- Pydantic for runtime validation
- SQLAlchemy 2.0 typed mappings

## Future Enhancements

- [ ] Add authentication (JWT, OAuth2)
- [ ] Implement role-based access control
- [ ] Add pagination metadata
- [ ] Integrate Telegram bot API
- [ ] Integrate WhatsApp Business API
- [ ] Add task categories/tags
- [ ] Implement task assignments
- [ ] Add file attachments
- [ ] Create WebSocket support for real-time updates
- [ ] Add comprehensive test suite
- [ ] Implement rate limiting
- [ ] Add API versioning

## License

Proprietary - OpenClaw System

## Support

For issues and questions, please contact the development team.

