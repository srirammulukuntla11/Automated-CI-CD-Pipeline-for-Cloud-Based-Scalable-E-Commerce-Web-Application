# 🚀 Automated CI/CD Pipeline for Cloud-Based Web Application

## 📌 Project Overview
This project demonstrates a complete DevOps pipeline where a Flask web application is containerized using Docker and automatically built and tested using GitHub Actions.

## 🛠️ Tech Stack
- Python (Flask)
- Docker
- GitHub Actions
- AWS (EC2)

## 🔄 Workflow
1. Code pushed to GitHub
2. GitHub Actions triggers CI/CD pipeline
3. Docker image is built
4. Container is tested automatically
5. Ready for deployment on AWS

## ▶️ Run Locally

```bash
docker build -t devops-app .
docker run -p 5000:5000 devops-app