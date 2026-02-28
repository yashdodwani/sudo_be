# OpenClaw API - Quick Reference

**Base URL:** `http://your-server:8001`

---

## Quick Links

- 📚 [Full Documentation](./API_DOCUMENTATION.md)
- 🔍 Swagger UI: `http://your-server:8001/docs`
- 📖 ReDoc: `http://your-server:8001/redoc`

---

## Endpoints Summary

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/tasks` | Create new task |
| `GET` | `/tasks` | List all tasks |
| `GET` | `/tasks/{id}` | Get task by ID |
| `PATCH` | `/tasks/{id}` | Update task |
| `DELETE` | `/tasks/{id}` | Delete task |

### Reminders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/reminders` | Create reminder |
| `GET` | `/reminders` | List reminders |
| `DELETE` | `/reminders/{id}` | Delete reminder |

---

## Quick Examples

### Create Task
```bash
curl -X POST http://localhost:8001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Task",
    "description": "Task details",
    "status": "pending",
    "source": "ui"
  }'
```

### Get All Tasks
```bash
curl http://localhost:8001/tasks
```

### Get Pending Tasks
```bash
curl http://localhost:8001/tasks?status=pending
```

### Update Task Status
```bash
curl -X PATCH http://localhost:8001/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Create Reminder
```bash
curl -X POST http://localhost:8001/reminders \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "{task_id}",
    "remind_at": "2026-03-01T09:00:00Z",
    "channel": "telegram"
  }'
```

---

## Enums

### Task Status
- `pending`
- `completed`
- `cancelled`

### Task Source
- `telegram`
- `whatsapp`
- `ui`
- `system`

### Reminder Channel
- `telegram`
- `whatsapp`
- `ui`

---

## TypeScript Types

```typescript
// Task
interface Task {
  id: string;  // UUID
  title: string;
  description: string | null;
  status: 'pending' | 'completed' | 'cancelled';
  due_time: string | null;  // ISO 8601
  source: 'telegram' | 'whatsapp' | 'ui' | 'system';
  created_at: string;  // ISO 8601
  updated_at: string;  // ISO 8601
}

// Task Create Request
interface TaskCreate {
  title: string;
  description?: string | null;
  status?: 'pending' | 'completed' | 'cancelled';
  due_time?: string | null;
  source?: 'telegram' | 'whatsapp' | 'ui' | 'system';
}

// Task Update Request
interface TaskUpdate {
  title?: string;
  description?: string | null;
  status?: 'pending' | 'completed' | 'cancelled';
  due_time?: string | null;
}

// Reminder
interface Reminder {
  id: string;  // UUID
  task_id: string;  // UUID
  remind_at: string;  // ISO 8601
  channel: 'telegram' | 'whatsapp' | 'ui';
  sent: boolean;
  created_at: string;  // ISO 8601
}

// Reminder Create Request
interface ReminderCreate {
  task_id: string;  // UUID
  remind_at: string;  // ISO 8601
  channel: 'telegram' | 'whatsapp' | 'ui';
}
```

---

## Frontend API Client Example

```typescript
// api.ts
const API_BASE = 'http://localhost:8001';

export const api = {
  // Tasks
  tasks: {
    list: (params?: { status?: string; skip?: number; limit?: number }) =>
      fetch(`${API_BASE}/tasks?${new URLSearchParams(params as any)}`).then(r => r.json()),
    
    get: (id: string) =>
      fetch(`${API_BASE}/tasks/${id}`).then(r => r.json()),
    
    create: (data: TaskCreate) =>
      fetch(`${API_BASE}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(r => r.json()),
    
    update: (id: string, data: TaskUpdate) =>
      fetch(`${API_BASE}/tasks/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(r => r.json()),
    
    delete: (id: string) =>
      fetch(`${API_BASE}/tasks/${id}`, { method: 'DELETE' })
  },
  
  // Reminders
  reminders: {
    list: (params?: { task_id?: string; sent?: boolean; skip?: number; limit?: number }) =>
      fetch(`${API_BASE}/reminders?${new URLSearchParams(params as any)}`).then(r => r.json()),
    
    create: (data: ReminderCreate) =>
      fetch(`${API_BASE}/reminders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(r => r.json()),
    
    delete: (id: string) =>
      fetch(`${API_BASE}/reminders/${id}`, { method: 'DELETE' })
  }
};

// Usage
const tasks = await api.tasks.list({ status: 'pending' });
const newTask = await api.tasks.create({ title: 'New Task', source: 'ui' });
```

---

## Common Patterns

### Create Task with Reminder
```javascript
// 1. Create task
const task = await api.tasks.create({
  title: 'Important Meeting',
  description: 'Quarterly review',
  due_time: '2026-03-01T15:00:00Z',
  source: 'ui'
});

// 2. Create reminder 1 hour before
const reminder = await api.reminders.create({
  task_id: task.id,
  remind_at: '2026-03-01T14:00:00Z',
  channel: 'telegram'
});
```

### Mark Task as Complete
```javascript
await api.tasks.update(taskId, { status: 'completed' });
```

### Get Task's Reminders
```javascript
const reminders = await api.reminders.list({ task_id: taskId });
```

---

## Error Handling

```javascript
try {
  const task = await api.tasks.create(data);
} catch (error) {
  if (error.response?.status === 404) {
    console.error('Not found');
  } else if (error.response?.status === 422) {
    console.error('Validation error:', error.response.data);
  } else {
    console.error('Unknown error:', error);
  }
}
```

---

## Notes

- All IDs are UUIDs
- Datetimes use ISO 8601 format with timezone
- Deleting a task cascades to its reminders
- Pagination: default limit is 100, max is 1000
- No authentication required (v1.0.0)

---

For detailed documentation, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

