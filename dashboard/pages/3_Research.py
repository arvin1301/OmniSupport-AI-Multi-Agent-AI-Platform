import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# RESEARCH IMPORT
# ============================================================

from voice_assistant.agents.research import ResearchAgent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OmniSupport AI - Research",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DARK BLACK THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       REMOVE STREAMLIT HEADER
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
       GLOBAL BACKGROUND
    ======================================================== */

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


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: #090c12;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #090c12;
    }


    /* ========================================================
       HEADINGS
    ======================================================== */

    h1,
    h2,
    h3,
    h4 {
        color: #f8fafc !important;
    }

    p {
        color: #aeb8c8;
    }


    /* ========================================================
       TEXT AREA
    ======================================================== */

    textarea {
        background-color: #0d1119 !important;
        color: #f8fafc !important;
        border: 1px solid #374151 !important;
        border-radius: 10px !important;
    }


    /* ========================================================
       INPUTS
    ======================================================== */

    input {
        background-color: #0d1119 !important;
        color: #f8fafc !important;
    }


    /* ========================================================
       BUTTONS
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
       METRICS
    ======================================================== */

    div[data-testid="metric-container"] {
        background-color: #0d1119;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 18px;
        min-height: 105px;
    }

    div[data-testid="metric-container"] label {
        color: #7f8ba3 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }


    /* ========================================================
       SOURCE LINKS
    ======================================================== */

    a {
        color: #818cf8 !important;
    }

    a:hover {
        color: #a5b4fc !important;
    }


    /* ========================================================
       ALERTS
    ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ========================================================
       DIVIDERS
    ======================================================== */

    hr {
        border-color: #1f2937;
    }


    /* ========================================================
       SIDEBAR STATUS
    ======================================================== */

    .sidebar-status {
        color: #4ade80;
        font-size: 14px;
        font-weight: 600;
    }


    /* ========================================================
       FOOTER
    ======================================================== */

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        padding-top: 25px;
        margin-top: 35px;
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

    st.caption("Research Agent")

    st.divider()

    st.subheader("Research Configuration")

    st.write("Search")

    st.markdown(
        """
        <div style="
            background-color:#0d1119;
            border:1px solid #1f2937;
            border-radius:8px;
            padding:10px;
            color:#e5e7eb;
            font-size:14px;
        ">
        Google News RSS
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("LLM")

    st.markdown(
        """
        <div style="
            background-color:#0d1119;
            border:1px solid #1f2937;
            border-radius:8px;
            padding:10px;
            color:#e5e7eb;
            font-size:14px;
        ">
        Qwen 3.8 27B
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("Sources")

    st.markdown(
        """
        <div style="
            background-color:#0d1119;
            border:1px solid #1f2937;
            border-radius:8px;
            padding:10px;
            color:#e5e7eb;
            font-size:14px;
        ">
        Up to 5
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.info(
        "The Research Agent searches current web information, "
        "collects relevant sources, and generates a synthesized answer."
    )

    st.divider()

    st.caption("SYSTEM STATUS")

    st.markdown(
        '<div class="sidebar-status">Online</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# HEADER
# ============================================================

st.title("Research Agent")

st.markdown(
    """
    Research current information from the web using structured
    web search, multiple sources, source references, and an
    LLM-powered synthesis process.
    """
)


# ============================================================
# INITIALIZE AGENT
# ============================================================

@st.cache_resource
def get_research_agent():

    return ResearchAgent()


try:

    agent = get_research_agent()

except Exception as e:

    st.error(
        "Research Agent could not be initialized."
    )

    st.code(
        str(e)
    )

    st.stop()


# ============================================================
# RESEARCH QUESTION
# ============================================================

st.header("Research Question")

question = st.text_area(
    "What would you like me to research?",
    placeholder=(
        "Example: What are the latest developments in generative AI?"
    ),
    height=120,
)


# ============================================================
# RESEARCH BUTTON
# ============================================================

if st.button(
    "Research",
    type="primary",
    use_container_width=True,
):

    if not question.strip():

        st.warning(
            "Please enter a research question."
        )

    else:

        with st.spinner(
            "Researching the web..."
        ):

            try:

                result = agent.research(
                    question.strip()
                )

            except Exception as e:

                st.error(
                    f"Research Agent Error:\n\n{e}"
                )

                result = None


        if result:

            # =================================================
            # ANSWER
            # =================================================

            st.divider()

            st.subheader("Research Answer")

            answer = result.get(
                "answer",
                "No answer returned.",
            )

            st.markdown(answer)


            # =================================================
            # SOURCES
            # =================================================

            sources = result.get(
                "sources",
                [],
            )

            st.divider()

            st.subheader(
                f"Sources ({len(sources)})"
            )

            if sources:

                for index, source in enumerate(
                    sources,
                    start=1,
                ):

                    title = source.get(
                        "title",
                        "Untitled source",
                    )

                    url = source.get(
                        "url",
                        "",
                    )

                    domain = source.get(
                        "domain",
                        "",
                    )

                    snippet = source.get(
                        "snippet",
                        "",
                    )

                    st.markdown(
                        f"**{index}. {title}**"
                    )

                    if domain:

                        st.caption(
                            f"Source: {domain}"
                        )

                    if snippet:

                        st.write(
                            snippet
                        )

                    if url:

                        st.markdown(
                            f"[Open source]({url})"
                        )

                    st.write("")

            else:

                st.info(
                    "No sources were returned."
                )


# ============================================================
# AGENT INFORMATION
# ============================================================

st.divider()

st.subheader("Agent Information")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Agent",
        "Research Agent",
    )

with col2:

    st.metric(
        "LLM",
        "Qwen 3.8 27B",
    )

with col3:

    st.metric(
        "Maximum Sources",
        "5",
    )


# ============================================================
# RESEARCH PIPELINE
# ============================================================

st.divider()

st.subheader("Research Pipeline")

st.markdown(
    """
    **Research Question**

    ↓

    **Web Search**

    ↓

    **Source Collection**

    ↓

    **Source Cleaning**

    ↓

    **Research Context**

    ↓

    **Qwen LLM Synthesis**

    ↓

    **Answer + Source References**
    """
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        OmniSupport AI · Research Agent
        <br>
        Web Search · Source References · LLM Synthesis
    </div>
    """,
    unsafe_allow_html=True,
)