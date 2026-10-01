import sys
from pathlib import Path

import streamlit as st

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# RAG IMPORTS
# ============================================================

from voice_assistant.agents.rag.rag_agent import RAGAgent
from voice_assistant.agents.rag.ingestion import RAGIngestion


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OmniSupport AI - RAG",
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
       SIDEBAR CONFIGURATION VALUES
       ======================================================== */

    .config-label {
        color: #aeb8c8;
        font-size: 14px;
        margin-top: 8px;
        margin-bottom: 6px;
    }

    .config-value {
        background-color: #0d1119;
        color: #e5e7eb;

        border: 1px solid #1f2937;
        border-radius: 10px;

        padding: 10px 12px;

        margin-bottom: 16px;

        font-size: 14px;

        font-family: Arial, sans-serif;

        line-height: 1.4;

        overflow-wrap: anywhere;
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
       PRIMARY BUTTON
       ======================================================== */

    .stButton > button[kind="primary"] {
        background-color: #1f2937;
        border-color: #4b5563;
        color: #ffffff;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #374151;
        border-color: #6366f1;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background-color: #0d1119;

        border: 1px solid #1f2937;

        border-radius: 14px;

        padding: 10px;
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
       DATAFRAME
       ======================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #1f2937;

        border-radius: 12px;

        overflow: hidden;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    div[data-testid="stExpander"] {
        background-color: #0d1119;

        border: 1px solid #1f2937;

        border-radius: 12px;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
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
       RAG INFO BOX
       ======================================================== */

    .rag-info {
        background-color: #0d1119;

        border: 1px solid #1f2937;

        border-radius: 14px;

        padding: 18px;

        margin-top: 10px;

        margin-bottom: 20px;
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


    /* ========================================================
       DIVIDERS
       ======================================================== */

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

    st.caption("Retrieval-Augmented Generation Agent")

    st.divider()

    st.subheader("RAG Configuration")

    st.markdown(
        '<div class="config-label">LLM</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="config-value">openai/gpt-oss-120b</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="config-label">Embedding Model</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="config-value">all-MiniLM-L6-v2</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="config-label">Vector Database</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="config-value">ChromaDB</div>',
        unsafe_allow_html=True,
    )


    st.divider()

    st.subheader("Supported Documents")

    st.write("PDF")

    st.write("TXT")

    st.write("DOCX")


    st.divider()

    st.subheader("Pipeline")

    st.write("Document Loader")

    st.write("Text Chunking")

    st.write("Embeddings")

    st.write("ChromaDB")

    st.write("Similarity Search")

    st.write("LLM Response")


    st.divider()

    st.caption("SYSTEM STATUS")

    st.markdown(
        '<div class="sidebar-status">Online</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# INITIALIZE RAG COMPONENTS
# ============================================================

@st.cache_resource
def get_rag_agent():

    return RAGAgent()


@st.cache_resource
def get_rag_ingestion():

    return RAGIngestion()


try:

    rag_agent = get_rag_agent()

except Exception as e:

    st.error(
        f"Could not initialize the RAG Agent: {e}"
    )

    st.stop()


try:

    rag_ingestion = get_rag_ingestion()

except Exception as e:

    st.error(
        f"Could not initialize RAG ingestion: {e}"
    )

    st.stop()


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "RAG Agent"
)

st.caption(
    "Ask questions about your uploaded documents using "
    "retrieval-augmented generation."
)


# ============================================================
# RAG OVERVIEW
# ============================================================

st.markdown(
    """
    <div class="rag-info">
        <strong>Retrieval-Augmented Generation</strong><br>
        Upload documents, create embeddings, store them in
        ChromaDB, retrieve relevant content, and generate
        answers using the RAG language model.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DOCUMENT UPLOAD
# ============================================================

st.subheader(
    "Document Upload"
)

uploaded_file = st.file_uploader(
    "Upload a document",
    type=[
        "pdf",
        "txt",
        "docx",
    ],
)


if uploaded_file is not None:

    upload_dir = (
        PROJECT_ROOT
        / "data"
        / "documents"
    )

    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        upload_dir
        / uploaded_file.name
    )


    with open(
        file_path,
        "wb",
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )


    st.success(
        f"Document uploaded: {uploaded_file.name}"
    )


    # ========================================================
    # INGEST DOCUMENT
    # ========================================================

    ingest_button = st.button(
        "Ingest Document",
        type="primary",
        use_container_width=True,
    )


    if ingest_button:

        with st.spinner(
            "Processing document and creating embeddings..."
        ):

            try:

                result = rag_ingestion.ingest(
                    str(file_path)
                )

                st.session_state[
                    "rag_ingestion_result"
                ] = result

            except Exception as e:

                st.session_state[
                    "rag_ingestion_result"
                ] = {
                    "success": False,
                    "error": str(e),
                }


# ============================================================
# INGESTION RESULT
# ============================================================

if "rag_ingestion_result" in st.session_state:

    ingestion_result = (
        st.session_state[
            "rag_ingestion_result"
        ]
    )


    if ingestion_result.get(
        "success",
        False,
    ):

        st.success(
            "Document successfully ingested into the vector database."
        )


        # ----------------------------------------------------
        # INGESTION METRICS
        # ----------------------------------------------------

        st.subheader(
            "Ingestion Summary"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Characters",
                ingestion_result.get(
                    "characters",
                    ingestion_result.get(
                        "total_characters",
                        0,
                    ),
                ),
            )


        with col2:

            st.metric(
                "Chunks",
                ingestion_result.get(
                    "chunks",
                    ingestion_result.get(
                        "total_chunks",
                        0,
                    ),
                ),
            )


        with col3:

            st.metric(
                "Embeddings",
                ingestion_result.get(
                    "embeddings",
                    ingestion_result.get(
                        "total_embeddings",
                        0,
                    ),
                ),
            )


    elif ingestion_result.get(
        "error"
    ):

        st.error(
            f"Document ingestion failed: "
            f"{ingestion_result['error']}"
        )


st.divider()


# ============================================================
# ASK RAG
# ============================================================

st.subheader(
    "Ask Your Documents"
)

st.write(
    "Ask a question about the information contained "
    "in your uploaded documents."
)


question = st.text_area(
    "Question",
    placeholder=(
        "Examples:\n"
        "What are the main findings of the document?\n"
        "What does the document say about artificial intelligence?\n"
        "Summarize the key points.\n"
        "What are the business impacts discussed in the document?"
    ),
    height=140,
)


ask_button = st.button(
    "Ask RAG Agent",
    type="primary",
    use_container_width=True,
)


# ============================================================
# PROCESS RAG QUESTION
# ============================================================

if ask_button:

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            try:

                result = rag_agent.answer(
                    question.strip()
                )

                st.session_state[
                    "rag_result"
                ] = result

            except Exception as e:

                st.session_state[
                    "rag_result"
                ] = {
                    "answer": "",
                    "sources": [],
                    "error": str(e),
                }


# ============================================================
# DISPLAY RAG RESULT
# ============================================================

if "rag_result" in st.session_state:

    result = st.session_state[
        "rag_result"
    ]


    st.divider()

    st.subheader(
        "Answer"
    )


    # --------------------------------------------------------
    # ERROR
    # --------------------------------------------------------

    if result.get("error"):

        st.error(
            result["error"]
        )


    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    answer = result.get(
        "answer",
        "",
    )


    if answer:

        st.markdown(
            answer
        )


    # --------------------------------------------------------
    # SOURCES
    # --------------------------------------------------------

    sources = result.get(
        "sources",
        [],
    )


    if sources:

        st.subheader(
            "Retrieved Sources"
        )


        with st.expander(
            "View Retrieved Sources",
            expanded=True,
        ):

            for index, source in enumerate(
                sources,
                start=1,
            ):

                if isinstance(
                    source,
                    dict,
                ):

                    title = source.get(
                        "title",
                        f"Source {index}",
                    )

                    st.markdown(
                        f"**{title}**"
                    )


                    if source.get(
                        "url"
                    ):

                        st.markdown(
                            source["url"]
                        )


                    if source.get(
                        "content"
                    ):

                        st.write(
                            source["content"]
                        )

                else:

                    st.write(
                        source
                    )


# ============================================================
# RAG AGENT INFORMATION
# ============================================================

st.divider()

st.subheader(
    "Agent Information"
)

info_col1, info_col2 = st.columns(2)


with info_col1:

    st.markdown(
        """
**Agent:** RAG Agent

**LLM:** `openai/gpt-oss-120b`

**Embedding Model:** `all-MiniLM-L6-v2`

**Vector Database:** ChromaDB
"""
    )


with info_col2:

    st.markdown(
        """
**Capabilities:**

- PDF document ingestion
- Text document ingestion
- Document chunking
- Semantic embeddings
- Vector similarity search
- Context retrieval
- Document question answering
- Source retrieval
- Natural-language interaction
"""
    )


# ============================================================
# RAG PIPELINE
# ============================================================

st.divider()

st.subheader(
    "RAG Pipeline"
)

pipeline_col1, pipeline_col2, pipeline_col3, pipeline_col4 = (
    st.columns(4)
)


with pipeline_col1:

    st.metric(
        "Step 1",
        "Document",
    )

    st.caption(
        "Load PDF, TXT, or DOCX"
    )


with pipeline_col2:

    st.metric(
        "Step 2",
        "Embeddings",
    )

    st.caption(
        "Convert chunks into vectors"
    )


with pipeline_col3:

    st.metric(
        "Step 3",
        "Retrieval",
    )

    st.caption(
        "Find relevant document context"
    )


with pipeline_col4:

    st.metric(
        "Step 4",
        "Generation",
    )

    st.caption(
        "Generate grounded response"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        OmniSupport AI · RAG Agent
        <br>
        ChromaDB · Sentence Transformers · Groq · Retrieval-Augmented Generation
    </div>
    """,
    unsafe_allow_html=True,
)