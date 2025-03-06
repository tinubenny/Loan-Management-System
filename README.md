# Loan Management System - Django REST API

A robust Django-based Loan Management System with authentication, OTP verification, loan management, repayment tracking, foreclosure, and role-based access control.

## 📖 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Loan Management (User)](#loan-management-user)
  - [Loan Management (Admin)](#loan-management-admin)
  - [Loan Repayment & Foreclosure](#loan-repayment--foreclosure)
- [Loan Calculation Logic](#loan-calculation-logic)
- [Deployment Guide](#deployment-guide)
- [Database Structure](#database-structure)
- [Contact & Support](#contact--support)

---

## 📌 Features

### 🔐 User Authentication & Role-Based Access
- ✅ User Registration with OTP Verification (via Nodemailer)
- ✅ JWT-based Authentication (Login & Refresh Tokens)
- ✅ Role-based access (Admin/User)
- ✅ Admin manages all loans, users manage their own loans.

### 💰 Loan Management
- ✅ Apply for a new loan (Specify amount, tenure, interest rate).
- ✅ View active & past loans with breakdown details.
- ✅ Admin approval/rejection of loan applications.
- ✅ Foreclosure of a loan before tenure completion.
- ✅ Loan repayment tracking with balance updates.

### 📊 Loan Calculation & Repayment
- ✅ Monthly installment & total payable amount auto-calculated.
- ✅ Yearly compound interest calculation.
- ✅ Foreclosure recalculates interest dynamically.
- ✅ Admin access to all loan applications and transactions.

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework (DRF)
- **Authentication:** JWT (Simple JWT)
- **Email OTP Service:** Nodemailer (via SMTP)
- **Database:** PostgreSQL
- **Deployment:** Render

---

## 📌 Installation & Setup

### 🔹 Step 1: Clone the Repository
```sh
git clone https://github.com/tinubenny/Loan-Management-System.git
cd loan-management
```

### 🔹 Step 2: Create a Virtual Environment & Install Dependencies
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 🔹 Step 3: Configure Environment Variables
Create a `.env` file in the project directory:
```ini
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_USER=your-tinujosephc@gmail.com
EMAIL_PASS=fyua pudw fjee xfay
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### 🔹 Step 4: Apply Migrations & Create Admin User
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### 🔹 Step 5: Run the Development Server
```sh
python manage.py runserver
```
API is available at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔍 API Endpoints

### 1️⃣ Authentication
| Method | Endpoint | Description |
|--------|------------|-------------|
| **POST** | `/api/register/` | Register a new user with OTP verification |
| **POST** | `/api/verify-otp/` | Verify OTP for registration |
| **POST** | `/api/login/` | Login & receive JWT tokens |
| **POST** | `/api/token/refresh/` | Refresh JWT token |

### 2️⃣ Loan Management (User)
| Method | Endpoint | Description |
|--------|------------|-------------|
| **POST** | `/api/loans/apply/` | Apply for a loan |
| **GET** | `/api/loans/` | View user-specific loans (Admins see all loans) |

### 3️⃣ Loan Management (Admin)
| Method | Endpoint | Description |
|--------|------------|-------------|
| **GET** | `/api/admin/loans/` | View all loans (Admin only) |
| **GET** | `/api/admin/users/` | View all registered users |
| **PUT** | `/api/admin/loans/update/{loan_id}/` | Approve/Reject loan application |
| **DELETE** | `/api/admin/loans/delete/{loan_id}/` | Delete a loan record |

### 4️⃣ Loan Repayment & Foreclosure
| Method | Endpoint | Description |
|--------|------------|-------------|
| **POST** | `/api/loans/repay/` | Make a repayment |
| **PUT** | `/api/loans/foreclose/{loan_id}/` | Foreclose a loan early |

---

## ✅ Loan Calculation Logic

### 📌 Monthly Installment Calculation
```python
monthly_installment = (amount * interest_rate / 100) / 12
```

### 📌 Total Payable Amount
```python
total_payable = amount + (amount * interest_rate / 100)
```

### 📌 Foreclosure Logic
```python
adjusted_total_payable = amount + (interest_due for months used)
```

---

## 🚀 Deployment Guide

### 🔹 Step 1: Push Code to GitHub
```sh
git init
git add .
git commit -m "Initial Commit"
git branch -M main
git remote add origin https://github.com/tinubenny/Loan-Management-System.git
git push -u origin main
```

### 🔹 Step 2: Deploy on Render
1. Create a new **Render Web Service**.
2. Set runtime to **Python**.
3. Set Start Command:
```sh
gunicorn loan_management.wsgi:application
```
4. Add Environment Variables in Render:
```ini
DATABASE_URL=postgresql://loan_db_nyr8_user:hMQMDHPXdHj0nZnu8ohVxyWBpyx93eQQ@dpg-cv3n6atds78s73dv6ak0-a/loan_db_nyr8
SECRET_KEY=B-iPuW3slMsQHP3DC_cP1c1j8WPcaK8w7LXNdjHg-iLD_GElSZquUhg1HDH1etE0Pz8
DEBUG=False
```
5. Click **Deploy** 🚀

---

## 🛠️ Database Structure

### 🔹 Users Table (CustomUser)
| ID | Username | Email | Role | Is Verified |
|----|---------|-------|------|-------------|
| 1  | admin   | admin@example.com | admin | True |
| 2  | user1   | user1@gmail.com | user | True |

### 🔹 Loans Table (Loan)
| ID | User ID | Amount | Term | Status | Total Payable | Monthly Installment |
|----|--------|--------|------|--------|---------------|--------------------|
| 1  | 2      | 5000   | 12   | approved | 5523.57 | 460.30 |
| 2  | 3      | 10000  | 24   | pending | NULL | NULL |

### 🔹 Loan Repayments (LoanRepayment)
| ID | Loan ID | Amount Paid | Payment Date |
|----|--------|------------|-------------|
| 1  | 2      | 460.30     | 2025-03-04  |

---
