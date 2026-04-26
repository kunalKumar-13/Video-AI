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

# Super Mario Retro Theme Override
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    .stApp {
        background-color: #5C94FC;
        background-image: 
            linear-gradient(45deg, rgba(255, 255, 255, 0.1) 25%, transparent 25%, transparent 75%, rgba(255, 255, 255, 0.1) 75%, rgba(255, 255, 255, 0.1)), 
            linear-gradient(45deg, rgba(255, 255, 255, 0.1) 25%, transparent 25%, transparent 75%, rgba(255, 255, 255, 0.1) 75%, rgba(255, 255, 255, 0.1));
        background-size: 60px 60px;
        background-position: 0 0, 30px 30px;
        color: #000;
        font-family: 'Press Start 2P', cursive;
    }
    
    /* Native Header Override */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* All markdown text */
    .stMarkdown p, h1, h2, h3, h4, h5, h6, label, span {
        color: #fff !important;
        text-shadow: 2px 2px 0px #000;
        letter-spacing: 1px;
    }

    /* Text Inputs (Pixel Layout) */
    .stTextArea textarea {
        background: #fff !important;
        border: 4px solid #000 !important;
        border-radius: 0px !important;
        color: #000 !important;
        text-shadow: none !important;
        font-size: 1rem;
        box-shadow: 6px 6px 0px #000;
        transition: all 0.1s linear;
        padding: 10px;
    }
    .stTextArea textarea:focus {
        border-color: #E52521 !important;
        box-shadow: 8px 8px 0px #E52521;
        transform: translate(-2px, -2px);
    }
    
    /* Dropdowns */
    .stSelectbox div[data-baseweb="select"] > div {
        background: #fff !important;
        border: 4px solid #000 !important;
        border-radius: 0px !important;
        color: #000 !important;
        box-shadow: 4px 4px 0px #000;
    }
    .stSelectbox div[data-baseweb="select"] span {
        color: #000 !important;
        text-shadow: none !important;
    }
    
    /* Premium Button Override - Mario Red Style */
    .stButton > button {
        background-color: #E52521 !important;
        color: white !important;
        border: 4px solid #000 !important;
        border-radius: 0px !important;
        padding: 1rem 2rem !important;
        font-family: 'Press Start 2P', cursive !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        text-shadow: 2px 2px 0px #000 !important;
        box-shadow: inset -4px -4px 0px rgba(0,0,0,0.3), 4px 4px 0px #000 !important;
        transition: all 0.1s linear !important;
    }
    .stButton > button:hover {
        background-color: #FBD000 !important;
        color: #000 !important;
        text-shadow: 2px 2px 0px #fff !important;
        transform: translate(2px, 2px) !important;
        box-shadow: inset -4px -4px 0px rgba(0,0,0,0.2), 2px 2px 0px #000 !important;
    }
    .stButton > button:active {
        transform: translate(4px, 4px) !important;
        box-shadow: none !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background: #8B0000;
        border: 4px solid #000;
        border-bottom: none;
        border-radius: 0;
        padding: 12px 24px;
        color: #fff;
        font-family: 'Press Start 2P', cursive;
        font-size: 0.7rem;
    }
    .stTabs [aria-selected="true"] {
        background: #E52521 !important;
        color: #FBD000 !important;
        border: 4px solid #000 !important;
        border-bottom: 4px solid #E52521 !important;
        box-shadow: 4px -4px 0px rgba(0,0,0,0.2);
        margin-bottom: -4px;
        z-index: 10;
        text-shadow: 2px 2px 0px #000;
    }
    
    /* Alerts and Cards */
    .stAlert {
        background-color: #43B047 !important;
        border: 4px solid #000 !important;
        border-radius: 0px !important;
        color: #fff !important;
        box-shadow: 4px 4px 0px #000 !important;
    }
    
    /* Hide top padding */
    .block-container {
        padding-top: 1rem;
    }
    
    /* MARIO TITLE CONTAINER */
    .mario-title-container {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    .mario-title {
        font-family: 'Press Start 2P', cursive;
        font-size: 4rem;
        color: #E52521;
        text-shadow: 4px 4px 0px #000, 8px 8px 0px #fff;
        letter-spacing: -2px;
        animation: bounce 1s ease-in-out infinite alternate;
    }
    .mario-title span {
        color: #FBD000;
    }
    .mario-subtitle {
        font-size: 1rem;
        color: #fff;
        text-shadow: 2px 2px 0px #000;
        margin-top: 2rem;
        animation: blink 1s step-end infinite;
    }
    @keyframes bounce {
        0% { transform: translateY(0); }
        100% { transform: translateY(-15px); }
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
</style>
""", unsafe_allow_html=True)

# Custom HTML Header
st.markdown("""
<div class="mario-title-container">
    <div class="mario-title">SUPER FORGE<span>AI</span></div>
    <div class="mario-subtitle">PRESS START TO GENERATE</div>
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

