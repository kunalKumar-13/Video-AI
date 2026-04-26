# Deployment Guide for Forge AI 🎬

Forge AI can be deployed to several platforms. Here are the best options:

## 1. HuggingFace Spaces (Recommended for AI Apps)
HuggingFace Spaces provides a free tier that is excellent for Streamlit applications.

### Steps:
1.  **Create a New Space**: Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2.  **Configure**:
    *   **Space Name**: `forge-ai` (or your choice).
    *   **SDK**: Select **Streamlit**.
    *   **Visibility**: Public or Private.
3.  **Upload Files**: You can either:
    *   Use `git push` to the space repository.
    *   Upload files manually via the web interface.
4.  **Set Environment Variables**:
    *   Go to **Settings** > **Variables and Secrets**.
    *   Add a **New Secret**:
        *   **Key**: `GROQ_API_KEY`
        *   **Value**: (Your Groq API Key)
5.  **Wait for Build**: HuggingFace will automatically detect `requirements.txt` and `app.py` and start the app.

---

## 2. Streamlit Community Cloud
The easiest way if your code is already on GitHub.

### Steps:
1.  **GitHub**: Ensure your code is pushed to a public GitHub repository.
2.  **Deploy**: Go to [share.streamlit.io](https://share.streamlit.io/).
3.  **App Setup**:
    *   Select your Repository, Branch, and Main file path (`app.py`).
4.  **Secrets**:
    *   Click **Advanced settings**.
    *   In the **Secrets** section, add:
        ```toml
        GROQ_API_KEY = "your_key_here"
        ```
5.  **Launch**: Click **Deploy**.

---

## 3. Docker-based Deployment (Railway, Render, VPS)
Use the provided `Dockerfile`.

### Steps:
1.  **Railway/Render**: Connect your GitHub repository.
2.  **Environment**: Add `GROQ_API_KEY` to the environment variables in the service dashboard.
3.  **Build**: Both Railway and Render will detect the `Dockerfile` and build it automatically.

---

## 4. Local Run (To "Make it Work" now)
If you want to run it locally with the fixes I just applied:

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run**:
    ```bash
    streamlit run app.py
    ```

> [!TIP]
> I have moved your `.env` file to the root directory and added `Pillow` to `requirements.txt`. It should now work perfectly when run locally!
