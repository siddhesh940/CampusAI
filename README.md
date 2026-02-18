<h1 align="center">🎓 CampusAI – Smart Student Onboarding Platform</h1>

<p align="center">
  <strong>A production-grade, multi-tenant SaaS platform for university student onboarding.</strong><br>
  <em>Built with FastAPI + Next.js 14 + Streamlit + Supabase + PostgreSQL</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.111+-009688?logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Next.js-14-000000?logo=next.js&logoColor=white" />
  <img src="https://img.shields.io/badge/TypeScript-5.5-3178C6?logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Supabase-Hosted-3ECF8E?logo=supabase&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white" />
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-project-structure">Structure</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-api-reference">API</a> •
  <a href="#-deployment">Deployment</a>
</p>

---

## 📌 Overview

CampusAI streamlines the entire student onboarding journey for universities — from admission to full campus integration. It provides:

- **Student Portal** — guided onboarding, document uploads, fee tracking, hostel application, LMS activation
- **Admin Panel** — student management, document verification, onboarding analytics
- **Super Admin** — multi-university management, subscription plans, platform oversight
- **AI Assistant** — contextual chatbot powered by knowledge base
- **Streamlit App** — standalone onboarding engine with chat, dashboards, and admin tools

---

## ✨ Features

| Module                         | Description                                                                                        |
| ------------------------------ | -------------------------------------------------------------------------------------------------- |
| **Authentication & RBAC**      | JWT-based auth with access + refresh tokens, role-based permissions (Student / Admin / SuperAdmin) |
| **Multi-Tenant Architecture**  | University-scoped data isolation, per-tenant branding via middleware                               |
| **Student Dashboard**          | Onboarding progress tracker, dynamic checklists, deadlines & reminders                             |
| **Document Management**        | Upload → Review → Approve/Reject cycle with Supabase Storage                                       |
| **Fee Payments**               | Simulated payment flow, status tracking, PDF receipt generation (ReportLab)                        |
| **LMS Activation**             | Track and manage learning platform activation per student                                          |
| **Hostel Applications**        | Room selection, application tracking, admin allocation                                             |
| **AI Chat Assistant**          | Knowledge-base powered chatbot for instant student help                                            |
| **Timetable & Courses**        | Course enrollment, timetable management                                                            |
| **Mentor Assignment**          | Assign mentors to students, track mentorship progress                                              |
| **Compliance & Notifications** | Compliance checks, in-app notifications                                                            |
| **Admin Panel**                | Student management, document verification, analytics dashboard                                     |
| **Super Admin Console**        | University CRUD, subscription management, platform oversight                                       |
| **Streamlit Onboarding App**   | Standalone app with guided onboarding chat, dashboards, portals                                    |
| **Rate Limiting**              | API request throttling per user/minute                                                             |

---

## 🛠 Tech Stack

### Backend (FastAPI)

| Technology               | Purpose                               |
| ------------------------ | ------------------------------------- |
| **FastAPI**              | Async REST API framework              |
| **SQLAlchemy 2.0**       | Async ORM with PostgreSQL             |
| **Alembic**              | Database migrations                   |
| **Pydantic v2**          | Request/response validation           |
| **python-jose + bcrypt** | JWT authentication & password hashing |
| **Supabase SDK**         | Cloud storage & database              |
| **ReportLab**            | PDF receipt generation                |
| **pytest + httpx**       | Testing                               |

### Frontend (Next.js)

| Technology                  | Purpose                                                      |
| --------------------------- | ------------------------------------------------------------ |
| **Next.js 14**              | App Router, SSR/SSG                                          |
| **TypeScript**              | Type safety                                                  |
| **Tailwind CSS**            | Utility-first styling                                        |
| **Radix UI**                | Accessible UI primitives (Dialog, Tabs, Select, Toast, etc.) |
| **Framer Motion**           | Animations & transitions                                     |
| **TanStack React Query v5** | Data fetching & caching                                      |
| **Zustand**                 | Client state management                                      |
| **React Hook Form + Zod**   | Form handling & validation                                   |
| **Recharts**                | Dashboard charts & analytics                                 |
| **Lucide React**            | Icon library                                                 |

### Streamlit App (campus_ai/)

| Technology     | Purpose                    |
| -------------- | -------------------------- |
| **Streamlit**  | Interactive web UI         |
| **SQLAlchemy** | ORM (SQLite for local dev) |
| **Plotly**     | Interactive charts         |

### Infrastructure

| Technology           | Purpose                                           |
| -------------------- | ------------------------------------------------- |
| **PostgreSQL 16**    | Primary database                                  |
| **Supabase**         | Hosted Postgres + Storage                         |
| **Docker Compose**   | Local dev orchestration (backend + frontend + db) |
| **Vercel**           | Frontend hosting                                  |
| **Render / Railway** | Backend hosting                                   |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT (Next.js 14)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐ │
│  │ Landing  │  │  Auth    │  │Dashboard │  │  Admin Panel   │ │
│  │  Page    │  │  Pages   │  │  Pages   │  │ (Admin/Super)  │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘ │
│                React Query + Zustand + Axios                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │  HTTPS (REST API)
┌───────────────────────────┴─────────────────────────────────────┐
│                    API SERVER (FastAPI)                          │
│  ┌────────┐  ┌────────┐  ┌───────────┐  ┌───────────────────┐ │
│  │  JWT   │  │  RBAC  │  │   Rate    │  │     Tenant        │ │
│  │ Auth   │  │ Guard  │  │  Limiter  │  │   Middleware      │ │
│  └────────┘  └────────┘  └───────────┘  └───────────────────┘ │
│                            │                                    │
│  ┌─────────────────────────┴──────────────────────────────────┐│
│  │                   ROUTERS (API Endpoints)                  ││
│  │  auth │ users │ documents │ payments │ hostel │ lms │ chat ││
│  │  courses │ timetable │ mentor │ onboarding │ admin │ super ││
│  └────────────────────────────────────────────────────────────┘│
│                            │                                    │
│  ┌─────────────────────────┴──────────────────────────────────┐│
│  │                   DATA ACCESS LAYER                        ││
│  │            SQLAlchemy ORM + Pydantic Schemas               ││
│  └────────────────────────────────────────────────────────────┘│
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
   ┌────┴─────┐     ┌──────┴───────┐    ┌──────┴──────┐
   │ Supabase │     │   Supabase   │    │  Streamlit  │
   │PostgreSQL│     │   Storage    │    │  App (Chat) │
   └──────────┘     └──────────────┘    └─────────────┘
```

---

## 📁 Project Structure

```
CampusAI/
│
├── .env                          # ⬅ Single unified env file (all services)
├── docker-compose.yml            # Docker orchestration (backend + frontend + db)
├── README.md
├── supabase_schema.sql           # Supabase DB schema v1
├── supabase_schema_v2.sql        # Supabase DB schema v2
│
├── backend/                      # ── FastAPI Backend ──
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── seed.py                   # Database seeding script
│   ├── alembic/                  # DB migrations
│   │   ├── env.py
│   │   └── versions/
│   │       ├── dd961d1f2045_initial_tables.py
│   │       └── 37313e3da4da_add_v2_tables_courses_timetable_mentor_.py
│   ├── app/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── config.py             # Pydantic settings (loads root .env)
│   │   ├── database.py           # Async engine & session factory
│   │   ├── auth/                 # JWT handler, permissions, RBAC
│   │   ├── core/                 # Dependencies, exceptions, security
│   │   ├── middleware/           # Rate limiter, tenant resolution
│   │   ├── models/               # SQLAlchemy ORM models
│   │   │   ├── user.py           #   Users, roles
│   │   │   ├── document.py       #   Document uploads & verification
│   │   │   ├── payment.py        #   Fee payments & receipts
│   │   │   ├── hostel.py         #   Hostel applications & rooms
│   │   │   ├── lms.py            #   LMS activation tracking
│   │   │   ├── chat.py           #   AI chat history
│   │   │   ├── course.py         #   Courses & enrollments
│   │   │   ├── timetable.py      #   Timetable entries
│   │   │   ├── mentor.py         #   Mentor assignments
│   │   │   ├── onboarding.py     #   Onboarding checklists
│   │   │   ├── notification.py   #   In-app notifications
│   │   │   ├── compliance.py     #   Compliance records
│   │   │   └── university.py     #   University & tenants
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   │   ├── auth.py, user.py, document.py, payment.py
│   │   │   ├── hostel.py, chat.py, course.py, timetable.py
│   │   │   ├── mentor.py, onboarding.py, compliance.py
│   │   │   └── university.py
│   │   ├── routers/              # API route handlers
│   │   │   ├── auth.py           #   /auth/* (register, login, refresh)
│   │   │   ├── users.py          #   /users/* (profile CRUD)
│   │   │   ├── documents.py      #   /documents/* (upload, review)
│   │   │   ├── payments.py       #   /payments/* (initiate, receipt)
│   │   │   ├── hostel.py         #   /hostel/* (apply, allocate)
│   │   │   ├── lms.py            #   /lms/* (activate, status)
│   │   │   ├── chat.py           #   /chat/* (message, history)
│   │   │   ├── courses.py        #   /courses/*
│   │   │   ├── timetable.py      #   /timetable/*
│   │   │   ├── mentor.py         #   /mentor/*
│   │   │   ├── onboarding.py     #   /onboarding/*
│   │   │   ├── dashboard.py      #   /dashboard/*
│   │   │   ├── compliance.py     #   /compliance/*
│   │   │   ├── admin.py          #   /admin/* (student mgmt, analytics)
│   │   │   └── superadmin.py     #   /superadmin/* (university mgmt)
│   │   ├── services/             # Business logic layer
│   │   └── utils/                # Helpers & constants
│   └── tests/
│       ├── conftest.py
│       └── test_health.py
│
├── frontend/                     # ── Next.js 14 Frontend ──
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── tsconfig.json
│   └── src/
│       ├── middleware.ts          # Auth guard middleware
│       ├── app/
│       │   ├── layout.tsx         # Root layout
│       │   ├── page.tsx           # Landing page
│       │   ├── globals.css
│       │   ├── (auth)/            # Login & register pages
│       │   ├── (dashboard)/       # Student dashboard
│       │   ├── (admin)/           # Admin & super admin panels
│       │   ├── about/
│       │   ├── contact/
│       │   ├── blog/
│       │   ├── careers/
│       │   ├── privacy/
│       │   ├── terms/
│       │   └── cookies/
│       ├── components/
│       │   ├── ui/                # Radix-based UI components
│       │   ├── dashboard/         # Dashboard-specific components
│       │   ├── landing/           # Landing page sections
│       │   └── providers.tsx      # React Query + Theme providers
│       ├── hooks/                 # Custom React hooks
│       ├── services/              # API client & service layer
│       ├── stores/                # Zustand state stores
│       ├── types/                 # TypeScript type definitions
│       └── lib/                   # Utility configurations
│
├── campus_ai/                    # ── Streamlit Onboarding App ──
│   ├── main.py                   # Streamlit app entry point
│   ├── database.py               # SQLAlchemy engine (SQLite)
│   ├── models.py                 # ORM models (User, Student, Reminder, etc.)
│   ├── auth.py                   # Auth helpers (register, login)
│   ├── knowledge_base.json       # AI assistant knowledge base
│   ├── requirements.txt
│   ├── services/
│   │   ├── onboarding_engine.py  # Stage-based onboarding logic
│   │   ├── stage_service.py      # Stage progression
│   │   └── reminder_service.py   # Automated reminders
│   ├── views/
│   │   ├── dashboard.py          # Student dashboard
│   │   ├── onboarding_chat.py    # AI chat interface
│   │   ├── profile.py            # Student profile
│   │   ├── admin_panel.py        # Admin management
│   │   └── portals.py            # Fee, Document, LMS, Hostel portals
│   ├── static/
│   │   └── styles.css            # Custom CSS
│   └── templates/
│
└── PPT Slides/                   # ── Presentation Slides ──
    ├── Slide 1 - Title.txt
    ├── Slide 2 - Problem Statement.txt
    ├── Slide 3 - Proposed Solution.txt
    ├── Slide 4 - Key Features.txt
    ├── Slide 5 - System Architecture Prompt.txt
    ├── Slide 6 - How It Works (Workflow).txt
    ├── Slide 7 - Impact & Benefits.txt
    └── Slide 8 - Conclusion & Future Scope.txt
```

---

## 🚀 Getting Started

### Prerequisites

| Tool                    | Version                 |
| ----------------------- | ----------------------- |
| Python                  | 3.11+                   |
| Node.js                 | 18+                     |
| PostgreSQL              | 16 (or use Docker)      |
| Docker & Docker Compose | Latest (optional)       |
| Supabase Account        | For storage & hosted DB |

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/CampusAI.git
cd CampusAI
```

### 2. Environment Setup

The project uses a **single root `.env` file** for all services:

```bash
# .env is already present at project root
# Edit values as needed (DB credentials, Supabase keys, JWT secret)
```

### 3. Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head            # Run database migrations
uvicorn app.main:app --reload --port 8000
```

Backend runs at: **http://localhost:8000**  
API docs at: **http://localhost:8000/docs** (Swagger UI)

### 4. Frontend Setup (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: **http://localhost:3000**

### 5. Streamlit App

```bash
cd campus_ai
pip install -r requirements.txt
streamlit run main.py
```

Streamlit runs at: **http://localhost:8501**

### 6. Docker (Full Stack — One Command)

```bash
docker-compose up --build
```

This starts:

- **Backend** → `localhost:8000`
- **Frontend** → `localhost:3000`
- **PostgreSQL** → `localhost:5432`

---

## 📡 API Reference

Base URL: `http://localhost:8000/api/v1`

### Authentication

| Method | Endpoint             | Auth   | Description          |
| ------ | -------------------- | ------ | -------------------- |
| POST   | `/auth/register`     | Public | Register new user    |
| POST   | `/auth/login`        | Public | Login & get tokens   |
| POST   | `/auth/refresh`      | Token  | Refresh access token |
| POST   | `/auth/verify-email` | Public | Verify email address |

### Users

| Method | Endpoint    | Auth     | Description              |
| ------ | ----------- | -------- | ------------------------ |
| GET    | `/users/me` | Student+ | Get current user profile |
| PUT    | `/users/me` | Student+ | Update profile           |

### Onboarding

| Method | Endpoint                     | Auth     | Description             |
| ------ | ---------------------------- | -------- | ----------------------- |
| GET    | `/onboarding/progress`       | Student+ | Get onboarding progress |
| PUT    | `/onboarding/checklist/{id}` | Student+ | Update checklist item   |

### Documents

| Method | Endpoint                 | Auth     | Description             |
| ------ | ------------------------ | -------- | ----------------------- |
| POST   | `/documents/upload`      | Student+ | Upload document         |
| GET    | `/documents`             | Student+ | List user documents     |
| PUT    | `/documents/{id}/review` | Admin+   | Approve/reject document |

### Payments

| Method | Endpoint                 | Auth     | Description          |
| ------ | ------------------------ | -------- | -------------------- |
| POST   | `/payments/initiate`     | Student+ | Initiate fee payment |
| GET    | `/payments`              | Student+ | List payments        |
| GET    | `/payments/{id}/receipt` | Student+ | Download PDF receipt |

### Hostel

| Method | Endpoint                | Auth     | Description               |
| ------ | ----------------------- | -------- | ------------------------- |
| POST   | `/hostel/apply`         | Student+ | Submit hostel application |
| GET    | `/hostel/status`        | Student+ | Check application status  |
| PUT    | `/hostel/{id}/allocate` | Admin+   | Allocate room             |

### LMS

| Method | Endpoint        | Auth     | Description      |
| ------ | --------------- | -------- | ---------------- |
| POST   | `/lms/activate` | Student+ | Activate LMS     |
| GET    | `/lms/status`   | Student+ | Check LMS status |

### AI Chat

| Method | Endpoint        | Auth     | Description        |
| ------ | --------------- | -------- | ------------------ |
| POST   | `/chat/message` | Student+ | Send message to AI |
| GET    | `/chat/history` | Student+ | Get chat history   |

### Courses & Timetable

| Method | Endpoint     | Auth     | Description            |
| ------ | ------------ | -------- | ---------------------- |
| GET    | `/courses`   | Student+ | List available courses |
| GET    | `/timetable` | Student+ | View timetable         |

### Mentor

| Method | Endpoint  | Auth     | Description          |
| ------ | --------- | -------- | -------------------- |
| GET    | `/mentor` | Student+ | View assigned mentor |

### Admin

| Method | Endpoint                   | Auth   | Description          |
| ------ | -------------------------- | ------ | -------------------- |
| GET    | `/admin/students`          | Admin+ | List all students    |
| GET    | `/admin/analytics`         | Admin+ | Onboarding analytics |
| GET    | `/admin/documents/pending` | Admin+ | Pending reviews      |
| GET    | `/dashboard/stats`         | Admin+ | Dashboard statistics |

### Super Admin

| Method | Endpoint                    | Auth  | Description          |
| ------ | --------------------------- | ----- | -------------------- |
| GET    | `/superadmin/universities`  | Super | List universities    |
| POST   | `/superadmin/universities`  | Super | Create university    |
| GET    | `/superadmin/subscriptions` | Super | Manage subscriptions |

---

## ⚙️ Environment Variables

All services read from a **single root `.env`** file:

| Variable                        | Service   | Description                        |
| ------------------------------- | --------- | ---------------------------------- |
| `APP_NAME`                      | Backend   | Application name                   |
| `APP_ENV`                       | Backend   | `development` / `production`       |
| `DEBUG`                         | Backend   | Debug mode toggle                  |
| `API_V1_PREFIX`                 | Backend   | API route prefix                   |
| `BACKEND_CORS_ORIGINS`          | Backend   | Allowed CORS origins (JSON array)  |
| `DATABASE_URL`                  | Backend   | Async PostgreSQL connection string |
| `DATABASE_URL_SYNC`             | Backend   | Sync PostgreSQL connection string  |
| `SUPABASE_URL`                  | Backend   | Supabase project URL               |
| `SUPABASE_ANON_KEY`             | Backend   | Supabase anonymous key             |
| `SUPABASE_SERVICE_ROLE_KEY`     | Backend   | Supabase service role key          |
| `SUPABASE_STORAGE_BUCKET`       | Backend   | Storage bucket name                |
| `JWT_SECRET_KEY`                | Backend   | JWT signing secret                 |
| `JWT_ALGORITHM`                 | Backend   | JWT algorithm (HS256)              |
| `ACCESS_TOKEN_EXPIRE_MINUTES`   | Backend   | Access token TTL                   |
| `REFRESH_TOKEN_EXPIRE_DAYS`     | Backend   | Refresh token TTL                  |
| `RATE_LIMIT_PER_MINUTE`         | Backend   | API rate limit                     |
| `NEXT_PUBLIC_API_URL`           | Frontend  | Backend API URL                    |
| `NEXT_PUBLIC_APP_NAME`          | Frontend  | App display name                   |
| `NEXT_PUBLIC_SUPABASE_URL`      | Frontend  | Supabase URL (client)              |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Frontend  | Supabase anon key (client)         |
| `SECRET_KEY`                    | Streamlit | Session secret key                 |
| `ADMIN_REGISTRATION_CODE`       | Streamlit | Admin signup code                  |

---

## 📊 Database Models

### Backend (PostgreSQL via SQLAlchemy)

| Model          | Table                   | Description                      |
| -------------- | ----------------------- | -------------------------------- |
| `User`         | `users`                 | User accounts & roles            |
| `University`   | `universities`          | Multi-tenant university data     |
| `Document`     | `documents`             | Uploaded documents & status      |
| `Payment`      | `payments`              | Fee payment records              |
| `Hostel`       | `hostels`               | Hostel applications & allocation |
| `LMS`          | `lms_activations`       | LMS activation tracking          |
| `ChatMessage`  | `chat_messages`         | AI chat history                  |
| `Course`       | `courses`               | Available courses                |
| `Timetable`    | `timetable_entries`     | Class schedules                  |
| `Mentor`       | `mentors`               | Mentor assignments               |
| `Onboarding`   | `onboarding_checklists` | Onboarding progress              |
| `Notification` | `notifications`         | In-app notifications             |
| `Compliance`   | `compliance_records`    | Compliance checks                |

### Streamlit App (SQLite)

| Model         | Table          | Description                        |
| ------------- | -------------- | ---------------------------------- |
| `User`        | `users`        | Auth (name, email, password, role) |
| `Student`     | `students`     | Profile & onboarding stage         |
| `Reminder`    | `reminders`    | Automated deadline reminders       |
| `ChatHistory` | `chat_history` | Chat conversations                 |
| `Escalation`  | `escalations`  | Student escalation requests        |

---

## 🐳 Docker Services

| Service            | Container           | Port | Image                |
| ------------------ | ------------------- | ---- | -------------------- |
| Backend (FastAPI)  | `campusai-backend`  | 8000 | Custom (Dockerfile)  |
| Frontend (Next.js) | `campusai-frontend` | 3000 | Custom (Dockerfile)  |
| PostgreSQL         | `campusai-db`       | 5432 | `postgres:16-alpine` |

---

## 🚢 Deployment

### Frontend → Vercel

1. Connect GitHub repo to Vercel
2. Set root directory to `frontend`
3. Add environment variables (`NEXT_PUBLIC_*`)
4. Deploy

### Backend → Render / Railway

1. Create Web Service
2. Root directory: `backend`
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### Database → Supabase

1. Create Supabase project
2. Copy connection string to `.env`
3. Run: `alembic upgrade head`
4. Enable RLS policies

---

## 🧪 Testing

```bash
cd backend
pytest tests/ -v
```

---

## 📝 Presentation Slides

Project presentation materials are in the `PPT Slides/` folder:

1. **Title** — Project introduction
2. **Problem Statement** — Current onboarding challenges
3. **Proposed Solution** — CampusAI approach
4. **Key Features** — Feature overview
5. **System Architecture** — Technical architecture
6. **How It Works** — User workflow
7. **Impact & Benefits** — Expected outcomes
8. **Conclusion & Future Scope** — Roadmap

---

## 🔮 Future Scope

- **Email & SMS Notifications** (SendGrid / Twilio)
- **Real-time Chat** via WebSockets
- **Mobile App** (React Native)
- **Payment Gateway Integration** (Razorpay / Stripe)
- **Biometric Verification** for document auth
- **Multi-language Support** (i18n)
- **Advanced Analytics** with ML-based predictions

---

## 📜 License

MIT License – see [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>CampusAI</strong> — Built with precision. Designed for scale. 🚀
</p>
