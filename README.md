# 🏫 ShalaConnect — शाळाकनेक्ट

> A production-ready school management platform for Cluster Heads (केंद्रप्रमुख) managing multiple rural schools in Maharashtra.

---

## 📸 Features

| Module | Admin (Cluster Head) | Headmaster |
|--------|----------------------|------------|
| **Dashboard** | Attendance overview, charts, alerts | Personal dashboard, pending tasks |
| **Schools** | Full CRUD, photo upload, topper info | View own school info |
| **Attendance** | View all schools, daily submission chart | Submit & view own school attendance |
| **GR Documents** | Upload PDFs, track "seen by" | View & acknowledge documents |
| **Meetings** | Schedule online/offline, notify all | View, acknowledge meetings |
| **Events** | Create events, upload photos & reports | View events & photos |
| **Forms** | Build dynamic forms, export to Excel | Fill assigned forms |
| **Users** | Manage headmaster accounts | — |
| **Notifications** | — | Real-time bell, unread count |
| **Public Portal** | — | Public school listing + attendance chart |

---

## 🏗️ Tech Stack

- **Backend:** Spring Boot 3.2, Spring Security (JWT), Spring Data JPA, MySQL 8, Apache POI
- **Frontend:** React 18, Vite, Tailwind CSS, React Router v6, React Hook Form, Recharts, Axios
- **DevOps:** Docker, Docker Compose, Nginx

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Java 21+
- Node.js 20+
- MySQL 8.0+
- Maven 3.9+

---

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ShalaConnect.git
cd ShalaConnect
```

---

### 2. Database Setup

```sql
CREATE DATABASE school_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

### 3. Backend Setup

```bash
cd backend

# Copy environment config
cp .env.example .env

# Edit .env and set your MySQL credentials
# DB_PASSWORD=your_mysql_password

# Run the application
./mvnw spring-boot:run
```

The backend starts on **http://localhost:7070**

On first run, a default admin account is created:
- **Email:** `admin@shalaconnect.in`
- **Password:** `Admin@123`

> ⚠️ Change this password immediately after first login!

---

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

The frontend starts on **http://localhost:5173**

---

## 🐳 Docker Setup (Recommended)

Run the entire stack with one command:

```bash
# From the root directory
docker-compose up -d
```

- Frontend: **http://localhost:80**
- Backend API: **http://localhost:7070**
- MySQL: **localhost:3306**

---

## 📁 Project Structure

```
ShalaConnect/
├── backend/                          # Spring Boot API
│   └── src/main/java/com/shalaconnect/
│       ├── controller/               # REST controllers
│       ├── service/                  # Business logic
│       │   └── impl/                 # Service implementations
│       ├── repository/               # Spring Data JPA repos
│       ├── model/                    # JPA entities
│       ├── dto/
│       │   ├── request/              # Request DTOs
│       │   └── response/             # Response DTOs
│       ├── security/                 # JWT filter & util
│       ├── config/                   # Security, Web, App config
│       └── exception/                # Global exception handler
│
├── frontend/                         # React SPA
│   └── src/
│       ├── components/
│       │   ├── layout/               # DashboardLayout, ProtectedRoute
│       │   └── ui/                   # Modal, StatCard, Skeleton, etc.
│       ├── pages/
│       │   ├── auth/                 # Login page
│       │   ├── admin/                # Admin portal pages
│       │   ├── headmaster/           # Headmaster portal pages
│       │   └── public/               # Public school portal
│       ├── services/                 # Axios API layer
│       ├── hooks/                    # useApi, useMutation
│       ├── context/                  # AuthContext
│       └── App.jsx                   # Router setup
│
├── database/
│   └── init.sql                      # DB initialization script
├── docker-compose.yml
└── README.md
```

---

## 🔑 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/login` | Public | Login |
| GET | `/api/auth/me` | Any | Get current user |
| POST | `/api/auth/register-headmaster` | Admin | Create headmaster |
| GET | `/api/schools` | Public | List all schools |
| POST | `/api/schools` | Admin | Create school |
| GET | `/api/attendance/summary` | Admin | Today's summary |
| POST | `/api/attendance` | Headmaster | Submit attendance |
| POST | `/api/gr` | Admin | Upload GR document |
| POST | `/api/gr/{id}/seen` | Any | Mark GR as seen |
| POST | `/api/meetings` | Admin | Schedule meeting |
| POST | `/api/meetings/{id}/acknowledge` | Headmaster | Acknowledge |
| POST | `/api/forms` | Admin | Create form |
| POST | `/api/forms/{id}/respond` | Headmaster | Submit response |
| GET | `/api/forms/{id}/export` | Admin | Export to Excel |

---

## 🎨 Design System

- **Primary:** Blue (`#2563eb` — `#1e3a8a`)
- **Success:** Green
- **Warning:** Amber/Orange
- **Danger:** Red
- **Typography:** Inter (Google Fonts)
- **Component library:** Tailwind CSS + custom `.card`, `.btn-*`, `.badge-*`, `.input` utilities

---

## 🔐 Security

- JWT-based stateless authentication (7-day expiry)
- Role-based access control: `ADMIN` and `HEADMASTER` roles
- Password hashing with BCrypt
- CORS configured per environment
- Input validation with Hibernate Validator on all endpoints

---

## 📋 Development Notes

- **Hot reload:** Both frontend (Vite HMR) and backend (Spring DevTools) support hot reload
- **File uploads:** Stored in `uploads/` directory, served as static files
- **Excel export:** Apache POI generates `.xlsx` from form responses
- **Notifications:** Headmasters are auto-notified on GR uploads, meeting schedules, and form assignments

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

Made with ❤️ for Maharashtra's rural education system.
