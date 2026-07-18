# 🏥 AI Care Notes Assistant

> An AI-powered healthcare documentation system that converts doctor-patient conversations into structured SOAP notes using Azure OpenAI, LangChain, FastAPI, and React.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-0078D4)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# 📖 Overview

AI Care Notes Assistant is an end-to-end healthcare AI application that automates clinical documentation by converting doctor-patient conversations into structured **SOAP (Subjective, Objective, Assessment, Plan)** notes.

The system combines Speech-to-Text, Named Entity Recognition (NER), Protected Health Information (PHI) detection, Retrieval-Augmented Generation (RAG), and Large Language Models (LLMs) to streamline medical documentation while preserving clinical accuracy.

---

# ✨ Features

- 🎤 Speech-to-Text processing
- 🩺 Automatic SOAP Note Generation
- 🤖 Azure OpenAI powered LLM responses
- 🔒 PHI (Protected Health Information) Detection
- 🏥 Medical Entity Extraction
- ⚡ FastAPI REST Backend
- 💻 React Frontend
- ☁ Azure Integration
- 📂 Modular Project Architecture
- 🔑 Azure Key Vault Integration
- 📊 Database Support
- 🔄 Queue-based Processing Pipeline

---

# 🏗 System Architecture

```text
                    Doctor & Patient
                           │
                           ▼
                  Audio Conversation
                           │
                           ▼
               Speech-to-Text (Azure)
                           │
                           ▼
          PHI Detection & Entity Extraction
                           │
                           ▼
              LangChain Processing Pipeline
                           │
                           ▼
                 Azure OpenAI GPT Model
                           │
                           ▼
              Structured SOAP Note Output
                           │
                           ▼
                    React Dashboard
```

---

# 📁 Project Structure

```text
ai-care-notes-assistant/
│
├── backend/
│   ├── app/
│   ├── worker/
│   ├── requirements.txt
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠 Tech Stack

### Backend

- Python
- FastAPI
- LangChain
- Azure OpenAI
- Azure Key Vault
- Azure Speech Services

### Frontend

- React
- JavaScript
- HTML
- CSS

### AI & NLP

- GPT Models
- Named Entity Recognition
- PHI Detection
- Prompt Engineering

### Cloud

- Microsoft Azure
- Azure OpenAI
- Azure Storage
- Azure Key Vault

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/Iffrahkhan-harihar/ai-care-notes-assistant.git

cd ai-care-notes-assistant
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm start
```

---

# 🔑 Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=

AZURE_SPEECH_KEY=
AZURE_SPEECH_REGION=

DATABASE_URL=

JWT_SECRET=
```

---

# ▶ Running the Application

Start the backend

```bash
cd backend

uvicorn main:app --reload
```

Start the frontend

```bash
cd frontend

npm start
```

---

# 📡 API

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/upload-audio` | Upload doctor-patient conversation |
| POST | `/generate-notes` | Generate SOAP notes |
| GET | `/health` | Health Check |
| GET | `/docs` | Swagger Documentation |

---

# 🔄 Workflow

1. Upload doctor-patient audio
2. Convert speech to text
3. Detect Protected Health Information
4. Extract medical entities
5. Send processed transcript to Azure OpenAI
6. Generate structured SOAP Notes
7. Display results in React dashboard

---

# 📈 Future Improvements

- Multi-language support
- Real-time transcription
- Doctor authentication
- Hospital EMR integration
- Voice diarization
- Fine-tuned medical LLM
- Docker deployment
- Kubernetes support

---

# 🤝 Contributing

Contributions are welcome!

If you'd like to improve the project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Iffrahkhan Harihar**

AI Engineer | Generative AI | Computer Vision | Deep Learning

LinkedIn:
https://linkedin.com/in/iffrahkhan-harihar-3327a0401

GitHub:
https://github.com/Iffrahkhan-harihar
