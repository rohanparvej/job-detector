# Fake vs Real Job Detector

This application uses machine learning to identify fraudulent job postings by analyzing patterns in descriptions and metadata. It provides a probability score to help users distinguish between legitimate opportunities and potential scams. The deployed server has been turned off for maintenance will be up in due time.

---

## 🚀 Overview

* **Dataset:** Trained with **18,000 open-source job entries**.
* **Architecture:** Designed for seamless interaction between the frontend and backend.
* **Training:** Scripts are provided to allow users to recreate or update the model locally.

---

## 🛠️ Setup & Installation

### 1. Training the Model
> [!IMPORTANT]  
> **The trained model files are not included** in this repository due to file size constraints. You must generate the model locally before starting the backend.

1. Navigate to the `training/` folder.
2. Run the training script provided to preprocess data and export the model file.

### 2. Configuration (CORS)
To ensure the frontend and backend work in harmony, please verify the **CORS (Cross-Origin Resource Sharing)** settings:
* **Backend:** Ensure your allowed origins include the frontend URL (e.g., `http://localhost:3000`).
* **Frontend:** Verify the API base URL matches the backend port.

### 3. Execution
Once the model is generated and CORS is configured, start the backend and frontend servers. The system is designed to integrate out of the box.

---

## 📁 Project Structure

* `client/`: The user interface for submitting job details.
* `server/`: The API service handling requests and model inference.
* `server/ml/`: The prediction sript and model will be stored here.
* `training/`: Contains the Python training scripts and data preprocessing logic.

---

## 🌐 Demo
The first beta version is here! Check out-> https://job-detector.pages.dev

---

## ✨ Future Suggestions

* **Browser Extension:** Adapt the model for a Chrome or Firefox extension to scan sites like LinkedIn or Indeed in real-time.
* **Explainable AI (XAI):** Integrate a feature that highlights specific "red flag" keywords (e.g., "Western Union," "No experience needed") to explain the model's decision.
* **Dockerization:** Adding a `docker-compose.yml` file would simplify the setup process for other developers by containerizing the entire stack.
* **Real-time Alerts:** Integrate a notification system to alert users if a job they saved is later flagged as suspicious by the community.
