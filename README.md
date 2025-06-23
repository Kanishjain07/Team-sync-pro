# 🛠️ Team Sync Pro – Backend (Flask)

Team Sync Pro is a role-based team collaboration tool. This repository contains only the backend implementation developed using Flask, with secure authentication, RESTful APIs, and MySQL integration. It provides JSON responses for all routes to be consumed by a separate frontend application.

## 📌 Roles Supported

- 🛡️ Admin  
- 🧑‍💼 Team Lead  
- 👤 Member  

Each role has dedicated API endpoints for dashboards, tasks, and project management with role-based access control.


## 🚀 Backend Features

- 🔐 User Authentication (Signup, Login, Logout using Flask-Login)  
- 🧾 Role-based Authorization (Access control middleware)  
- 📁 Project and Task APIs (CRUD operations)  
- 💬 Chat API (Send/receive messages)  
- 📤 File Upload API  
- 🗓️ Calendar Endpoint (Deadlines, events)  
- 🧑‍💻 User Management (Admin only)  
- 📜 System Logs API  

All features are exposed through RESTful JSON APIs.


## 🧰 Tech Stack

- Framework: Flask  
- ORM: SQLAlchemy  
- Database: MySQL  
- Authentication: Flask-Login  
- API Testing: Postman

## ⚙️ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Kanishjain07/Team-sync-pro.git
cd Team-sync-pro
