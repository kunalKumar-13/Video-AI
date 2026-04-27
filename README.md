# Forge AI 🎬

Forge AI is a professional multi-agent orchestrated system designed to transform a free-form narrative into a comprehensive, visually rich movie production plan. Through an automated pipeline, an initial raw story string is systematically converted into a story blueprint, a professional script, a detailed director's scene plan, and an AI-generated image storyboard.

## System Architecture

The project leverages a multi-agent system built entirely on **LangGraph**. The backend uses **FastAPI**, while the frontend is a beautifully themed **Streamlit** dashboard intended for a sleek, minimal, professional cinematic studio aesthetic.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kunalKumar-13/Video-AI.git
   cd Video-AI
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**:
   Create a `.env` file and insert your API keys:
   ```bash
   GROQ_API_KEY="your_api_key_here"
   ```

## How to Run

**Frontend Dashboard (Recommended)**
```bash
streamlit run app.py
```

**FastAPI Backend Server**
```bash
uvicorn api:app --reload
```

## Deployment

This project is configured to deploy correctly to **Streamlit Community Cloud**.
When deploying, make sure to configure the `GROQ_API_KEY` within the App Settings -> Secrets box using standard TOML format.
