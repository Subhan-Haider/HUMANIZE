import os
from dotenv import load_dotenv

# Initialize environment FIRST
load_dotenv()

import streamlit as BlizFlow
import streamlit as st # Keep st alias for internal convenience but BlizFlow is now the primary name
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from transformer.neural import NeuralTextHumanizer
from transformer.smart_system import SmartHumanizationOrchestrator
from transformer.perplexity_analyzer import PerplexityAnalyzer, IterativeHumanizer
from transformer.detector_tester import DetectorTester
from nltk.tokenize import word_tokenize
import difflib
import time
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None

try:
    from readability import Readability
except ImportError:
    Readability = None

# --- CACHING FOR PERFORMANCE ---
@st.cache_resource(show_spinner=False)
def load_neural_model():
    with st.spinner("🧠 Initializing BlizFlow AI... (First run may take a minute to download ~500MB)"):
        return NeuralTextHumanizer()

def main():
    """
    Main application entry point with polished UI.
    """
    download_nltk_resources()

    # --- PAGE CONFIG ---
    st.set_page_config(
        page_title="BlizFlow AI",
        page_icon="blizflow_favicon.png",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://blizflow.site/support',
            'Report a bug': "https://blizflow.site/bugs",
            'About': "# BlizFlow AI v3.1.5\n\n**The Gold Standard in Neural Stealth Writing.**\n\n© 2026 BlizFlow Labs. All rights reserved. Built with BlizFlow Ghost-Stealth Technology."
        }
    )



    # --- PREMIUM LIGHT CSS ---
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');

        /* Background & Global */
        .stApp {
            background: #f8fafc;
            font-family: 'Inter', sans-serif;
            color: #1e293b;
        }

        /* Titles */
        h1, h2, h3 {
            font-family: 'Outfit', sans-serif !important;
            color: #0f172a !important;
            font-weight: 800 !important;
            letter-spacing: -0.025em;
        }

        /* Premium Containers */
        [data-testid="stVerticalBlock"] > div > div > div.stBox {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        }

        /* Inputs */
        .stTextArea textarea {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            color: #334155 !important;
            font-size: 16px !important;
            padding: 1rem !important;
            transition: all 0.2s ease;
            box-shadow: inset 0 2px 4px 0 rgba(0,0,0,0.02);
        }
        .stTextArea textarea:focus {
            border-color: #6366f1 !important;
            background: #fff !important;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1) !important;
        }

        /* Buttons */
        .stButton button {
            background: #6366f1 !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            height: 48px !important;
            border: none !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2) !important;
        }
        .stButton button:hover {
            background: #4f46e5 !important;
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3) !important;
        }
        
        /* Secondary Style Button */
        button[kind="secondary"] {
            background: white !important;
            color: #475569 !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        }

        /* Sidebar Styling (Premium Glass) */
        [data-testid="stSidebar"] {
            background-color: #fcfcfd !important;
            border-right: 1px solid #f1f5f9 !important;
        }
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            padding: 2.5rem 1.5rem !important;
            gap: 2rem !important;
        }
        [data-testid="stSidebar"] .stMarkdown h2 {
            font-size: 1.6rem !important;
            letter-spacing: -0.03em;
            color: #0f172a !important;
            font-family: 'Outfit', sans-serif !important;
            margin-bottom: 0.5rem !important;
        }
        [data-testid="stSidebar"] .stMarkdown h3 {
            font-size: 0.72rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.12em !important;
            color: #6366f1 !important;
            margin-top: 2rem !important;
            margin-bottom: 0.75rem !important;
            font-weight: 800 !important;
            opacity: 0.8;
        }
        
        /* Custom Sidebar Inputs */
        /* Premium Sidebar Tiles */
        div[data-testid="stRadio"] div[role="radiogroup"] {
            gap: 12px !important;
            padding: 10px 0 !important;
        }
        div[data-testid="stRadio"] label[data-baseweb="radio"] {
            background: #ffffff !important;
            border: 1px solid #edf2f7 !important;
            border-radius: 14px !important;
            padding: 14px 18px !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
            margin-bottom: 2px !important;
            cursor: pointer !important;
        }
        div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
            border-color: #6366f1 !important;
            background-color: #f8fafc !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.08) !important;
        }
        div[data-testid="stRadio"] label[data-baseweb="radio"] [data-baseweb="radio__label"] {
            font-weight: 600 !important;
            color: #1e293b !important;
            font-size: 0.92rem !important;
        }
        div[data-testid="stRadio"] label[data-baseweb="radio"] [data-testid="stCaptionContainer"] {
            font-size: 0.72rem !important;
            color: #94a3b8 !important;
            line-height: 1.4 !important;
            margin-top: 4px !important;
        }
        /* Active State */
        div[data-testid="stRadio"] label[data-baseweb="radio"] div:first-child[aria-checked="true"] + span {
            color: #6366f1 !important;
            font-weight: 700 !important;
        }
        
        /* Modern Slider */
        .stSlider [data-testid="stTickBar"] {
            display: none;
        }
        .stSlider [data-testid="stThumb"] {
            border: 2px solid #6366f1 !important;
        }
        
        /* Stylish Expanders */
        .stExpander {
            background: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }
        .stExpander summary {
            font-weight: 600 !important;
            color: #334155 !important;
        }

        /* Metrics Display */
        [data-testid="stMetricValue"] {
            color: #6366f1 !important;
            font-family: 'Outfit', sans-serif;
        }
        
        /* Analysis Card */
        .metric-card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            border: 1px solid #e2e8f0;
            margin-top: 20px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        }
        
        /* Standard Button Reset */
        .stButton button {
            width: 100% !important;
        }

        /* --- RESPONSIVE MEDIA QUERIES --- */
        @media screen and (max-width: 768px) {
            h1 { font-size: 1.75rem !important; }
            .stBox { padding: 1.5rem !important; }
            [data-testid="stVerticalBlock"] { gap: 1rem !important; }
            
            /* Compact Header for Mobile */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
                text-align: center !important;
            }
            .stImage { margin: 0 auto !important; }
            
            /* Stack buttons on mobile */
            div[data-testid="column"] button {
                width: 100% !important;
                margin-bottom: 10px !important;
            }
            
            /* Adjust sidebar for mobile */
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
                padding: 1.5rem 1rem !important;
            }
        }

        @media screen and (max-width: 480px) {
            h1 { font-size: 1.5rem !important; }
            [data-testid="stMetricValue"] { font-size: 1.25rem !important; }
        }

        /* Standard Button Reset */
        .stButton button {
            width: 100% !important;
        }

        /* --- THE PURGE: Hide All Streamlit Artifacts --- */
        #MainMenu {visibility: hidden; display: none !important;}
        footer {visibility: hidden; display: none !important;}
        [data-testid="stHeader"] {display: none !important;}
        [data-testid="stStatusWidget"] {display: none !important;}
        [data-testid="stAppToolbar"] {display: none !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        [data-testid="stDecoration"] {display: none !important;}
        div.stDeployButton {display: none !important;}
        
        /* Eliminate the 'Source file changed' rerun bar & Status Tooltips */
        div[data-testid="stNotification"] {display: none !important;}
        div.stException {display: none !important;}
        
        /* Hide all Deploy Dialogs and Popups */
        iframe[title="streamlit_status_widget"] {display: none !important;}
        div[role="dialog"] {display: none !important;}
        div[data-testid="stDialog"] {display: none !important;}
        .stDeployButton {display: none !important;}
        
        /* Hide the 'Running...' indicator specifically */
        div[data-testid="stStatusWidget"] {
            visibility: hidden !important;
            display: none !important;
        }

        /* Eliminate the top padding that remains after hiding header */
        .block-container {
            padding-top: 3.5rem !important;
            padding-bottom: 2rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )




    # --- HEADER ---
    col_logo, col_title, col_links = st.columns([1, 4, 1.5])
    with col_logo:
        try:
            st.image("blizflow_logo.png", width=90)
        except:
            st.markdown("### ⚡")
            
    with col_title:
        st.markdown("<h1 style='margin-bottom: 0;'>BlizFlow AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; font-size: 1.1rem; font-weight: 500;'>The Gold Standard in Neural Stealth Writing</p>", unsafe_allow_html=True)

    with col_links:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: right; display: flex; flex-direction: column; gap: 6px; align-items: flex-end;'>
                <a href='https://github.com/Subhan-Haider/HUMANIZE' target='_blank' style='text-decoration: none;'>
                    <button style='background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 4px 10px; cursor: pointer; color: #475569; font-weight: 600; font-family: "Inter", sans-serif; display: flex; align-items: center; gap: 8px; width: 140px; justify-content: center; font-size: 0.8rem;'>
                        <svg height="16" width="16" viewBox="0 0 16 16"><path fill="#475569" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
                        GitHub
                    </button>
                </a>
                <a href='https://blizflow.site' target='_blank' style='text-decoration: none;'>
                    <button style='background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 4px 10px; cursor: pointer; color: #475569; font-weight: 600; font-family: "Inter", sans-serif; display: flex; align-items: center; gap: 8px; width: 140px; justify-content: center; font-size: 0.8rem;'>
                        <svg height="16" width="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" /></svg>
                        Website
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 2px; background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%); margin: 24px 0; border-radius: 1px; opacity: 0.3;'></div>", unsafe_allow_html=True)



    # --- SIDEBAR ---
    with st.sidebar:
        # Custom Sidebar Branding
        try:
            col_side_l, col_side_c, col_side_r = st.columns([1, 2, 1])
            with col_side_c:
                st.image("blizflow_logo.png", use_container_width=True)
            st.markdown("<div style='text-align: center; font-size: 0.65rem; font-weight: 800; color: #6366f1; letter-spacing: 0.23em; margin-bottom: 2rem;'>POWERED BY BLIZFLOW</div>", unsafe_allow_html=True)
        except:
            st.markdown("### 💠 BLIZFLOW AI")

        st.header("⚙️ Settings")
        
        # API Key Management
        env_key = os.getenv("OPENROUTER_API_KEY", "")
        if not env_key:
            st.warning("🔐 API Key required to run the engine")
            manual_key = st.text_input("Enter OpenRouter Key", type="password", help="Get yours at openrouter.ai")
            if manual_key:
                os.environ["OPENROUTER_API_KEY"] = manual_key
                st.success("Key applied!")
        
        # We don't show a success message if loaded via .env to keep the UI clean for production

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        mode = st.radio(
            "Transformation Engine",
            ["Standard (Fast)", "Deep AI (Neural)", "🧠 Smart Adaptive", "🎯 Perplexity-Guided (Best)"],
            captions=["Best for quick edits", "Best for heavy rewriting", "AI analyzes & optimizes", "Iterates until human-like"]
        )

        st.markdown("---")
        st.subheader("🎭 Quality Profile")
        
        tone = st.selectbox(
            "Writing Tone",
            ["Balanced", "Professional", "Academic", "Casual", "Creative"],
            help="Adjusts the 'vibe' of the humanized output."
        )
        
        audience = st.selectbox(
            "Target Audience",
            ["General", "Business Executives", "Students", "Technical Experts", "Casual Readers"],
            help="Tailors the vocabulary and complexity for specific readers."
        )

        st.markdown("---")
        if mode == "Standard (Fast)":
            st.subheader("⚡ Options")
            use_passive = st.checkbox("Passive Voice", value=True)
            use_synonyms = st.checkbox("Synonym Swaps", value=True)
            academic_trans = st.checkbox("Transitions", value=True)
            stealth_level = 3 # Default
            use_artifacts = False
            preserve_formatting = True # Default
            use_emojis = False # Default
        else:
            st.subheader("🛡️ Stealth Level")
            stealth_level = st.select_slider(
                "Humanization Level",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: {
                    1: "1. Light (Blog Safe)", 
                    2: "2. Balanced (Opinions)", 
                    3: "3. Natural (Imperfections)", 
                    4: "4. Wild (Anti-Detector)", 
                    5: "5. NUCLEAR (GPTZero 3.15b Bypass)"
                }[x]
            )
            
            if stealth_level >= 4:
                st.warning("Levels 4+ add significant 'chaos' to bypass detectors. Output may require light editing.")
            
            use_artifacts = st.checkbox("🔮 Magic Bypass (Anti-Detector)", value=False, help="Injects invisible characters to break AI detectors.")
            
            st.markdown("---")
            st.subheader("🛠️ Custom Controls")
            preserve_formatting = st.checkbox("🔒 Preserve Structure", value=True, help="Prevents the AI from merging paragraphs or changing structure.")
            use_emojis = st.checkbox("😉 Emoji Injection", value=False, help="Injects human-like emojis to bypass robotic detection.")
            
            st.info("Neural mode rewrites sentences to bypass AI detection patterns.")
            use_passive, use_synonyms, academic_trans = False, False, False

        st.markdown("---")
        st.subheader("📁 Bulk Process")
        uploaded_file = st.file_uploader("Upload Document (PDF/DOCX)", type=['pdf', 'docx'])
        if uploaded_file:
            st.success(f"File '{uploaded_file.name}' loaded!")

        st.markdown("---")
        with st.sidebar.expander("ℹ️ About BlizFlow AI"):
            st.markdown("""
                **BlizFlow AI** is a premium neural steering engine developed by **Subhan Haider**.
                
                Our mission is to protect the integrity of human writing in an increasingly automated world. 
                Using advanced **"Ghost Stealth"** technology and multi-pass linguistic shattering, we ensure your 
                voice remains uniquely yours and undetected by even the most aggressive AI classifiers.
                
                **Subhan-Haider Lab (c) 2026**
                Built with BlizFlow, Transformers & OpenRouter.
                
                ---
                **Built for:**
                - Developers & Researchers
                - Content Integrity Teams
                - Privacy-Conscious Writers
                
                *Version 3.1.5 (Nuclear Update)*
            """)

        with st.sidebar.expander("⚖️ Terms & Privacy"):
            st.markdown("""
                ### 1. Usage Ethics
                BlizFlow AI is intended for protecting original human thoughts from being incorrectly flagged as AI. We do not support or condone the use of this tool for academic dishonesty or spam.
                
                ### 2. Data Privacy
                We process your text in real-time. No input data is stored on our servers after the humanization session is closed.
                
                ### 3. Attribution
                This software is part of the **Subhan Haider Open-Link Initiative**. Please provide proper attribution when using this tool in research or commercial projects.
                
                ### 4. No Warranty
                The software is provided "as is", without warranty of any kind.
            """)

    # --- FILE UPLOAD HANDLING ---
    if uploaded_file and not st.session_state.get('main_input_text', ''):
        try:
            content = ""
            if uploaded_file.type == "application/pdf":
                if PyPDF2:
                    reader = PyPDF2.PdfReader(uploaded_file)
                    for page in reader.pages:
                        content += page.extract_text() + "\n"
                else:
                    st.error("PDF processing library (PyPDF2) is not installed.")
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                if docx:
                    doc = docx.Document(uploaded_file)
                    for para in doc.paragraphs:
                        content += para.text + "\n"
                else:
                    st.error("Word processing library (python-docx) is not installed.")
            
            if content:
                st.session_state["main_input_text"] = content
                st.toast("Document content loaded successfully!")
                st.rerun()
        except Exception as e:
            st.error(f"Error reading file: {e}")

    # --- MAIN LAYOUT ---
    st.markdown('<div class="stBox">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### 📝 Original Text')
        if "main_input_text" not in st.session_state:
            st.session_state["main_input_text"] = ""
            
        user_text = st.text_area(
            "Input", 
            value=st.session_state["main_input_text"], 
            height=400, 
            placeholder="Paste your AI-generated text here...", 
            key="input_area_widget",
            label_visibility="collapsed"
        )
        st.session_state["main_input_text"] = user_text

        # Real-time AI Detection for Input
        if user_text:
            tester = DetectorTester()
            results = tester.test_with_local_heuristics(user_text)
            prob = results['ai_probability']
            
            # Premium AI Audit Card
            color = "#ef4444" if prob > 60 else "#f59e0b" if prob > 30 else "#22c55e"
            bg_color = "rgba(239, 68, 68, 0.05)" if prob > 60 else "rgba(245, 158, 11, 0.05)" if prob > 30 else "rgba(34, 197, 94, 0.05)"
            
            st.markdown(f"""
                <div style="background: {bg_color}; border-radius: 16px; padding: 20px; border: 1px solid {color}33; margin-bottom: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 1.2rem;">🕵️</span>
                            <span style="font-weight: 700; color: #1e293b; font-size: 0.85rem; letter-spacing: 0.05em; text-transform: uppercase;">Raw AI Density</span>
                        </div>
                        <span style="color: {color}; font-weight: 800; font-size: 1.4rem; font-family: 'Outfit', sans-serif;">{prob:.1f}%</span>
                    </div>
                    <div style="background: rgba(0,0,0,0.05); height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: {color}; width: {prob}%; height: 100%; border-radius: 4px; box-shadow: 0 0 10px {color}66; transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);"></div>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.75rem; color: #64748b; font-weight: 500;">
                        { "⚠️ High risk of detection" if prob > 60 else "🔸 Moderate AI patterns found" if prob > 30 else "✅ Low AI signature detected" }
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Input Controls
        c1, c2 = st.columns([1, 1])
        with c1:
            st.caption(f"Words: {len(user_text.split()) if user_text else 0}")
        with c2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state["main_input_text"] = ""
                st.session_state.result = ""
                st.rerun()
        
    with col2:
        st.markdown('### ✨ Humanized Result')
        if 'result' not in st.session_state:
            st.session_state.result = ""
        if 'history' not in st.session_state:
            st.session_state.history = []
            
        if st.session_state.result:
            # Use a premium styled text area that is guaranteed to be visible
            st.text_area(
                "Final Humanized Text", 
                value=st.session_state.result, 
                height=400, 
                key="rendered_result_area",
                help="This is your bypass-ready text. Use the buttons below to copy or download.",
                label_visibility="collapsed"
            )
            
            st.success("✨ Your humanized variation is ready!")
            
            # Result Controls
            rc1, rc2, rc3 = st.columns([1, 1, 1])
            with rc1:
                st.caption(f"Words: {len(st.session_state.result.split())}")
            with rc2:
                st.download_button(
                    label="📥 Download",
                    data=st.session_state.result,
                    file_name="humanized_text.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with rc3:
                # Use st.code as the primary copy-friendly container
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    # Fallback script for broader compatibility
                    import json
                    safe_text = json.dumps(st.session_state.result)
                    st.components.v1.html(f"""
                        <script>
                        parent.navigator.clipboard.writeText({safe_text});
                        </script>
                    """, height=0)
                    st.toast("Copied to clipboard!", icon="✅")
            
            # History Tracking
            if st.session_state.result and st.session_state.result not in [h['text'] for h in st.session_state.history]:
                st.session_state.history.append({
                    "time": time.strftime("%H:%M:%S"),
                    "text": st.session_state.result,
                    "level": stealth_level
                })
                if len(st.session_state.history) > 5: st.session_state.history.pop(0)

            # Diff View
            with st.expander("🔍 View Changes (Visual Diff)"):
                d = difflib.HtmlDiff()
                diff_table = d.make_table(user_text.splitlines(), st.session_state.result.splitlines())
                st.markdown(f'<div style="overflow-x:auto;">{diff_table}</div>', unsafe_allow_html=True)
                    
        else:
            st.info("Humanized variation will appear here after clicking the button below.")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- READABILITY DASHBOARD ---
    if st.session_state.result and Readability:
        st.markdown("### 📊 Readability Dashboard")
        try:
            r = Readability(st.session_state.result)
            fk = r.flesch_kincaid()
            ease = r.flesch()
            gunning = r.gunning_fog()
            
            r_col1, r_col2, r_col3 = st.columns(3)
            with r_col1:
                st.metric("Grade Level", fk.grade_level)
                st.caption("Flesch-Kincaid Grade")
            with r_col2:
                st.metric("Reading Ease", f"{ease.score:.1f}")
                st.caption(ease.ease)
            with r_col3:
                st.metric("Gunning Fog", f"{gunning.score:.1f}")
                st.caption(f"Level: {gunning.grade_level}")
        except:
            st.caption("Readability metrics unavailable for very short text.")
    elif st.session_state.result and not Readability:
        st.caption("📊 Readability Dashboard unavailable (library not found).")

    # --- SIDEBAR HISTORY ---
    with st.sidebar:
        st.markdown("---")
        st.subheader("📜 Session History")
        if not st.session_state.history:
            st.caption("No history yet.")
        else:
            for i, item in enumerate(reversed(st.session_state.history)):
                with st.expander(f"🕒 {item['time']} (Lvl {item['level']})"):
                    st.text(item['text'][:200] + "...")
                    if st.button(f"Restore", key=f"rest_{i}_{item['time']}"):
                        st.session_state.result = item['text']
                        # Input text is not managed here to avoid confusion, 
                        # but we could restore it if we saved it in history
                        st.rerun()

    # --- ACTION BAR ---
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        if st.button("🚀 Humanize Now", type="primary", use_container_width=True):
            if not user_text:
                st.warning("Please enter some text first.")
            else:
                process_text(user_text, mode, stealth_level, use_artifacts, tone, audience, preserve_formatting, use_emojis)
                
    with col_btn2:
        if st.button("🔄 Regenerate", use_container_width=True):
            if not user_text:
                st.warning("Original text is needed to generate another variation.")
            else:
                process_text(user_text, mode, stealth_level, use_artifacts, tone, audience, preserve_formatting, use_emojis)
    
    with col_btn3:
        if st.button("🔎 Analyze Stealth", use_container_width=True):
            if not st.session_state.result:
                st.warning("Please humanize text first.")
            else:
                with st.spinner("Analyzing AI detection..."):
                    tester = DetectorTester()
                    result = tester.test_with_local_heuristics(st.session_state.result)
                    recommendations = tester.recommend_improvements(result)
                    
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.subheader("🕵️ Stealth Analysis")
                    
                    m_col1, m_col2 = st.columns(2)
                    with m_col1:
                        st.metric("AI Probability", f"{result['ai_probability']:.1f}%")
                    with m_col2:
                        st.metric("Human Likeness", f"{result['human_probability']:.1f}%")
                    
                    st.markdown("**Core Checks:**")
                    for check, status in result['details'].items():
                        st.markdown(f"{status} **{check.replace('_', ' ').title()}**")
                    
                    st.markdown("---")
                    st.markdown("**💡 Optimization Tips:**")
                    for rec in recommendations:
                        st.markdown(f"- {rec}")

    # --- FOOTER ---
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 1px; background: #e2e8f0; width: 100%; opacity: 0.5;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='text-align: center; color: #94a3b8; font-size: 0.8rem; padding: 25px 0; font-family: "Inter", sans-serif; letter-spacing: 0.025em;'>
            © 2026 <b>BlizFlow AI Labs</b>. All rights reserved. <br>
            <span style='opacity: 0.7;'>The Gold Standard in Neural Stealth Writing | Ghost Stealth Engine v3.1.5</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- RESULTS LOGIC ---
def process_text(text, mode, stealth_level, use_artifacts, tone, audience, preserve_formatting=True, use_emojis=False):
    # Premium Loading Indicator
    loader = st.empty()
    loader.markdown("""
        <div style="background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 20px; display: flex; align-items: center; gap: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02); margin-bottom: 20px;">
            <div class="blizflow-loader"></div>
            <div>
                <div style="font-weight: 700; color: #1e293b; font-family: 'Outfit', sans-serif;">Initializing Neural Engine...</div>
                <div style="font-size: 0.85rem; color: #64748b; margin-top: 2px;">Shattering AI patterns & reconstructing flow</div>
            </div>
        </div>
        <style>
        .blizflow-loader {
            width: 30px;
            height: 30px;
            border: 3px solid #e0e7ff;
            border-top: 3px solid #6366f1;
            border-radius: 50%;
            animation: blizflow-spin 0.8s cubic-bezier(0.55, 0.055, 0.675, 0.19) infinite;
        }
        @keyframes blizflow-spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        start_time = time.time()
        
        # Logic
        if mode == "🎯 Perplexity-Guided (Best)":
            try:
                neural_engine = load_neural_model()
                
                # Load perplexity analyzer (cached)
                if 'perplexity_analyzer' not in st.session_state:
                    with st.spinner("Loading perplexity analyzer (one-time setup)..."):
                        st.session_state.perplexity_analyzer = PerplexityAnalyzer()
                
                analyzer = st.session_state.perplexity_analyzer
                iterative_sys = IterativeHumanizer(neural_engine, analyzer)
                
                # Iterative humanization
                result = iterative_sys.iterative_humanize(text, target_perplexity=80, max_iterations=3, tone=tone, audience=audience, preserve_formatting=preserve_formatting, use_emojis=use_emojis)
                transformed_text = result["text"]
                
                # Show metrics
                st.success(f"""
                **Perplexity-Guided Results:**
                - Initial Perplexity: {result['initial_perplexity']:.2f}
                - Final Perplexity: {result['final_perplexity']:.2f}
                - Improvement: +{result['improvement']:.2f}
                - Quality: {result['quality']}
                - Human Score: {result['human_score']:.1%}
                - Iterations: {result['iterations']}
                """)
                
            except Exception as e:
                st.error(f"Perplexity mode error: {e}")
                transformed_text = text
                
        elif mode == "🧠 Smart Adaptive":
            try:
                neural_engine = load_neural_model()
                smart_system = SmartHumanizationOrchestrator(neural_engine)
                
                # Smart humanization with automatic optimization
                result = smart_system.smart_humanize(text, max_iterations=2, tone=tone, audience=audience, preserve_formatting=preserve_formatting, use_emojis=use_emojis)
                transformed_text = result["text"]
                
                # Show analysis
                st.info(f"""
                **Smart Analysis:**
                - Text Type: {result['initial_analysis']['type']}
                - AI Density Reduced: {result['improvement']:.2%}
                - Iterations: {result['iterations']}
                """)
                
                # Show manual editing tips
                tips = smart_system.get_manual_editing_tips(result['final_analysis'])
                if tips:
                    with st.expander("💡 Manual Editing Tips (Click to expand)"):
                        for tip in tips:
                            st.markdown(tip)
                
            except Exception as e:
                st.error(f"Smart mode error: {e}")
                transformed_text = text
                
        elif mode == "Deep AI (Neural)":
            try:
                neural_engine = load_neural_model()
                transformed_text = neural_engine.humanize(text, stealth_level=stealth_level, use_artifacts=use_artifacts, tone=tone, audience=audience, preserve_formatting=preserve_formatting, use_emojis=use_emojis)
            except Exception as e:
                st.error(f"Error: {e}")
                transformed_text = text
        else:
            humanizer = AcademicTextHumanizer(
                p_passive=0.3,
                p_synonym_replacement=0.3,
                p_academic_transition=0.0
            )
            transformed_text = humanizer.humanize_text(
                text,
                use_passive=True,
                use_synonyms=True
            )
        
        end_time = time.time()
        
        # Update Session State
        st.session_state.result = transformed_text
        st.success(f"Generated new variation in {end_time - start_time:.2f}s")
        BlizFlow.rerun()

if __name__ == "__main__":
    main()