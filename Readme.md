# Chatbot Backend – FastAPI + PDF + LLM

A FastAPI-based backend that allows users to authenticate, upload PDF files, and query them using a Large Language Model (LLM). The app handles PDF text extraction, integrates with a chosen LLM API, and supports JWT-based authentication. It is fully containerized using Docker for easy deployment.

---

## ⚙️ Project Setup (Local) (1)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/rohithrkrishnan177/chatbot_backend.git
cd chatbot-backend
```

### 2️⃣ Create and Activate Virtual Environment
```bash
python -m venv venv
# Activate the environment
venv\Scripts\activate      # (Windows)
source venv/bin/activate     # (Linux/macOS)
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Environment Variables
You can create a `.env` file or export manually:
```bash
# Example environment variables
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
LLM_API_KEY=your_llm_api_key_here
```

### 5️⃣ Run the Application
```bash
uvicorn app.main:app --reload
```
Open the docs at 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🐳 Run Using Docker(2)

### Build and Run
```bash
docker build -t chatbot-backend .
docker run -d -p 8000:8000 chatbot-backend
```

Access the app at 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## LLM API Used

**Chosen Model:** Mistral (via Hugging Face API)

**Reason for Selection:**
- Provides free and reliable inference endpoints.
- Lightweight and efficient for short document queries.
- Easy integration using `httpx` without needing a heavy client library.
- Good balance of speed and contextual understanding.

---

## Authentication Flow

The application uses **JWT-based authentication**.  
- `/auth/signup`: Register new users.  
- `/auth/login`: Authenticate users and receive a JWT token.  
- Authenticated routes require the `Authorization: Bearer <token>` header.

---

## Endpoints Overview

| Endpoint       | Method | Auth | Description |
|----------------|--------|------|--|
| `/auth/signup` | POST | ❌ | Register a new user |
| `/auth/login`  | POST | ❌ | Login and receive JWT token |
| `/auth/logout` | POST | ✅ | Logout API |
| `/chat/stream` | POST | ✅ | Stream responses from LLM |

---

## Example Requests

### Signup
**POST** `/auth/signup`
```json
{
  "username": "testuser",
  "password": "testpassword"
}
```
**Response:**
```json
{
  "message": "User created successfully"
}
```

### Login
**POST** `/auth/login`
```json
{
  "username": "testuser",
  "password": "testpassword"
}
```
**Response:**
```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

### Ask Question with PDF
**POST** `/chat/stream`
Form-data:
- file: `document.pdf`
- question: `Summarize this document`

Header:
```
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "answer": "This document discusses..."
}
```

---

## Tech Stack

- **FastAPI** — high-performance web framework  
- **PyMuPDF** — for PDF text extraction  
- **httpx** — async API calls to LLM  
- **python-jose & passlib** — JWT authentication  
- **Docker** — for containerization  

---

## Author

**Rohith R Krishnan**  
[LinkedIn](https://www.linkedin.com/in/rohith-krishnan-32a758199/)

---
