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

# Dark Cinematic Theme Override
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;800;900&display=swap');
    
    :root {
        --bg-color: #05050A;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes floatBox {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes neonPulse {
        0% { text-shadow: 0 0 5px #FF3366, 0 0 10px #FF3366, 0 0 20px #FF3366; }
        50% { text-shadow: 0 0 2px #FF3366, 0 0 5px #FF9933, 0 0 10px #FF9933; }
        100% { text-shadow: 0 0 5px #FF3366, 0 0 10px #FF3366, 0 0 20px #FF3366; }
    }

    @keyframes rotateBg { 0% { transform: rotate(0deg) scale(1); } 50% { transform: rotate(180deg) scale(1.1); } 100% { transform: rotate(360deg) scale(1); } }
    @keyframes rotateBgReverse { 0% { transform: rotate(360deg) scale(1.1); } 50% { transform: rotate(180deg) scale(1); } 100% { transform: rotate(0deg) scale(1.1); } }

    .stApp {
        background-color: var(--bg-color);
        color: #E2E8F0;
        font-family: 'Outfit', sans-serif;
        overflow: hidden;
    }
    
    /* --- Pure CSS Aurora Shader Background --- */
    .stApp::before {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background-image: 
            radial-gradient(ellipse at 50% 50%, rgba(25, 76, 204, 0.25) 0%, transparent 60%),
            radial-gradient(ellipse at 30% 70%, rgba(255, 51, 102, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 70% 30%, rgba(0, 201, 255, 0.2) 0%, transparent 50%);
        background-blend-mode: screen;
        animation: rotateBg 25s ease-in-out infinite;
        z-index: -2;
        pointer-events: none;
    }
    .stApp::after {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background-image: 
            radial-gradient(ellipse at 60% 40%, rgba(153, 51, 255, 0.15) 0%, transparent 55%),
            radial-gradient(ellipse at 40% 60%, rgba(51, 204, 153, 0.1) 0%, transparent 55%);
        background-blend-mode: screen;
        animation: rotateBgReverse 30s ease-in-out infinite;
        z-index: -1;
        pointer-events: none;
    }
    
    /* Native Header Glassmorphism */
    header[data-testid="stHeader"] {
        background: rgba(5, 5, 10, 0.4) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Text Inputs (Enhanced Glassmorphism) */
    .stTextArea textarea {
        background: rgba(20, 20, 30, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
        color: #fff !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3), 0 8px 32px 0 rgba(0,0,0,0.2);
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stTextArea textarea:focus {
        background: rgba(30, 30, 45, 0.6) !important;
        border-color: #FF3366 !important;
        box-shadow: 0 0 25px rgba(255, 51, 102, 0.3), inset 0 2px 4px rgba(0,0,0,0.5);
        transform: translateY(-2px);
    }
    
    /* Dropdowns (Enhanced Glassmorphism) */
    .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(20, 20, 30, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px;
        color: #fff !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Premium Button Override */
    .stButton > button {
        background: linear-gradient(270deg, #FF3366, #FF9933, #FF3366);
        background-size: 200% 200%;
        animation: gradientShift 3s ease infinite;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 0.75rem 2.5rem;
        font-weight: 800;
        font-size: 1.1rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(255, 51, 102, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.03);
        box-shadow: 0 10px 30px rgba(255, 51, 102, 0.6);
        color: #000;
    }
    
    /* Tabs styling & Animation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(20, 20, 30, 0.3);
        backdrop-filter: blur(10px);
        border-radius: 12px 12px 0 0;
        padding: 12px 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: none;
        color: #888;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(255, 51, 102, 0.15) !important;
        color: #fff !important;
        border-bottom: 2px solid #FF3366 !important;
        box-shadow: 0 -4px 15px rgba(255, 51, 102, 0.1);
    }
    
    /* Alerts and Cards (Glassmorphism) */
    .stAlert {
        background: rgba(20, 20, 30, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 16px;
        color: #fff !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        animation: floatBox 4s ease-in-out infinite;
    }
    /* Hide top padding */
    .block-container {
        padding-top: 1rem;
    }
    
    /* CUSTOM FORGE AI HEADER */
    .forge-title-container {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        position: relative;
    }
    .forge-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 900;
        font-size: 5rem;
        margin: 0;
        background: linear-gradient(270deg, #FF3366, #FF9933, #00C9FF, #FF3366);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 6s ease infinite, floatBox 3s ease-in-out infinite;
        letter-spacing: -3px;
    }
    .forge-title span {
        font-size: 3.5rem;
        vertical-align: top;
    }
    .forge-subtitle {
        font-size: 1.4rem;
        color: #8A92A6;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-top: 0.5rem;
        font-weight: 300;
        animation: fadeIn 3s ease-in;
    }
</style>
""", unsafe_allow_html=True)

# Custom HTML Header
st.markdown("""
<div class="forge-title-container">
    <div class="forge-title">FORGE<span style="-webkit-text-fill-color: #fff; text-shadow: 0 0 15px rgba(255,255,255,0.8);">AI</span></div>
    <div class="forge-subtitle">Narrative to Visual Story Agent</div>
</div>
""", unsafe_allow_html=True)
st.write("---")

# Input Panel
col1, col2 = st.columns([3, 1])
with col1:
    narrative_input = st.text_area("Enter your story", height=200, placeholder="Once upon a time in a cyberpunk city...")
with col2:
    language = st.selectbox("Language", ["English", "Hindi", "Spanish", "French", "German", "Japanese", "Korean", "Arabic", "Portuguese", "Russian", "Italian", "Chinese (Mandarin)"])
    use_mock_data = st.checkbox("🛜 Use Mock Data (Bypass API Billing)", value=False, help="Enable this if your API key is out of credits to bypass remote LLM calls.")
    st.markdown("<br><br>", unsafe_allow_html=True)
    generate_btn = st.button("Generate Production 🚀", use_container_width=True)

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

