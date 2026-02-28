# OpenClaw Backend API Documentation

**Version:** 1.0.0  
**Base URL:** `http://your-server:8001`  
**Environment:** Production

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Response Format](#response-format)
4. [Error Handling](#error-handling)
5. [Endpoints](#endpoints)
   - [Health Check](#health-check)
   - [Tasks](#tasks)
   - [Reminders](#reminders)
6. [Data Models](#data-models)
7. [Examples](#examples)

---

## Overview

The OpenClaw Backend API provides RESTful endpoints for managing tasks and reminders. This API is designed to be consumed by:
- Web UI Dashboard
- Telegram Bot
- WhatsApp Bot
- Mobile Applications

**Features:**
- Full CRUD operations for tasks and reminders
- Filtering and pagination support
- Cascade deletion (deleting a task removes all its reminders)
- Automatic timestamps
- UUID-based identifiers

---

## Authentication

**Current Status:** No authentication required (v1.0.0)

**Future:** JWT-based authentication will be added in v2.0.0

---

## Response Format

### Success Response
```json
{
  "id": "uuid",
  "field1": "value1",
  "field2": "value2"
}
```

### List Response
```json
[
  {
    "id": "uuid",
    "field1": "value1"
  },
  {
    "id": "uuid",
    "field2": "value2"
  }
]
```

---

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Invalid request data |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

---

## Endpoints

### Health Check

#### GET `/health`

Check if the API is running.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "OpenClaw Backend",
  "environment": "development"
}
```

---

### Tasks

#### 1. Create Task

**POST** `/tasks`

Create a new task.

**Request Body:**
```json
{
  "title": "Review pull requests",
  "description": "Check and merge pending PRs from the team",
  "status": "pending",
  "due_time": "2026-03-01T10:00:00Z",
  "source": "ui"
}
```

**Request Fields:**

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| title | string | Yes | Task title (1-255 chars) | Any string |
| description | string | No | Detailed description | Any string |
| status | string | No | Task status | `pending`, `completed`, `cancelled` |
| due_time | datetime | No | Due date/time (ISO 8601) | ISO 8601 format |
| source | string | No | Where task was created | `telegram`, `whatsapp`, `ui`, `system` |

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Review pull requests",
  "description": "Check and merge pending PRs from the team",
  "status": "pending",
  "due_time": "2026-03-01T10:00:00Z",
  "source": "ui",
  "created_at": "2026-02-28T12:00:00Z",
  "updated_at": "2026-02-28T12:00:00Z"
}
```

---

#### 2. Get All Tasks

**GET** `/tasks`

Retrieve all tasks with optional filtering.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| skip | integer | No | 0 | Number of records to skip |
| limit | integer | No | 100 | Max records to return (1-1000) |
| status | string | No | - | Filter by status |

**Example Request:**
```
GET /tasks?status=pending&limit=10&skip=0
```

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Review pull requests",
    "description": "Check and merge pending PRs",
    "status": "pending",
    "due_time": "2026-03-01T10:00:00Z",
    "source": "ui",
    "created_at": "2026-02-28T12:00:00Z",
    "updated_at": "2026-02-28T12:00:00Z"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "Update documentation",
    "description": null,
    "status": "pending",
    "due_time": null,
    "source": "telegram",
    "created_at": "2026-02-28T13:00:00Z",
    "updated_at": "2026-02-28T13:00:00Z"
  }
]
```

---

#### 3. Get Single Task

**GET** `/tasks/{task_id}`

Retrieve a specific task by ID.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | UUID | Yes | Task identifier |

**Example Request:**
```
GET /tasks/550e8400-e29b-41d4-a716-446655440000
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Review pull requests",
  "description": "Check and merge pending PRs",
  "status": "pending",
  "due_time": "2026-03-01T10:00:00Z",
  "source": "ui",
  "created_at": "2026-02-28T12:00:00Z",
  "updated_at": "2026-02-28T12:00:00Z"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Task with id 550e8400-e29b-41d4-a716-446655440000 not found"
}
```

---

#### 4. Update Task

**PATCH** `/tasks/{task_id}`

Update an existing task. Only provided fields will be updated.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | UUID | Yes | Task identifier |

**Request Body (all fields optional):**
```json
{
  "title": "Review and merge pull requests",
  "description": "Updated description",
  "status": "completed",
  "due_time": "2026-03-02T10:00:00Z"
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Review and merge pull requests",
  "description": "Updated description",
  "status": "completed",
  "due_time": "2026-03-02T10:00:00Z",
  "source": "ui",
  "created_at": "2026-02-28T12:00:00Z",
  "updated_at": "2026-02-28T14:30:00Z"
}
```

---

#### 5. Delete Task

**DELETE** `/tasks/{task_id}`

Delete a task. This will also delete all associated reminders (cascade delete).

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | UUID | Yes | Task identifier |

**Example Request:**
```
DELETE /tasks/550e8400-e29b-41d4-a716-446655440000
```

**Response:** `204 No Content`

*(Empty response body)*

**Error Response:** `404 Not Found`
```json
{
  "detail": "Task with id 550e8400-e29b-41d4-a716-446655440000 not found"
}
```

---

### Reminders

#### 1. Create Reminder

**POST** `/reminders`

Create a new reminder for a task.

**Request Body:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "remind_at": "2026-03-01T09:00:00Z",
  "channel": "telegram"
}
```

**Request Fields:**

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| task_id | UUID | Yes | Associated task ID | Valid task UUID |
| remind_at | datetime | Yes | When to send reminder (ISO 8601) | ISO 8601 format |
| channel | string | Yes | Notification channel | `telegram`, `whatsapp`, `ui` |

**Response:** `201 Created`
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "remind_at": "2026-03-01T09:00:00Z",
  "channel": "telegram",
  "sent": false,
  "created_at": "2026-02-28T12:00:00Z"
}
```

**Error Response:** `404 Not Found` (if task doesn't exist)
```json
{
  "detail": "Task with id 550e8400-e29b-41d4-a716-446655440000 not found"
}
```

---

#### 2. Get All Reminders

**GET** `/reminders`

Retrieve all reminders with optional filtering.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| skip | integer | No | 0 | Number of records to skip |
| limit | integer | No | 100 | Max records to return (1-1000) |
| task_id | UUID | No | - | Filter by task ID |
| sent | boolean | No | - | Filter by sent status |

**Example Requests:**
```
GET /reminders
GET /reminders?sent=false
GET /reminders?task_id=550e8400-e29b-41d4-a716-446655440000
GET /reminders?sent=false&limit=20
```

**Response:** `200 OK`
```json
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "remind_at": "2026-03-01T09:00:00Z",
    "channel": "telegram",
    "sent": false,
    "created_at": "2026-02-28T12:00:00Z"
  },
  {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "remind_at": "2026-03-01T08:00:00Z",
    "channel": "whatsapp",
    "sent": true,
    "created_at": "2026-02-28T12:00:00Z"
  }
]
```

---

#### 3. Delete Reminder

**DELETE** `/reminders/{reminder_id}`

Delete a reminder.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| reminder_id | UUID | Yes | Reminder identifier |

**Example Request:**
```
DELETE /reminders/770e8400-e29b-41d4-a716-446655440002
```

**Response:** `204 No Content`

*(Empty response body)*

**Error Response:** `404 Not Found`
```json
{
  "detail": "Reminder with id 770e8400-e29b-41d4-a716-446655440002 not found"
}
```

---

## Data Models

### Task Status Enum
- `pending` - Task is pending
- `completed` - Task is completed
- `cancelled` - Task is cancelled

### Task Source Enum
- `telegram` - Created from Telegram bot
- `whatsapp` - Created from WhatsApp bot
- `ui` - Created from web UI
- `system` - Created by system

### Reminder Channel Enum
- `telegram` - Send via Telegram
- `whatsapp` - Send via WhatsApp
- `ui` - Show in UI

### DateTime Format
All datetime fields use ISO 8601 format with timezone:
```
2026-03-01T10:00:00Z
2026-03-01T10:00:00+00:00
```

---

## Examples

### Frontend Integration Examples

#### Using JavaScript Fetch API

```javascript
// Create a task
async function createTask() {
  const response = await fetch('http://your-server:8001/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title: 'New Task',
      description: 'Task description',
      status: 'pending',
      source: 'ui',
      due_time: '2026-03-01T10:00:00Z'
    })
  });
  
  const task = await response.json();
  console.log('Created task:', task);
  return task;
}

// Get all pending tasks
async function getPendingTasks() {
  const response = await fetch('http://your-server:8001/tasks?status=pending');
  const tasks = await response.json();
  console.log('Pending tasks:', tasks);
  return tasks;
}

// Update a task
async function updateTask(taskId) {
  const response = await fetch(`http://your-server:8001/tasks/${taskId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      status: 'completed'
    })
  });
  
  const task = await response.json();
  console.log('Updated task:', task);
  return task;
}

// Delete a task
async function deleteTask(taskId) {
  const response = await fetch(`http://your-server:8001/tasks/${taskId}`, {
    method: 'DELETE'
  });
  
  if (response.status === 204) {
    console.log('Task deleted successfully');
  }
}

// Create a reminder
async function createReminder(taskId) {
  const response = await fetch('http://your-server:8001/reminders', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      task_id: taskId,
      remind_at: '2026-03-01T09:00:00Z',
      channel: 'ui'
    })
  });
  
  const reminder = await response.json();
  console.log('Created reminder:', reminder);
  return reminder;
}
```

#### Using Axios

```javascript
import axios from 'axios';

const API_BASE = 'http://your-server:8001';

// Create a task
async function createTask(taskData) {
  try {
    const { data } = await axios.post(`${API_BASE}/tasks`, taskData);
    return data;
  } catch (error) {
    console.error('Error creating task:', error.response.data);
    throw error;
  }
}

// Get all tasks with filters
async function getTasks(filters = {}) {
  try {
    const { data } = await axios.get(`${API_BASE}/tasks`, {
      params: filters // { status: 'pending', limit: 10 }
    });
    return data;
  } catch (error) {
    console.error('Error fetching tasks:', error.response.data);
    throw error;
  }
}

// Update task
async function updateTask(taskId, updates) {
  try {
    const { data } = await axios.patch(`${API_BASE}/tasks/${taskId}`, updates);
    return data;
  } catch (error) {
    console.error('Error updating task:', error.response.data);
    throw error;
  }
}
```

#### React Hook Example

```javascript
import { useState, useEffect } from 'react';

function useTasks() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://your-server:8001/tasks');
      const data = await response.json();
      setTasks(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (taskData) => {
    try {
      const response = await fetch('http://your-server:8001/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData)
      });
      const newTask = await response.json();
      setTasks([newTask, ...tasks]);
      return newTask;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const updateTask = async (taskId, updates) => {
    try {
      const response = await fetch(`http://your-server:8001/tasks/${taskId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
      });
      const updatedTask = await response.json();
      setTasks(tasks.map(t => t.id === taskId ? updatedTask : t));
      return updatedTask;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const deleteTask = async (taskId) => {
    try {
      await fetch(`http://your-server:8001/tasks/${taskId}`, {
        method: 'DELETE'
      });
      setTasks(tasks.filter(t => t.id !== taskId));
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  return {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    deleteTask,
    refreshTasks: fetchTasks
  };
}
```

---

## CORS Configuration

The API has CORS enabled for all origins in development. For production, configure allowed origins appropriately.

**Current Configuration:**
```python
allow_origins=["*"]  # All origins allowed
allow_methods=["*"]   # All HTTP methods allowed
allow_headers=["*"]   # All headers allowed
```

---

## Interactive API Documentation

When the server is running, you can access interactive API documentation:

- **Swagger UI:** `http://your-server:8001/docs`
- **ReDoc:** `http://your-server:8001/redoc`

These provide a web interface to test all endpoints directly.

---

## Rate Limiting

**Current Status:** No rate limiting (v1.0.0)

**Future:** Rate limiting will be added in future versions.

---

## Pagination

For list endpoints (`GET /tasks`, `GET /reminders`):

- Default `limit`: 100
- Maximum `limit`: 1000
- Use `skip` and `limit` for pagination

**Example:**
```
GET /tasks?skip=0&limit=20   # Page 1
GET /tasks?skip=20&limit=20  # Page 2
GET /tasks?skip=40&limit=20  # Page 3
```

---

## Webhooks

**Current Status:** Not available (v1.0.0)

**Future:** Webhook support for task/reminder events planned for v2.0.0

---

## Support

For questions or issues, contact the backend team.

**API Version:** 1.0.0  
**Last Updated:** February 28, 2026

