Loan Management System - Django REST API
A robust Django-based Loan Management System with authentication, OTP verification, loan management, repayment tracking, foreclosure, and role-based access control.

📖 Table of Contents

Features
Tech Stack
Installation & Setup
API Endpoints
Authentication
Loan Management (User)
Loan Management (Admin)
Loan Repayment & Foreclosure
Loan Calculation Logic
Deployment Guide
Database Structure
Contact & Support


📌 Features

🔐 User Authentication & Role-Based Access
✅ User Registration with OTP Verification (via Nodemailer)
✅ JWT-based Authentication (Login & Refresh Tokens)
✅ Role-based access (Admin/User)
✅ Admin manages all loans, users manage their own loans.


💰 Loan Management

✅ Apply for a new loan (Specify amount, tenure, interest rate).
✅ View active & past loans with breakdown details.
✅ Admin approval/rejection of loan applications.
✅ Foreclosure of a loan before tenure completion.
✅ Loan repayment tracking with balance updates.


📊 Loan Calculation & Repayment

✅ Monthly installment & total payable amount auto-calculated.
✅ Yearly compound interest calculation.
✅ Foreclosure recalculates interest dynamically.
✅ Admin access to all loan applications and transactions.


🛠️ Tech Stack

Backend: Django, Django REST Framework (DRF)
Authentication: JWT (Simple JWT)
Email OTP Service: Nodemailer (via SMTP)
Database: PostgreSQL
Deployment: Render

📌 Installation & Setup
🔹 Step 1: Clone the Repository
git clone https://github.com/your-github-username/loan-management.git
cd loan-management

🔹 Step 2: Create a Virtual Environment & Install Dependencies
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

pip install -r requirements.txt

🔹 Step 3: Configure Environment Variables
Create a .env file in the project directory:
SECRET_KEY=your_secret_key
DEBUG=True

EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

🔹 Step 4: Apply Migrations & Create Admin User

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
Enter username, email, and password when prompted.

🔹 Step 5: Run the Development Server

python manage.py runserver
API is available at: http://127.0.0.1:8000/

🔍 API Endpoints

1️⃣ Authentication
Method	Endpoint	Description
POST	/api/register/	Register a new user with OTP verification
POST	/api/verify-otp/	Verify OTP for registration
POST	/api/login/	Login & receive JWT tokens
POST	/api/token/refresh/	Refresh JWT token

2️⃣ Loan Management (User)
Method	Endpoint	Description
POST	/api/loans/apply/	Apply for a loan
GET	/api/loans/	View user-specific loans (Admins see all loans)

3️⃣ Loan Management (Admin)
Method	Endpoint	Description
GET	/api/admin/loans/	View all loans (Admin only)
GET	/api/admin/users/	View all registered users
PUT	/api/admin/loans/update/{loan_id}/	Approve/Reject loan application
DELETE	/api/admin/loans/delete/{loan_id}/	Delete a loan record

4️⃣ Loan Repayment & Foreclosure
Method	Endpoint	Description
POST	/api/loans/repay/	Make a repayment
PUT	/api/loans/foreclose/{loan_id}/	Foreclose a loan early
✅ Loan Calculation Logic
📌 Monthly Installment Calculation


monthly_installment = (amount * interest_rate / 100) / 12
📌 Total Payable Amount

total_payable = amount + (amount * interest_rate / 100)
📌 Foreclosure Logic

adjusted_total_payable = amount + (interest_due for months used)
------------------------------------------------------------------

🚀 Deployment Guide

🔹 Step 1: Push Code to GitHub

git init
git add .
git commit -m "Initial Commit"
git branch -M main
git remote add origin https://github.com/your-username/loan-management.git
git push -u origin main
------------------------------------------------------------------
🔹 Step 2: Deploy on Render
Create a new Render Web Service.
Set runtime to Python.
Set Start Command:

gunicorn loan_management.wsgi:application
Add Environment Variables in Render:

DATABASE_URL=<Render PostgreSQL URL>
SECRET_KEY=<your-secret-key>
DEBUG=False

Click Deploy 🚀

🛠️ Database Structure
------------------------------------------------------------------
🔹 Users Table (CustomUser)
id	username	email	role	is_verified
1	admin	admin@example.com	admin	True
2	user1	user1@gmail.com	user	True
------------------------------------------------------------------
🔹 Loans Table (Loan)
id	user_id	amount	term	status	total_payable	monthly_installment
1	2	5000	12	approved	5523.57	460.30
2	3	10000	24	pending	NULL	NULL
------------------------------------------------------------------
🔹 Loan Repayments (LoanRepayment)
id	loan_id	amount_paid	payment_date
1	2	460.30	2025-03-04
------------------------------------------------------------------
