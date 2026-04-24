# 🚀 NexusTech: Automated CI/CD DevOps E-Commerce Platform

[![CI/CD Pipeline](https://github.com/srirammulukuntla11/Automated-CI-CD-Pipeline-for-Cloud-Based-Scalable-E-Commerce-Web-Application/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/srirammulukuntla11/Automated-CI-CD-Pipeline-for-Cloud-Based-Scalable-E-Commerce-Web-Application/actions/workflows/ci-cd.yml)
[![Live Demo](https://img.shields.io/badge/Live-Demo-success?style=flat&logo=render)](https://nexustech-cfpm.onrender.com)

## 📌 Project Overview
This project represents a complete, production-grade DevOps lifecycle. It features **NexusTech**, a high-end, full-stack E-Commerce web application that is fully integrated into an automated Continuous Integration and Continuous Deployment (CI/CD) pipeline.

## 🌐 Live Application
**Check out the live deployment here:** [https://nexustech-cfpm.onrender.com](https://nexustech-cfpm.onrender.com)

---

## 🛍️ Application Features (NexusTech)
Built from the ground up to simulate a real-world enterprise application:
- **Custom AI Product Photography:** High-end, locally hosted 3D product renders.
- **Advanced Cart & Checkout:** Glassmorphism UI, auto-syncing backend session cache, and multi-step secure checkout.
- **User Authentication:** Registration, login, and secure user profile dashboards with order history.
- **Financial Logic:** Interactive promo code engine (try `NEXUS20` or `WELCOME10`).
- **Interactive UI/UX:** Dynamic sorting (Price, Ratings), wishlist toggling (❤️), related product recommendations, and modern staggering animations.

---

## ⚙️ DevOps & Architecture
This application serves as the foundation for demonstrating modern CI/CD practices.

### 🛠️ Tech Stack
- **Backend/Frontend:** Python (Flask), Jinja2, Vanilla CSS (Glassmorphism), HTML5.
- **Production Server:** Gunicorn.
- **Containerization:** Docker.
- **Continuous Integration (CI):** GitHub Actions.
- **Continuous Deployment (CD):** Render (PaaS).

### 🔄 The CI/CD Workflow
1. **Push & Trigger:** Developer pushes new code to the `main` branch.
2. **Automated Testing (CI):** GitHub Actions automatically spins up an Ubuntu environment, builds the Docker image, and executes a local container health-check to ensure the build did not break.
3. **Automated Deployment (CD):** Render Web Services detects the successful GitHub commit, automatically pulls the code, installs dependencies (`requirements.txt`), and deploys the update to the live internet seamlessly.

---

## ▶️ Run Locally

### Using Python
```bash
pip install -r requirements.txt
python app.py
```

### Using Docker
```bash
docker build -t devops-app .
docker run -p 5000:5000 devops-app
```
Then navigate to `http://localhost:5000` in your web browser.