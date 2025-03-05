# 🛡️ Decentralized Identity & Authentication System

## 📖 Overview
This project implements a **Decentralized Identity & Authentication System** using **FastAPI (Backend) & React.js (Frontend)**. Users can **sign up, log in, generate Decentralized Identifiers (DIDs), sign messages, and verify their identity** in a secure, decentralized manner.

---

## ⚡ Tech Stack
- **Backend**: Python, FastAPI, PostgreSQL, SQLAlchemy, JWT
- **Frontend**: React.js, React Router, Context API
- **Security**: RSA Key Pairs, JWT Authentication, CORS Handling

---

## 🚀 Features
✅ User Signup with Decentralized Identity (DID)  
✅ Secure Login with JWT Authentication  
✅ DID Public Key Storage & Retrieval  
✅ Message Signing & Signature Verification  
✅ React.js Frontend with Dashboard & Authentication  

---

## 🔧 Setup Instructions

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### **2️⃣ Backend Setup**
```sh
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

### **3️⃣ Configure Environment Variables**
Create a `.env` file in the **backend** folder:
```
DATABASE_URL=postgresql://your_user:your_password@localhost/your_db
SECRET_KEY=your_secret_key
```

### **4️⃣ Run Backend**
```sh
uvicorn main:app --reload
```
(*API will be available at `http://127.0.0.1:8000/docs`*)

### **5️⃣ Frontend Setup**
```sh
cd frontend
npm install
npm start
```
(*Frontend will be available at `http://localhost:3000`*)

---

## 🔗 API Endpoints

### **🔑 Authentication**
| METHOD | ENDPOINT | DESCRIPTION |
|--------|----------|-------------|
| `POST` | `/signup` | Register a new user with DID |
| `POST` | `/login` | Authenticate user & return JWT |

### **👤 User Identity**
| METHOD | ENDPOINT | DESCRIPTION |
|--------|----------|-------------|
| `GET` | `/did` | Retrieve DID & Public Key |
| `POST` | `/verify` | Verify a signed message |

### **🔒 Protected Routes**
| METHOD | ENDPOINT | DESCRIPTION |
|--------|----------|-------------|
| `GET` | `/protected` | Test Authenticated Route |

---

## 📊 Project Metrics

- **🚀 FastAPI Backend** - Lightweight, async-based, and scalable.
- **🔐 RSA Encryption** - Secure identity verification.
- **📦 PostgreSQL Storage** - Secure user identity storage.
- **🖥️ React Frontend** - Interactive UI for authentication & DID retrieval.
- **⚡ CORS Enabled** - Allows cross-origin requests from `http://localhost:3000`.

---

## 🤝 Contributing
1. **Fork** the repository  
2. **Create a new branch** (`git checkout -b feature-branch`)  
3. **Commit changes** (`git commit -m "Added new feature"`)  
4. **Push to GitHub** (`git push origin feature-branch`)  
5. **Open a Pull Request** 🚀  
