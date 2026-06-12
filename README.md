# Online-Shoppers-Intention-Predictor
<img width="1918" height="1031" alt="Screenshot 2026-06-13 042548" src="https://github.com/user-attachments/assets/22d1912b-b2aa-4070-b2e0-00506b953d5b" />
<img width="1917" height="1025" alt="Screenshot 2026-06-13 042718" src="https://github.com/user-attachments/assets/d17dfd83-cd80-409a-b40a-798f14f844fb" />


A complete end-to-end ML Classification project that predicts whether an online shopper will make a purchase or not.

# Live Demo
# Frontend:https://ml-project-eujs.onrender.com
# Swagger UI: https://ml-project-eujs.onrender.com/docs
Tech Stack
Source DB: MySQL
Data Warehouse: PostgreSQL
ETL: Python (Extract → Transform → Load)
ML: Scikit-learn, XGBoost, MLflow
API: FastAPI
Monitoring: Evidently AI
Scheduler: APScheduler
CI/CD: GitHub Actions → Docker Hub → Render
Deploy: Render Free Tier

# Project Structure
ml-classification-project/ ├── api/ # FastAPI app, templates, static files ├── data/ # Raw CSV data and reload script ├── etl/ # Extract, Transform, Load scripts ├── ml/ # Preprocessing, Training, Evaluation, Prediction ├── monitoring/ # Evidently drift report ├── scheduler/ # APScheduler auto retrain job ├── tests/ # Pytest test cases ├── .github/workflows/ # GitHub Actions CI/CD ├── Dockerfile # Docker configuration ├── render.yaml # Render deployment config └── requirements.txt # Python dependencies

# Architecture
MySQL (source) → ETL → PostgreSQL (warehouse) → ML Training → Model → FastAPI → Docker → Render

# Dataset
Source: Online Shoppers Purchasing Intention Dataset
Rows: 12,330
Target: Revenue (Will Purchase or Not)
Features: 17 behavioral and session features
ML Pipeline
ETL — Extract raw data from MySQL, transform, load into PostgreSQL warehouse
Preprocessing — StandardScaler, SelectKBest (top 10 features), SMOTE for class imbalance
Training — Random Forest vs XGBoost, best model selected automatically
Evaluation — Accuracy, Precision, Recall, F1, ROC AUC
MLflow — Experiment tracking and model logging
Model Performance
Metric	Score
Accuracy	91.82%
Precision	89.96%
Recall	94.33%
F1 Score	92.09%
ROC AUC	97.32%
API Endpoints
Method	Endpoint	Description
GET	/	Frontend UI
GET	/health	Health check
POST	/predict	Make prediction
Setup and Run Locally
Prerequisites
Python 3.11
MySQL 8.0
PostgreSQL 15+
Docker (optional)
Steps
# clone repository
git clone https://github.com/ChinmayRumale/ML-Project
cd ml-classification-project

# create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# install dependencies
pip install -r requirements.txt

# setup environment variables
cp .env.example .env
# edit .env with your MySQL and PostgreSQL credentials

# load data into MySQL
python data/reload_data.py

# run ETL pipeline (MySQL → PostgreSQL)
python etl/load.py

# train model
python ml/train.py

# run API
uvicorn api.main:app --reload
Run with Docker
docker build -t shoppers-ml .
docker run -p 8000:8000 --env-file .env shoppers-ml
Run Tests
pytest tests/test_api.py -v
Run Scheduler (Auto Retrain)
python -c "from scheduler.retrain_job import run_pipeline; run_pipeline()"
Generate Drift Report
python monitoring/drift_report.py
CI/CD Pipeline
Push to main branch triggers GitHub Actions
MySQL + PostgreSQL services spin up automatically
Tests run automatically
Docker image built and pushed to Docker Hub
Render auto deploys latest image

# Environment Variables
DB_HOST=localhost DB_PORT=3306 DB_USER=root DB_PASSWORD=your_password DB_NAME=shoppers_db PG_HOST=localhost PG_PORT=5432 PG_USER=postgres PG_PASSWORD=your_password PG_NAME=shoppers_warehouse MLFLOW_TRACKING_URI=./mlruns MODEL_PATH=./ml/model.pkl

# Author
Chinmay Rumale
