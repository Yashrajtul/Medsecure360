# MedSecure360 🏥

**MedSecure360** is a comprehensive Patient Monitoring and Health Analytics System that integrates wearable device data, medical diagnostics, and administrative healthcare insights. It aims to provide real-time monitoring, efficient diagnostics management, and enhanced patient care using a data-driven approach.

---

## 🚀 Features

- 👨‍⚕️ Patient Management System (Demographics, Conditions, Allergies, etc.)
- 📊 Real-time vitals ingestion from wearable devices
- 🧪 Diagnostic records with structured medical data
- 🛠️ ETL pipeline for ingesting and transforming raw health data
- 🔒 Secure database connectivity via environment configuration
- 📈 Health analytics ready with normalized database schema

---

## 🗂️ Project Structure

    MedSecure360/
    ├── image/
    │   └── ER Diagram - Medsecure360.png 
    ├── data/
    │   ├── medsecure360.csv  
    │   ├── patient_diagnostics.json  
    │   └── wearable_vitals.csv  # ETL csv data
    ├── db/
    │   ├── SQL Queries/
    │   │   └── sql_file_medsecure360.sql
    │   ├── db_connection.py # DB connector with context management
    │   └── etl.py # ETL script for wearable data
    │
    ├── main.py # Entry point of the application
    ├── requirements.txt # Python dependencies
    ├── setup.sh # Shell script to setup virtual env (Linux/Mac)
    ├── .env.py # Sample environment file (rename to env.py)
    └── README.md

---


## ⚙️ Getting Started

### 📥 1. Clone the Repository

    git clone https://github.com/yourusername/MedSecure360.git
    cd MedSecure360


### 🐧 2. Setup on Linux/macOS

    setup.sh

### 🪟 2. Setup on Windows

    setup.bat

### ✅ This will:
* Create a virtual environment
* Install required packages from requirements.txt

### ⚠️ 3. Configure Environment
Rename .env.py to env.py and add your MySQL database credentials:

    host = "your_host"
    user = "your_username"
    password = "your_password"
    database = "your_database"

### ▶️ 4. Run the Project

    python main.py
    
### 🔐 Notes

* Ensure MySQL server is running and accessible.
* Wearable data and diagnostics must align with the normalized schema.
* Comply with data privacy laws (HIPAA/GDPR) for real-world deployments.