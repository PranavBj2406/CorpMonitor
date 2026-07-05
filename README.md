# 🚀 CorpMonitor – AI-Powered Director Change Extraction Platform

CorpMonitor is an AI-powered document intelligence platform that automates the extraction of director appointment, resignation, removal, and re-appointment events from corporate disclosure documents.

Instead of manually reviewing lengthy PDF filings, users can upload a ZIP archive containing corporate documents, and the application identifies director-related changes, extracts structured information using Google's Gemini AI, and presents the results through an intuitive web interface.

---

## 🌟 Problem Statement

Corporate announcements often contain critical governance updates such as:

- Director Appointments
- Director Resignations
- Director Removals
- Director Re-appointments

These updates are typically buried inside lengthy PDF filings, making manual analysis time-consuming and error-prone.

CorpMonitor automates this workflow by transforming unstructured corporate documents into structured JSON data that can be consumed by analysts, compliance teams, or downstream systems.

---

## ✨ Features

- 📄 Upload ZIP archives containing one or more corporate PDF documents
- 🤖 AI-powered information extraction using Google Gemini
- 🏢 Extracts company details and director information
- 📅 Identifies effective dates of director changes
- 🎯 Confidence scoring for extracted information
- 📊 Summary statistics for processed documents
- ⚡ FastAPI backend with asynchronous processing
- 💻 Modern Next.js frontend
- 🐳 Dockerized backend deployment
- ☁️ Production deployment on AWS EC2
- 🔄 Automated CI/CD using GitHub Actions

---

## 🛠 Tech Stack

### Frontend

- Next.js
- TypeScript
- Tailwind CSS
- Framer Motion

### Backend

- FastAPI
- Python
- Pydantic

### AI

- Google Gemini 2.5 Flash API

### Infrastructure

- Docker
- Nginx
- AWS EC2
- GitHub Actions
- Cloudflare Tunnel (HTTPS)

---

## 🏗 System Architecture

```
                User
                  │
                  ▼
      Next.js Frontend (Vercel)
                  │
             HTTPS Request
                  │
                  ▼
        Cloudflare Tunnel
                  │
                  ▼
             Nginx Reverse Proxy
                  │
                  ▼
        Dockerized FastAPI Backend
                  │
                  ▼
        Google Gemini 2.5 Flash
                  │
                  ▼
       Structured Director Changes
```

---

## 📋 Information Extracted

For every detected director change, CorpMonitor extracts:

- Company Name
- Stock Ticker
- Director Name
- Change Type
- Effective Date
- Reason Stated
- Extraction Confidence

---

## 📦 Sample Output

```json
{
  "company_name": "Ramsons Projects Limited",
  "director_name": "Mr. Rakesh Arora",
  "change_type": "appointment",
  "effective_date": "2022-09-29",
  "stock_ticker": "530925",
  "extraction_confidence": "high"
}
```

---

## 🚀 Deployment

### Frontend

- Next.js deployed on **Vercel**

### Backend

- Dockerized FastAPI application
- Hosted on **AWS EC2**
- Reverse proxied using **Nginx**
- Automated deployment via **GitHub Actions**

---

## ⚙️ Running Locally

### Clone Repository

```bash
git clone https://github.com/PranavBj2406/CorpMonitor.git
cd CorpMonitor
```

### Backend

```bash
cd server

python -m venv venv

source venv/bin/activate      # Linux

venv\Scripts\activate         # Windows

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Frontend

```bash
cd my-app

npm install

npm run dev
```

---

## 📌 Future Improvements

- Authentication & User Accounts
- Batch Processing Dashboard
- Export Results as CSV / Excel
- Historical Processing Logs
- Company-wise Analytics
- Cloud Storage Integration
- Kubernetes Deployment

---

## 👨‍💻 Author

**Pranav BJ**

Computer Science Engineering (Data Science)

GitHub: https://github.com/PranavBj2406

---

⭐ If you found this project interesting, consider giving the repository a star.
