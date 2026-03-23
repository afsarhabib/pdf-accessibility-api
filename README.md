# 📄 PDF Accessibility Validation & Remediation API

A Python-based FastAPI service to scan PDF files for accessibility compliance, identify issues, calculate compliance scores, and provide remediation insights.

---

## 🚀 Features

* Scan PDF files for accessibility issues
* Compute compliance score per file
* Identify issues (metadata, text layer, empty pages)
* Provide fix suggestions
* Generate aggregated report (`/report`)
* Dockerized for easy deployment
* Supports automated evaluation

---

## 🧱 Project Structure

```
pdf-accessibility-api/
│
├── app/
│   ├── main.py
│   ├── api/
│   ├── services/
│   ├── models/
│
├── data/
│   └── sample_pdfs/
│
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup (Local Development)

### 1. Create Virtual Environment

```
python -m venv venv
```

### 2. Activate Environment

#### Windows (PowerShell)

```
venv\Scripts\Activate.ps1
```

#### Windows (CMD)

```
venv\Scripts\activate
```

---

### 3. Install Dependencies

```
pip install fastapi uvicorn PyPDF2 pytest pytest-cov
pip freeze > requirements.txt
```

---

## ▶️ Run Application

```
uvicorn app.main:app --reload
```

Open:

* Swagger UI: http://127.0.0.1:8000/docs
* Health Check: http://127.0.0.1:8000/health

---

## 🧪 API Usage

### 🔹 Scan PDFs

**POST `/scan`**

```
{
  "files": ["data/sample_pdfs/sample1.pdf"]
}
```

---

### 🔹 Get Report

**GET `/report`**

Returns:

* Total files scanned
* Total issues
* Average score
* Worst file
* Compliance summary

---

## 🐳 Docker Setup

### Build & Run

```
docker compose down
docker compose up --build
```

---

### Access

* API: http://localhost:8000
* Docs: http://localhost:8000/docs

---

## 🧪 Testing & Coverage

### Run Tests

```
pytest
```

### Pytest Configuration

```
[pytest]
addopts = --cov=app --cov-report=xml --cov-report=term
```

---

## 🧹 Cleanup Before Submission

### Remove Virtual Environment

```
rmdir /s /q venv
```

---

### Ignore Files

Create `.gitignore`:

```
venv/
__pycache__/
*.pyc
*.log
scan_results.json
```

---

## 📦 Submission Guidelines

Ensure your ZIP contains:

```
my-submission.zip
└── pdf-accessibility-api/
    ├── docker-compose.yml
    ├── Dockerfile
    ├── app/
    ├── requirements.txt
```

---

## 🎯 Evaluation Requirements

* `/health` endpoint returns 200
* API runs via Docker
* Correct JSON response format
* All endpoints functional

---

## 🏆 Hackathon Summary

This project provides a scalable, containerized solution for validating PDF accessibility compliance, generating insights, and suggesting remediation steps.

---

## 👨‍💻 Author

Afsar Habib
Data Platform Architect | Python | GCP
