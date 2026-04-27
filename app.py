import streamlit as st
import os
import json
from dotenv import load_dotenv
import requests
from io import BytesIO
from PIL import Image

# Load env before any imports that use it
load_dotenv()

from workflows.graph import create_workflow

# Configure page
st.set_page_config(
    page_title="Forge AI - Cinematic Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# High-End Professional Dark Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-base: #000000;
        --bg-surface: #0a0a0a;
        --bg-surface-hover: #1a1a1a;
        --border-color: #222222;
        --text-primary: #ededed;
        --text-secondary: #888888;
        --accent: #2563EB;
        --accent-glow: rgba(37, 99, 235, 0.2);
    }
    
    .stApp {
        background-color: var(--bg-base);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        background-image: 
            linear-gradient(to right, rgba(255,255,255,0.03) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        background-attachment: fixed;
    }
    
    /* Native Header Override */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* All markdown text */
    .stMarkdown p, h1, h2, h3, h4, h5, h6, label, span {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }

    p { color: var(--text-secondary) !important; }

    /* Inputs (Sleek dark mode) */
    .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-size: 0.95rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
        padding: 0.75rem;
    }
    
    .stTextArea textarea:focus, .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: var(--text-secondary) !important;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.1) !important;
    }
    
    /* Premium Button Override - Primary CTA */
    .stButton > button {
        background: var(--text-primary) !important;
        color: var(--bg-base) !important;
        border: 1px solid var(--text-primary) !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px 0 rgba(255,255,255,0.1) !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: transparent !important;
        color: var(--text-primary) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
        border-bottom: 1px solid var(--border-color);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        padding: 12px 0;
        color: var(--text-secondary);
        font-weight: 500;
        transition: color 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: var(--text-primary) !important;
        border-bottom: 2px solid var(--text-primary) !important;
    }
    
    /* Alerts and Cards */
    .stAlert {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    /* Checkbox alignment */
    .stCheckbox {
        display: flex;
        align-items: center;
        height: 100%;
    }

    /* FORGE TITLE CONTAINER */
    .forge-title-container {
        text-align: center;
        padding: 3rem 0 1rem;
    }
    .forge-title {
        font-weight: 700;
        font-size: 3.5rem;
        color: var(--text-primary);
        letter-spacing: -1px;
        margin: 0;
    }
    .forge-title span {
        color: var(--text-secondary) !important;
        font-weight: 300;
    }
    .forge-subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-top: 0.5rem;
        font-weight: 400;
    }
</style>
""", unsafe_allow_html=True)

# Custom HTML Header
st.markdown("""
<div class="forge-title-container">
    <div class="forge-title">Forge <span>AI</span></div>
    <div class="forge-subtitle">Professional Cinematic Story Agent</div>
</div>
""", unsafe_allow_html=True)
st.write("")

# Input Panel Structure - Properly Aligned
narrative_input = st.text_area("Story Narrative", height=140, placeholder="Once upon a time in a cyberpunk city...")

col1, col2 = st.columns([1, 1])
with col1:
    language = st.selectbox("Output Language", ["English", "Hindi", "Spanish", "French", "German", "Japanese", "Korean", "Arabic", "Portuguese", "Russian", "Italian", "Chinese (Mandarin)"])
with col2:
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
    use_mock_data = st.checkbox("🛜 Use Mock Data (Bypass API Billing)", value=False)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
generate_btn = st.button("Generate Production Model →", use_container_width=True)

# Workflow Execution
if generate_btn and narrative_input:
    # Check for API Key
    api_key = os.getenv("GROQ_API_KEY")
    
    if not use_mock_data and not api_key:
        with st.sidebar:
            st.warning("GROQ_API_KEY not found in environment.")
            api_key = st.text_input("Enter Groq API Key", type="password")
            if api_key:
                os.environ["GROQ_API_KEY"] = api_key
            else:
                st.error("Please provide a Groq API Key to proceed.")
                st.stop()

    with st.spinner("Initializing AI Multi-Agent Studio..."):
        workflow = create_workflow()
        
        initial_state = {
            "narrative": narrative_input,
            "language": language,
            "blueprint": None,
            "script": None,
            "scene_plan": None,
            "images": [],
            "evaluation": None,
            "mock_mode": use_mock_data,
            "errors": []
        }
        
    try:
        with st.spinner("AI Multi-Agent Studio is crafting your movie with Groq... This may take a minute."):
            # Run workflow
            result_state = workflow.invoke(initial_state)
            
        st.success("Generation Complete!")
    except Exception as e:
        st.error(f"🚨 Workflow encountered an error: {e}")
        st.stop()
    
    # Output Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📜 Script", "🎥 Scene Plan", "🖼️ Storyboard", "🎞️ Animatic Video", "🧪 Evaluation"])
    
    with tab1:
        if result_state.get("script"):
            st.subheader("Screenplay")
            for scene in result_state["script"].scenes:
                st.markdown(f"**SCENE {scene.scene_number} - {scene.location.upper()}**")
                st.caption(f"Transition: {scene.transition}")
                for dialogue in scene.dialogues:
                    st.write(dialogue)
                st.divider()
        else:
            st.warning("No script generated.")
            
    with tab2:
        if result_state.get("scene_plan"):
            st.subheader("Director's Vision")
            for visual in result_state["scene_plan"].visuals:
                st.markdown(f"**Scene {visual.scene_number}**")
                st.write(f"- 📍 **Location**: {visual.location}")
                st.write(f"- 📷 **Camera Shot**: {visual.camera_shot}")
                st.write(f"- 💡 **Lighting**: {visual.lighting}")
                st.write(f"- 🎭 **Mood**: {visual.mood}")
                st.info(f"**VFX Prompt**: {visual.detailed_image_prompt}")
                st.divider()
        else:
            st.warning("No scene plan generated.")
            
    with tab3:
        if result_state.get("images") and result_state.get("scene_plan"):
            st.subheader("Visual Storyboard")
            cols = st.columns(2)
            
            for idx, (img_url, visual) in enumerate(zip(result_state["images"], result_state["scene_plan"].visuals)):
                col = cols[idx % 2]
                with col:
                    if img_url:
                        st.image(img_url, caption=f"Scene {visual.scene_number}: {visual.mood}", use_column_width=True)
                    else:
                        st.warning(f"Could not generate image for Scene {visual.scene_number}.")
        elif not result_state.get("images"):
            st.warning("No images could be generated. This might be due to API failure or rate limits.")
            
    with tab4:
        st.subheader("Animatic Video Render")
        if result_state.get("images"):
            with st.spinner("Stitching video frames..."):
                frames = []
                # If mock mode is true, get 3 identical frames for demonstration
                urls = result_state["images"]
                if result_state.get("mock_mode") and len(urls) == 1:
                    urls = urls * 3 
                    
                for url in urls:
                    if url:
                        try:
                            # Using a distinct user agent to grab pollination images smoothly
                            headers = {'User-Agent': 'Mozilla/5.0'}
                            response = requests.get(url, headers=headers)
                            img = Image.open(BytesIO(response.content)).convert("RGB")
                            # Resize to 720p roughly
                            img = img.resize((1024, 1024))
                            frames.append(img)
                        except Exception as e:
                            st.error(f"Failed to load frame: {e}")
                
                if frames:
                    gif_path = "story_animatic.gif"
                    frames[0].save(
                        gif_path,
                        save_all=True,
                        append_images=frames[1:],
                        duration=1500,  # 1.5 seconds per scene frame
                        loop=0
                    )
                    st.success("Video Rendering Complete!")
                    st.image(gif_path, use_column_width=True, caption="Storyboard Animatic Video")
                else:
                    st.warning("Couldn't process frames into a video stream.")
        else:
            st.warning("No images generated to stitch into a video.")

    with tab5:
        if result_state.get("evaluation"):
            eval_report = result_state["evaluation"]
            st.subheader("Agent Evaluation Report")
            
            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("Coherence Score", f"{eval_report.coherence_score}/10")
            metric_col2.metric("Pipeline Approved?", "✅ Yes" if eval_report.approved else "❌ No")
            
            st.markdown("### Issues Identified")
            if eval_report.issues_found:
                for issue in eval_report.issues_found:
                    st.write(f"- {issue}")
            else:
                st.success("No critical issues found!")
        else:
            st.warning("No evaluation report generated.")

