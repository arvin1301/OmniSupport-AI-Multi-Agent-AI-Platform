import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# OMNISUPPORT IMPORTS
# ============================================================

from voice_assistant.orchestrator import AgentOrchestrator


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OmniSupport AI - Data Analysis",
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

    div[data-testid="stMetricDelta"] {
        color: #4ade80 !important;
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

    st.caption("Data Analysis Agent")

    st.divider()

    st.subheader("Analysis Configuration")

    st.write("Analysis Engine")

    st.code("Pandas")

    st.write("Execution")

    st.code("Controlled Python Executor")

    st.write("Dataset Formats")

    st.code("CSV / XLSX / XLS")

    st.divider()

    st.info(
        "Upload a dataset and ask questions using natural "
        "language. The Data Analysis Agent generates "
        "analysis, results, and visualizations."
    )

    st.divider()

    st.caption("SYSTEM STATUS")

    st.markdown(
        '<div class="sidebar-status">Online</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.title("Data Analysis Agent")

st.caption(
    "Analyze CSV and Excel datasets using the "
    "OmniSupport multi-agent system."
)


# ============================================================
# ORCHESTRATOR
# ============================================================

@st.cache_resource
def get_orchestrator():
    return AgentOrchestrator()


orchestrator = get_orchestrator()


# ============================================================
# DATASET UPLOAD
# ============================================================

st.header("Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=[
        "csv",
        "xlsx",
        "xls",
    ],
)


if uploaded_file is not None:

    # --------------------------------------------------------
    # SAVE UPLOADED FILE
    # --------------------------------------------------------

    upload_dir = (
        PROJECT_ROOT
        / "data"
        / "uploads"
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
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )


    # --------------------------------------------------------
    # LOAD DATASET
    # --------------------------------------------------------

    try:

        orchestrator.load_data(
            str(file_path)
        )

        dataset_info = (
            orchestrator.get_dataset_info()
        )

        agent = orchestrator.data_agent

        df = agent.df


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        st.success(
            f"Dataset loaded successfully: "
            f"{uploaded_file.name}"
        )

        st.info(
            "Dataset is now registered as the active "
            "OmniSupport dataset. The Voice Assistant "
            "can use this dataset."
        )


        # ====================================================
        # DATASET OVERVIEW
        # ====================================================

        st.header("Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Rows",
                dataset_info["rows"],
            )


        with col2:

            st.metric(
                "Columns",
                dataset_info["columns"],
            )


        with col3:

            missing_count = int(
                df.isna().sum().sum()
            )

            st.metric(
                "Missing Values",
                missing_count,
            )


        with col4:

            duplicate_count = int(
                df.duplicated().sum()
            )

            st.metric(
                "Duplicate Rows",
                duplicate_count,
            )


        # ====================================================
        # ACTIVE DATASET
        # ====================================================

        st.header("Active Dataset")

        st.info(
            f"Currently loaded: "
            f"{Path(dataset_info['file_path']).name}"
        )


        # ====================================================
        # DATA PREVIEW
        # ====================================================

        st.header("Data Preview")

        st.dataframe(
            df.head(100),
            use_container_width=True,
        )


        # ====================================================
        # COLUMN INFORMATION
        # ====================================================

        with st.expander("Column Information"):

            column_info = []

            for column in df.columns:

                column_info.append(
                    {
                        "Column": column,
                        "Data Type": str(
                            df[column].dtype
                        ),
                        "Unique Values": int(
                            df[column].nunique()
                        ),
                        "Missing Values": int(
                            df[column].isna().sum()
                        ),
                    }
                )


            column_info_df = pd.DataFrame(
                column_info
            )


            st.dataframe(
                column_info_df,
                use_container_width=True,
                hide_index=True,
            )


        # ====================================================
        # MISSING VALUES
        # ====================================================

        missing_values = (
            df.isna()
            .sum()
            .reset_index()
        )

        missing_values.columns = [
            "Column",
            "Missing Values",
        ]

        missing_values = missing_values[
            missing_values["Missing Values"] > 0
        ]


        if not missing_values.empty:

            with st.expander("Missing Values"):

                st.dataframe(
                    missing_values,
                    use_container_width=True,
                    hide_index=True,
                )


        # ====================================================
        # ASK YOUR DATASET
        # ====================================================

        st.header("Ask Your Dataset")

        question = st.text_area(
            "Ask a question about your dataset",
            placeholder=(
                "Examples:\n"
                "Which product generated the highest sales?\n"
                "Show sales by product.\n"
                "Compare sales across regions.\n"
                "What is the average sales value?\n"
                "What is the correlation between sales and quantity?\n"
                "Show a chart of sales by product."
            ),
            height=140,
        )


        # ====================================================
        # ANALYZE BUTTON
        # ====================================================

        analyze_button = st.button(
            "Analyze Dataset",
            type="primary",
            use_container_width=True,
        )


        if analyze_button:

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                # --------------------------------------------
                # PROCESS THROUGH ORCHESTRATOR
                # --------------------------------------------

                with st.spinner(
                    "Analyzing dataset..."
                ):

                    try:

                        result = orchestrator.process(
                            question
                        )

                    except Exception as e:

                        st.error(
                            f"Data Analysis Error:\n\n{e}"
                        )

                        result = None


                if result:

                    # ----------------------------------------
                    # AGENT INFORMATION
                    # ----------------------------------------

                    st.caption(
                        f"Handled by: "
                        f"{result['agent']} agent"
                    )


                    # ----------------------------------------
                    # ANALYSIS ANSWER
                    # ----------------------------------------

                    st.subheader("Analysis")

                    st.markdown(
                        result["answer"]
                    )


                    # ----------------------------------------
                    # CALCULATED RESULTS
                    # ----------------------------------------

                    if result.get("results"):

                        st.subheader(
                            "Calculated Results"
                        )

                        calculated_results = (
                            result["results"]
                        )


                        # DataFrame result
                        if isinstance(
                            calculated_results,
                            pd.DataFrame,
                        ):

                            st.dataframe(
                                calculated_results,
                                use_container_width=True,
                            )


                        # Dictionary result
                        elif isinstance(
                            calculated_results,
                            dict,
                        ):

                            try:

                                result_df = pd.DataFrame(
                                    [calculated_results]
                                )

                                st.dataframe(
                                    result_df,
                                    use_container_width=True,
                                    hide_index=True,
                                )

                            except Exception:

                                st.json(
                                    calculated_results
                                )


                        # Other result types
                        else:

                            st.write(
                                calculated_results
                            )


                    # ----------------------------------------
                    # CHARTS
                    # ----------------------------------------

                    charts = result.get(
                        "charts",
                        [],
                    )


                    if charts:

                        st.subheader(
                            "Visualization"
                        )


                        for chart_path in charts:

                            chart_file = Path(
                                chart_path
                            )


                            if chart_file.exists():

                                st.image(
                                    str(chart_file),
                                    use_container_width=True,
                                )

                            else:

                                st.warning(
                                    f"Chart file not found: "
                                    f"{chart_path}"
                                )


    except Exception as e:

        st.error(
            f"Unable to load dataset: {e}"
        )


# ============================================================
# NO DATASET
# ============================================================

else:

    st.info(
        "Upload a CSV or Excel file to begin."
    )


# ============================================================
# AGENT INFORMATION
# ============================================================

st.divider()

st.header("Agent Information")

info_col1, info_col2 = st.columns(2)


# ------------------------------------------------------------
# AGENT DETAILS
# ------------------------------------------------------------

with info_col1:

    st.markdown(
        f"""
**Agent:** Data Analysis Agent

**LLM:** `{orchestrator.data_agent.model}`

**Analysis Engine:** Pandas

**Execution:** Controlled Python Executor

**Orchestrator:** Agent Router + Data Agent
"""
    )


# ------------------------------------------------------------
# CAPABILITIES
# ------------------------------------------------------------

with info_col2:

    st.markdown(
        """
**Supported Files:**

- CSV
- XLSX
- XLS

**Capabilities:**

- Statistical analysis
- Grouping and aggregation
- Data comparisons
- Missing-value analysis
- Correlation analysis
- Visualization
- Natural-language data questions
- Dataset-aware agent routing
- Voice Assistant dataset access
"""
    )


# ============================================================
# ORCHESTRATOR DATASET STATE
# ============================================================

st.divider()

st.header("Orchestrator Dataset State")

current_dataset = (
    orchestrator.get_dataset_info()
)


if current_dataset["loaded"]:

    st.success(
        "A dataset is currently active "
        "in the Orchestrator."
    )

    st.write(
        f"**File:** "
        f"{Path(current_dataset['file_path']).name}"
    )

    st.write(
        f"**Rows:** "
        f"{current_dataset['rows']}"
    )

    st.write(
        f"**Columns:** "
        f"{current_dataset['columns']}"
    )

    st.caption(
        "Shared dataset state is available to "
        "other OmniSupport processes, including "
        "the Voice Assistant."
    )


else:

    st.info(
        "No dataset is currently active."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        OmniSupport AI · Data Analysis Agent
        <br>
        Pandas · Python · CSV · Excel · Visualization
    </div>
    """,
    unsafe_allow_html=True,
)