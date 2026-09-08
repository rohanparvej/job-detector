# Fake vs Real Job Detector

This application uses machine learning to identify fraudulent job postings by analyzing patterns in descriptions and metadata. It provides a probability score to help users distinguish between legitimate opportunities and potential scams, featuring a fully bundled FastAPI backend and frontend.
>(merged client and server for presentation.)

---

## 🚀 Overview

* **Dataset:** Trained with **18,000 open-source job entries**.
* **Architecture:** Full-stack monolithic setup where FastAPI serves both the API endpoints and the frontend templates directly.
* **Training:** Scripts are provided to allow users to recreate or update the model locally using `uv`.

---

## 🛠️ Setup & Installation

### 1. Prerequisites & Environment
Ensure you have Python 3.10, 3.11, or 3.12 installed, along with `uv` for fast package management.

### 2. Training the Model
> [!IMPORTANT]  
> **The trained model files are not included** in this repository due to file size constraints. You must generate the model locally before starting the server.

1. Navigate to the training or model generation directory.
2. Run the training script to preprocess data and export the model file into your project's `ml/` path.

### 3. Installing Dependencies with `uv`
Set up your virtual environment and install the required dependencies (including the CPU version of PyTorch):

```bash
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install --find-links https://download.pytorch.org/whl/cpu torch fastapi uvicorn numpy
```

*(Alternatively, if a `requirements.txt` is present: `uv pip install -r requirements.txt`)*

### 4. Running the Application
Start the unified FastAPI server:

```bash
python main.py
```
Open your browser and navigate to `http://127.0.0.1:8000` to use the application.

---

## 📁 Project Structure

* `templates/`: Contains the frontend HTML files served directly by FastAPI.
* `static/`: Contains client-side CSS, JavaScript, and asset files.
* `ml/`: Houses the prediction script and trained model files.
* `training/`: Contains the Python training scripts and data preprocessing logic.
* `main.py`: The main FastAPI server entrypoint.

---

## 🌐 Demo
> **Status:** The live demo deployment is currently **turned off for maintenance** and will be back up in due time. Please run the project locally following the installation steps above.

---

## ✨ Future Improvements

* **Browser Extension:** Adapt the model for a Chrome or Firefox extension to scan sites like LinkedIn or Indeed in real-time.
* **Explainable AI (XAI):** Integrate a feature that highlights specific "red flag" keywords (e.g., "Western Union," "No experience needed") to explain the model's decision.
* **Dockerization:** Adding a `docker-compose.yml` file would simplify the setup process for other developers by containerizing the entire stack.
* **Real-time Alerts:** Integrate a notification system to alert users if a job they saved is later flagged as suspicious by the community.