import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OmniSupport AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    /* Remove Streamlit top header */
    header[data-testid="stHeader"] {
        display: none;
    }

    div[data-testid="stToolbar"] {
        display: none;
    }

    div[data-testid="stDecoration"] {
        display: none;
    }

    /* Main application */
    .stApp {
        background-color: #05070b;
        color: #f8fafc;
    }

    .stAppViewContainer {
        background-color: #05070b;
    }

    .main {
        background-color: #05070b;
        padding-top: 0 !important;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #090c12;
        border-right: 1px solid #1f2937;
    }

    /* Headings */
    h1,
    h2,
    h3 {
        color: #f8fafc !important;
    }

    p {
        color: #aeb8c8;
    }

    /* Agent information boxes */
    div[data-testid="stAlert"] {
        background-color: #0d1119;
        border: 1px solid #1f2937;
        border-radius: 14px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        background-color: #111827;
        color: #e5e7eb;
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 0.65rem 1rem;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #1e293b;
        border-color: #6366f1;
        color: #ffffff;
    }

    /* Dividers */
    hr {
        border-color: #1f2937;
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
# HOME
# ============================================================

st.title("OmniSupport AI")

st.subheader("Welcome to OmniSupport AI")

st.write(
    """
    OmniSupport AI is a multi-agent platform where a central
    voice assistant can route questions to specialized AI agents.
    """
)


st.divider()


# ============================================================
# RAG AGENT
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.info(
        """
        ### RAG Agent

        Ask questions about your uploaded documents.

        **Technology**

        - PDF / TXT / DOCX
        - Document chunking
        - Sentence Transformers
        - ChromaDB
        - Groq GPT OSS 120B
        """
    )

    if st.button(
        "Open RAG Agent",
        key="home_rag",
    ):
        st.switch_page(
            "pages/2_RAG.py"
        )


# ============================================================
# RESEARCH AGENT
# ============================================================

with col2:

    st.info(
        """
        ### Research Agent

        Research current information using web tools
        and return relevant sources.

        **Capabilities**

        - Web search
        - Source collection
        - Information synthesis
        - Source-based answers
        """
    )

    if st.button(
        "Open Research Agent",
        key="home_research",
    ):
        st.switch_page(
            "pages/3_Research.py"
        )


# ============================================================
# DATA ANALYSIS AGENT
# ============================================================

col3, col4 = st.columns(2)

with col3:

    st.info(
        """
        ### Data Analysis Agent

        Upload datasets and ask questions using natural language.

        **Capabilities**

        - CSV / Excel
        - Python / Pandas
        - Statistical analysis
        - Data visualization
        - AI-generated insights
        """
    )

    if st.button(
        "Open Data Analysis",
        key="home_data",
    ):
        st.switch_page(
            "pages/4_Data_Analysis.py"
        )


# ============================================================
# VOICE ASSISTANT
# ============================================================

with col4:

    st.info(
        """
        ### Voice Assistant

        Speak naturally with OmniSupport AI.

        **Pipeline**

        Speech → Whisper → Router → Agent → Answer → TTS
        """
    )

    if st.button(
        "Open Voice Assistant",
        key="home_voice",
    ):
        st.switch_page(
            "pages/5_Voice_Assistant.py"
        )


# ============================================================
# DATABASE AGENT
# ============================================================

st.divider()

st.subheader("Database Agent")

st.write(
    """
    Query the PostgreSQL database using natural-language questions.
    The Database Agent inspects the schema, generates SQL, executes
    the query, and returns the result.
    """
)

if st.button(
    "Open Database Agent",
    key="home_database",
):
    st.switch_page(
        "pages/7_Database.py"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "OmniSupport AI · Multi-Agent AI Platform · "
    "RAG · Research · Data Analysis · Voice · Database"
)