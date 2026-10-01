import streamlit as st

import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OmniSupport AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       REMOVE STREAMLIT TOP HEADER
    ======================================================== */

    header[data-testid="stHeader"] {
        display: none;
    }

    div[data-testid="stToolbar"] {
        display: none;
    }

    div[data-testid="stDecoration"] {
        display: none;
    }


    /* ========================================================
       GLOBAL APPLICATION
    ======================================================== */

    .stApp {
        background-color: #080b12;
        color: #f8fafc;
    }

    .stAppViewContainer {
        background-color: #080b12;
    }

    .main {
        background-color: #080b12;
        padding-top: 0 !important;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem;
    }


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: #0b0f18;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #0b0f18;
    }


    /* ========================================================
       HEADINGS
    ======================================================== */

    h1,
    h2,
    h3 {
        color: #f8fafc !important;
    }

    p {
        color: #aeb8c8;
    }


    /* ========================================================
       HERO LABEL
    ======================================================== */

    .hero-label {
        color: #818cf8;

        font-size: 12px;

        font-weight: 700;

        letter-spacing: 2px;

        text-transform: uppercase;

        margin-bottom: 8px;
    }


    /* ========================================================
       HERO DESCRIPTION
    ======================================================== */

    .hero-description {
        color: #94a3b8;

        font-size: 17px;

        line-height: 1.7;

        max-width: 850px;

        margin-top: 12px;

        margin-bottom: 0;
    }


    /* ========================================================
       METRIC CARDS
    ======================================================== */

    div[data-testid="metric-container"] {
        background-color: #101621;

        border: 1px solid #1f2937;

        border-radius: 16px;

        padding: 20px;

        min-height: 120px;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.20);
    }

    div[data-testid="metric-container"] label {
        color: #7f8ba3 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }

    div[data-testid="stMetricDelta"] {
        color: #4ade80 !important;
    }


    /* ========================================================
       AGENT DESCRIPTION
    ======================================================== */

    .agent-description {
        color: #8995a8;

        font-size: 14px;

        line-height: 1.65;

        min-height: 68px;

        margin-bottom: 10px;
    }


    /* ========================================================
       AGENT BUTTONS
    ======================================================== */

    .stButton > button {
        width: 100%;

        background-color: #111827;

        color: #e5e7eb;

        border: 1px solid #374151;

        border-radius: 10px;

        padding: 0.65rem 1rem;

        font-weight: 600;

        transition:
            background-color 0.2s ease,
            border-color 0.2s ease,
            color 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #1e293b;

        border-color: #6366f1;

        color: #ffffff;
    }


    /* ========================================================
       DIVIDERS
    ======================================================== */

    hr {
        border-color: #1f2937;
    }


    /* ========================================================
       SUCCESS MESSAGE
    ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ========================================================
       FOOTER
    ======================================================== */

    .footer {
        text-align: center;

        color: #64748b;

        font-size: 12px;

        padding-top: 30px;

        margin-top: 40px;

        border-top: 1px solid #1f2937;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("OmniSupport AI")

    st.caption("Multi-Agent AI Platform")

    st.divider()

    st.subheader("Platform")

    st.caption(
        "Use the navigation menu to access the specialized "
        "AI agents."
    )

    st.divider()

    st.caption("SYSTEM STATUS")

    st.success("Online")


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    '<div class="hero-label">MULTI-AGENT AI PLATFORM</div>',
    unsafe_allow_html=True,
)

st.title("OmniSupport AI")

st.markdown(
    """
    <div class="hero-description">
        An intelligent AI platform that combines voice interaction,
        document retrieval, web research, data analysis, and
        database querying through specialized AI agents.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()


# ============================================================
# PLATFORM OVERVIEW
# ============================================================

st.header("Platform Overview")

st.caption(
    "Core technologies powering the OmniSupport AI system."
)

st.write("")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)


with metric_col1:

    st.metric(
        label="AI Agents",
        value="5",
        delta="Specialized agents",
    )


with metric_col2:

    st.metric(
        label="Vector Database",
        value="ChromaDB",
        delta="Semantic retrieval",
    )


with metric_col3:

    st.metric(
        label="LLM Provider",
        value="Groq",
        delta="Fast inference",
    )


with metric_col4:

    st.metric(
        label="Voice STT",
        value="Whisper",
        delta="Speech recognition",
    )


# ============================================================
# AI AGENTS
# ============================================================

st.header("AI Agents")

st.caption(
    "Select an agent to open its dedicated workspace."
)

st.write("")


# ============================================================
# ROW 1
# ============================================================

agent_col1, agent_col2, agent_col3 = st.columns(3)


# ------------------------------------------------------------
# VOICE ASSISTANT
# ------------------------------------------------------------

with agent_col1:

    st.subheader("Voice Assistant")

    st.markdown(
        """
        <div class="agent-description">
            Interact with OmniSupport AI using continuous voice
            conversations powered by speech recognition, LLM
            reasoning, and text-to-speech.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "Open Voice Assistant",
        key="open_voice",
    ):

        st.switch_page(
            "pages/5_Voice_Assistant.py"
        )


# ------------------------------------------------------------
# RAG AGENT
# ------------------------------------------------------------

with agent_col2:

    st.subheader("RAG Agent")

    st.markdown(
        """
        <div class="agent-description">
            Upload documents and ask questions using semantic
            search and retrieval-augmented generation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "Open RAG",
        key="open_rag",
    ):

        st.switch_page(
            "pages/2_RAG.py"
        )


# ------------------------------------------------------------
# RESEARCH AGENT
# ------------------------------------------------------------

with agent_col3:

    st.subheader("Research Agent")

    st.markdown(
        """
        <div class="agent-description">
            Search the web and synthesize information from
            multiple online sources.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "Open Research",
        key="open_research",
    ):

        st.switch_page(
            "pages/3_Research.py"
        )


# ============================================================
# ROW 2
# ============================================================

st.write("")

agent_col1, agent_col2, agent_col3 = st.columns(3)


# ------------------------------------------------------------
# DATA ANALYSIS AGENT
# ------------------------------------------------------------

with agent_col1:

    st.subheader("Data Analysis Agent")

    st.markdown(
        """
        <div class="agent-description">
            Upload CSV or Excel datasets, analyze the data,
            generate insights, and create visualizations.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "Open Data Analysis",
        key="open_data",
    ):

        st.switch_page(
            "pages/4_Data_Analysis.py"
        )


# ------------------------------------------------------------
# DATABASE AGENT
# ------------------------------------------------------------

with agent_col2:

    st.subheader("Database Agent")

    st.markdown(
        """
        <div class="agent-description">
            Ask questions in natural language and let the
            agent generate and execute SQL queries against
            PostgreSQL.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "Open Database",
        key="open_database",
    ):

        st.switch_page(
            "pages/7_Database.py"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        OmniSupport AI · Multi-Agent AI Platform
        <br>
        Voice · RAG · Research · Data Analysis · Database
    </div>
    """,
    unsafe_allow_html=True,
)