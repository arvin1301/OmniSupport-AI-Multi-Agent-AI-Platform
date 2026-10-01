import streamlit as st
import pandas as pd

from voice_assistant.agents.database.database_agent import DatabaseAgent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OmniSupport AI - Database",
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
       CODE BLOCK
       ======================================================== */

    pre {
        background-color: #0a0e15 !important;

        border: 1px solid #1f2937 !important;

        border-radius: 10px !important;
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
       DATABASE STATUS
       ======================================================== */

    .database-status {
        background-color: #0d1119;

        border: 1px solid #1f2937;

        border-radius: 12px;

        padding: 16px;

        margin-bottom: 15px;
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

    st.caption("PostgreSQL Database Agent")

    st.divider()

    st.subheader("Database Engine")

    st.write("Database")
    st.code("PostgreSQL")

    st.write("Query Language")
    st.code("SQL")

    st.write("Access Mode")
    st.code("Read Only")

    st.divider()

    st.subheader("Capabilities")

    st.write("Natural-language SQL")

    st.write("Schema inspection")

    st.write("Read-only queries")

    st.write("Data retrieval")

    st.write("Result explanation")

    st.write("Table analysis")

    st.divider()

    st.caption("SYSTEM STATUS")

    st.markdown(
        '<div class="sidebar-status">Online</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# INITIALIZE DATABASE AGENT
# ============================================================

@st.cache_resource
def get_database_agent():

    return DatabaseAgent()


try:

    database_agent = get_database_agent()

except Exception as e:

    st.error(
        f"Could not initialize the Database Agent: {e}"
    )

    st.stop()


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "PostgreSQL Database"
)

st.caption(
    "Query your PostgreSQL database using natural language."
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

st.subheader(
    "Database Status"
)

try:

    connected = database_agent.test_connection()

    if connected:

        st.success(
            "PostgreSQL database connected successfully."
        )

    else:

        st.error(
            "PostgreSQL database connection failed."
        )

except Exception as e:

    st.error(
        f"Database connection error: {e}"
    )


st.divider()


# ============================================================
# DATABASE INFORMATION
# ============================================================

st.subheader(
    "Database Information"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Database",
        database_agent.connection.database,
    )


with col2:

    st.metric(
        "Host",
        database_agent.connection.host,
    )


with col3:

    st.metric(
        "Port",
        database_agent.connection.port,
    )


with col4:

    st.metric(
        "User",
        database_agent.connection.username,
    )


st.divider()


# ============================================================
# DATABASE SCHEMA
# ============================================================

st.subheader(
    "Database Schema"
)

try:

    schema = database_agent.get_schema()

    if not schema:

        st.info(
            "No database tables were found."
        )

    else:

        st.write(
            f"Tables: {len(schema)}"
        )

        for table_name, columns in schema.items():

            with st.expander(
                table_name,
                expanded=True,
            ):

                schema_rows = []

                for column in columns:

                    schema_rows.append(
                        {
                            "Column": column["name"],
                            "Type": column["type"],
                            "Nullable": (
                                "Yes"
                                if column["nullable"]
                                else "No"
                            ),
                        }
                    )

                schema_df = pd.DataFrame(
                    schema_rows
                )

                st.dataframe(
                    schema_df,
                    use_container_width=True,
                    hide_index=True,
                )

except Exception as e:

    st.error(
        f"Could not load database schema: {e}"
    )


st.divider()


# ============================================================
# NATURAL LANGUAGE DATABASE QUERY
# ============================================================

st.subheader(
    "Ask the Database"
)

st.write(
    "Ask a question in natural language. "
    "OmniSupport AI will generate a read-only SQL query, "
    "execute it against PostgreSQL, and explain the result."
)


question = st.text_area(
    "Database question",
    placeholder=(
        "Example: Which product line has the highest "
        "total sales?"
    ),
    height=120,
)


run_query = st.button(
    "Query Database",
    type="primary",
    use_container_width=True,
)


# ============================================================
# EXECUTE DATABASE QUERY
# ============================================================

if run_query:

    if not question.strip():

        st.warning(
            "Please enter a database question."
        )

    else:

        with st.spinner(
            "Querying PostgreSQL..."
        ):

            try:

                result = database_agent.query(
                    question.strip()
                )

                st.session_state[
                    "database_result"
                ] = result

            except Exception as e:

                st.session_state[
                    "database_result"
                ] = {
                    "answer": "",
                    "sql": None,
                    "results": None,
                    "error": str(e),
                }


# ============================================================
# DISPLAY QUERY RESULT
# ============================================================

if "database_result" in st.session_state:

    result = st.session_state[
        "database_result"
    ]

    st.divider()

    st.subheader(
        "Query Result"
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

        st.success(
            answer
        )


    # --------------------------------------------------------
    # GENERATED SQL
    # --------------------------------------------------------

    sql = result.get(
        "sql"
    )

    if sql:

        with st.expander(
            "Generated SQL",
            expanded=True,
        ):

            st.code(
                sql,
                language="sql",
            )


    # --------------------------------------------------------
    # DATAFRAME RESULT
    # --------------------------------------------------------

    data = result.get(
        "results"
    )

    if isinstance(
        data,
        pd.DataFrame,
    ):

        st.subheader(
            "Returned Data"
        )

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True,
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Rows Returned",
                len(data),
            )


        with col2:

            st.metric(
                "Columns Returned",
                len(data.columns),
            )


    elif data is not None:

        st.write(
            data
        )


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

st.divider()

st.subheader(
    "Example Questions"
)

examples = [
    "Which product line has the highest total sales?",
    "Show the average rating by branch.",
    "Which city has the highest total sales?",
    "What is the total revenue?",
    "Show the top 5 product lines by sales.",
]


for index, example in enumerate(examples):

    if st.button(
        example,
        key=f"example_{index}",
        use_container_width=True,
    ):

        with st.spinner(
            "Querying PostgreSQL..."
        ):

            try:

                result = database_agent.query(
                    example
                )

                st.session_state[
                    "database_result"
                ] = result

                st.rerun()

            except Exception as e:

                st.error(
                    f"Database query failed: {e}"
                )


# ============================================================
# AGENT INFORMATION
# ============================================================

st.divider()

st.subheader(
    "Agent Information"
)

info_col1, info_col2 = st.columns(2)


with info_col1:

    st.markdown(
        f"""
**Agent:** Database Agent

**Database:** PostgreSQL

**Query Mode:** Read-only SQL

**LLM:** `{database_agent.model}`

**Execution:** PostgreSQL
"""
    )


with info_col2:

    st.markdown(
        """
**Capabilities:**

- Natural-language database queries
- SQL generation
- Schema inspection
- Read-only SQL execution
- Aggregations
- Filtering
- Sorting
- Grouping
- Result explanation
- Tabular result display
"""
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        OmniSupport AI · Database Agent
        <br>
        PostgreSQL · Natural Language SQL · Read-Only Database Analysis
    </div>
    """,
    unsafe_allow_html=True,
)