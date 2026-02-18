# CampusAI — Smart Student Onboarding Platform

Production-grade student onboarding system for engineering colleges.

## Tech Stack

- **Frontend**: Streamlit (custom CSS styled)
- **Backend**: Python + SQLAlchemy ORM
- **Database**: SQLite (swappable to PostgreSQL)
- **Charts**: Plotly
- **Auth**: Salted SHA-256 password hashing
- **Routing**: Session-based multi-page navigation

## Project Structure

```
campus_ai/
├── main.py                    # Entry point
├── auth.py                    # Authentication module
├── models.py                  # SQLAlchemy ORM models
├── database.py                # Database configuration
├── knowledge_base.json        # FAQ knowledge base
├── .env                       # Environment variables
├── .env.example               # Environment template
├── requirements.txt           # Dependencies
├── static/
│   └── styles.css             # Custom CSS
├── services/
│   ├── onboarding_engine.py   # Chat/FAQ engine
│   ├── reminder_service.py    # Automated reminders
│   └── stage_service.py       # Stage calculation
├── pages/
│   ├── dashboard.py           # Student dashboard
│   ├── onboarding_chat.py     # AI chat assistant
│   ├── profile.py             # Student profile
│   ├── admin_panel.py         # Admin dashboard
│   └── portals.py             # Fee/Doc/LMS/Hostel portals
└── templates/
```

## Setup & Run

### 1. Install Dependencies

```bash
cd campus_ai
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run

```bash
streamlit run main.py
```

### 4. Access

Open http://localhost:8501

## Features

### Authentication

- Email + password registration
- Secure password hashing (salted SHA-256)
- Role-based access (Student / Admin)
- Admin registration requires a code

### Student Dashboard

- Welcome card with personalized greeting
- Animated progress bar (4-stage onboarding)
- KPI metric cards
- Pending tasks with priority badges
- Active reminders with deadlines
- Quick action buttons
- Onboarding journey visualization
- Completion donut chart (Plotly)

### AI Chat Assistant

- Rule-based intent detection (10 intents)
- Knowledge base responses (JSON)
- Personalized answers based on student status
- Chat history persistence
- Quick question buttons
- Escalation to admin

### Student Profile

- Editable academic info
- Onboarding action buttons (Pay Fee, Submit Docs, etc.)
- Status summary with color-coded badges
- Account settings view

### Internal Portals

- **Fee Portal**: Payment breakdown, method selection, instant confirmation
- **Document Portal**: Upload interface, verification tracking
- **LMS Portal**: Activation flow, course listing
- **Hostel Portal**: Room types, pricing, application form

### Admin Dashboard

- KPI metrics (students, fees, docs, LMS, escalations)
- Stage distribution bar chart
- Fee status pie chart
- Document verification chart
- Branch distribution analytics
- Searchable student directory with filters
- Escalation management with response system
- Completion rate reports

### Reminder Engine

- Auto-generates reminders based on student status
- Categories: fee, documents, LMS, orientation
- Deadline tracking with urgency indicators
- Auto-resolves when tasks are completed

## Database Schema

### users

| Field         | Type     | Description       |
| ------------- | -------- | ----------------- |
| id            | Integer  | Primary key       |
| name          | String   | Full name         |
| email         | String   | Unique email      |
| password_hash | String   | Hashed password   |
| role          | String   | student / admin   |
| created_at    | DateTime | Registration date |

### students

| Field                 | Type    | Description         |
| --------------------- | ------- | ------------------- |
| id                    | Integer | Primary key         |
| user_id               | Integer | FK to users         |
| branch                | String  | Academic branch     |
| year                  | Integer | Year of study       |
| hostel_preference     | String  | Room type           |
| fee_status            | String  | paid / unpaid       |
| documents_verified    | Boolean | Verification status |
| lms_activated         | Boolean | LMS status          |
| orientation_completed | Boolean | Orientation status  |
| mentor_assigned       | String  | Mentor name         |
| onboarding_stage      | Integer | 1-4                 |

### reminders

| Field      | Type     | Description                   |
| ---------- | -------- | ----------------------------- |
| id         | Integer  | Primary key                   |
| student_id | Integer  | FK to students                |
| message    | Text     | Reminder text                 |
| category   | String   | fee/documents/lms/orientation |
| deadline   | DateTime | Due date                      |
| resolved   | Boolean  | Completion status             |

### chat_history

| Field      | Type     | Description      |
| ---------- | -------- | ---------------- |
| id         | Integer  | Primary key      |
| student_id | Integer  | FK to students   |
| role       | String   | user / assistant |
| message    | Text     | Message content  |
| timestamp  | DateTime | Message time     |

### escalations

| Field          | Type    | Description        |
| -------------- | ------- | ------------------ |
| id             | Integer | Primary key        |
| student_id     | Integer | FK to students     |
| subject        | String  | Issue subject      |
| message        | Text    | Description        |
| status         | String  | pending / resolved |
| admin_response | Text    | Admin reply        |

## Switching to PostgreSQL

1. Install psycopg2: `pip install psycopg2-binary`
2. Update `.env`:
   ```
   DATABASE_URL=postgresql://user:pass@host:5432/campus_ai
   ```
3. Restart the app — tables auto-create

## Admin Access

Admin registration requires the code set in `.env` (default: `CAMPUS2026`).

## Security

- Passwords hashed with random salt + SHA-256
- Environment variables for sensitive config
- Role-based route protection
- Input validation on all forms
