import queue
import threading
import time
from pathlib import Path

import streamlit as st

from voice_assistant.orchestrator.agent_orchestrator import (
    AgentOrchestrator
)

from voice_assistant.stt import SpeechToText
from voice_assistant.tts import TextToSpeech


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OmniSupport AI - Voice Assistant",
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
       GLOBAL PAGE BACKGROUND
       ======================================================== */

    html,
    body {
        background-color: #05070b !important;
    }

    .stApp {
        background-color: #05070b !important;
        color: #f8fafc !important;
    }

    .stAppViewContainer {
        background-color: #05070b !important;
    }

    .main {
        background-color: #05070b !important;
        padding-top: 0 !important;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 1.5rem !important;
        padding-bottom: 6rem !important;
    }


    /* ========================================================
       REMOVE STREAMLIT HEADER
       ======================================================== */

    header[data-testid="stHeader"] {
        display: none !important;
    }

    div[data-testid="stToolbar"] {
        display: none !important;
    }

    div[data-testid="stDecoration"] {
        display: none !important;
    }


    /* ========================================================
       FIX STREAMLIT BOTTOM CHAT CONTAINER
       ======================================================== */

    /*
       Streamlit places st.chat_input() inside a fixed
       bottom container. These rules remove the white
       background surrounding the chat input.
    */

    div[data-testid="stBottom"] {
        background-color: #05070b !important;
        background: #05070b !important;

        border-top: 1px solid #1f2937 !important;
    }

    div[data-testid="stBottom"] > div {
        background-color: #05070b !important;
        background: #05070b !important;
    }

    div[data-testid="stBottomBlockContainer"] {
        background-color: #05070b !important;
        background: #05070b !important;

        border-top: none !important;
    }

    div[data-testid="stBottomBlockContainer"] > div {
        background-color: #05070b !important;
        background: #05070b !important;
    }


    /* ========================================================
       CHAT INPUT OUTER CONTAINER
       ======================================================== */

    div[data-testid="stChatInput"] {
        background-color: #05070b !important;
        background: #05070b !important;

        border: none !important;

        box-shadow: none !important;
    }

    div[data-testid="stChatInput"] > div {
        background-color: #05070b !important;
        background: #05070b !important;

        border: none !important;

        box-shadow: none !important;
    }


    /* ========================================================
       CHAT INPUT FORM
       ======================================================== */

    div[data-testid="stChatInput"] form {
        background-color: #0d1119 !important;
        background: #0d1119 !important;

        border: 1px solid #374151 !important;

        border-radius: 12px !important;

        box-shadow: none !important;
    }

    div[data-testid="stChatInput"] form > div {
        background-color: #0d1119 !important;
        background: #0d1119 !important;
    }


    /* ========================================================
       CHAT INPUT TEXTAREA
       ======================================================== */

    div[data-testid="stChatInput"] textarea {
        background-color: #0d1119 !important;
        background: #0d1119 !important;

        color: #f8fafc !important;

        border: none !important;

        border-radius: 12px !important;

        box-shadow: none !important;
    }

    div[data-testid="stChatInput"] textarea:focus {
        background-color: #0d1119 !important;
        color: #f8fafc !important;

        border: none !important;

        box-shadow: none !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #7f8ba3 !important;
    }


    /* ========================================================
       CHAT SEND BUTTON
       ======================================================== */

    div[data-testid="stChatInput"] button {
        background-color: #111827 !important;

        color: #e5e7eb !important;

        border: 1px solid #374151 !important;

        border-radius: 8px !important;
    }

    div[data-testid="stChatInput"] button:hover {
        background-color: #1e293b !important;

        border-color: #6366f1 !important;

        color: #ffffff !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: #090c12 !important;

        border-right: 1px solid #1f2937 !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #090c12 !important;
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
       METRICS
       ======================================================== */

    div[data-testid="metric-container"] {
        background-color: #0d1119 !important;

        border: 1px solid #1f2937 !important;

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
       CHAT MESSAGES
       ======================================================== */

    [data-testid="stChatMessage"] {
        background-color: #0d1119 !important;

        border: 1px solid #1f2937 !important;

        border-radius: 14px;

        padding: 10px;
    }


    /* ========================================================
       NORMAL BUTTONS
       ======================================================== */

    .stButton > button {
        width: 100%;

        background-color: #111827 !important;

        color: #e5e7eb !important;

        border: 1px solid #374151 !important;

        border-radius: 10px;

        padding: 0.65rem 1rem;

        font-weight: 600;

        transition:
            background-color 0.2s ease,
            border-color 0.2s ease,
            color 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #1e293b !important;

        border-color: #6366f1 !important;

        color: #ffffff !important;
    }


    /* ========================================================
       TEXT INPUTS
       ======================================================== */

    textarea {
        background-color: #0d1119 !important;

        color: #f8fafc !important;

        border: 1px solid #374151 !important;

        border-radius: 10px !important;
    }

    textarea::placeholder {
        color: #7f8ba3 !important;
    }

    input {
        background-color: #0d1119 !important;

        color: #f8fafc !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    div[data-testid="stExpander"] {
        background-color: #0d1119 !important;

        border: 1px solid #1f2937 !important;

        border-radius: 12px;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
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
       CODE BLOCKS
       ======================================================== */

    pre {
        background-color: #0a0e15 !important;

        border: 1px solid #1f2937 !important;

        border-radius: 10px !important;
    }


    /* ========================================================
       VOICE STATUS
       ======================================================== */

    .voice-status {
        background-color: #0d1119;

        border: 1px solid #1f2937;

        border-radius: 12px;

        padding: 15px;

        color: #aeb8c8;

        margin-bottom: 15px;
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


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #1f2937 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# VOICE CONVERSATION MANAGER
# ============================================================

class VoiceConversationManager:

    def __init__(self):

        self.stt = SpeechToText()

        self.tts = TextToSpeech()

        self.orchestrator = AgentOrchestrator()

        self.running = False

        self.thread = None

        self.stop_event = threading.Event()

        self.events = queue.Queue()

        self.tts_lock = threading.Lock()


    # ========================================================
    # START
    # ========================================================

    def start(self):

        if self.running:
            return

        self.stop_event.clear()

        self.running = True

        self.thread = threading.Thread(
            target=self._conversation_loop,
            daemon=True,
        )

        self.thread.start()


    # ========================================================
    # STOP
    # ========================================================

    def stop(self):

        self.stop_event.set()

        self.running = False

        # Stop microphone immediately.
        try:

            self.stt.stop_recording()

        except Exception:

            pass

        # Stop TTS immediately.
        self._stop_tts()

        self.events.put(
            {
                "type": "status",
                "message": "Voice conversation stopped.",
            }
        )


    # ========================================================
    # STOP TTS
    # ========================================================

    def _stop_tts(self):

        try:

            engine = getattr(
                self.tts,
                "engine",
                None,
            )

            if engine is not None:

                engine.stop()

        except Exception:

            pass


        try:

            stop_method = getattr(
                self.tts,
                "stop",
                None,
            )

            if callable(stop_method):

                stop_method()

        except Exception:

            pass


    # ========================================================
    # SPEAK
    # ========================================================

    def _speak(
        self,
        text,
    ):

        if not text:

            return

        if self.stop_event.is_set():

            return

        try:

            with self.tts_lock:

                if self.stop_event.is_set():

                    return

                self.events.put(
                    {
                        "type": "speaking"
                    }
                )

                self.tts.speak(
                    text
                )

        except Exception as e:

            if not self.stop_event.is_set():

                self.events.put(
                    {
                        "type": "error",
                        "message": f"TTS error: {e}",
                    }
                )


    # ========================================================
    # VOICE LOOP
    # ========================================================

    def _conversation_loop(self):

        self.events.put(
            {
                "type": "status",
                "message": (
                    "Voice conversation started. "
                    "Listening..."
                ),
            }
        )


        while not self.stop_event.is_set():

            try:

                # ------------------------------------------------
                # LISTEN
                # ------------------------------------------------

                self.events.put(
                    {
                        "type": "listening"
                    }
                )


                text = self.stt.listen(
                    stop_event=self.stop_event
                )


                # ------------------------------------------------
                # STOP CHECK
                # ------------------------------------------------

                if self.stop_event.is_set():

                    break


                if not text:

                    continue


                text = text.strip()


                if not text:

                    continue


                # ------------------------------------------------
                # VOICE STOP COMMAND
                # ------------------------------------------------

                if text.lower() in {
                    "stop",
                    "stop conversation",
                    "stop voice",
                    "stop voice conversation",
                    "stop assistant",
                    "exit",
                    "quit",
                }:

                    self.events.put(
                        {
                            "type": "user",
                            "text": text,
                        }
                    )

                    self.stop_event.set()

                    try:

                        self.stt.stop_recording()

                    except Exception:

                        pass

                    self._stop_tts()

                    break


                # ------------------------------------------------
                # USER MESSAGE
                # ------------------------------------------------

                self.events.put(
                    {
                        "type": "user",
                        "text": text,
                    }
                )


                # ------------------------------------------------
                # PROCESSING
                # ------------------------------------------------

                self.events.put(
                    {
                        "type": "processing"
                    }
                )


                result = self.orchestrator.process(
                    text
                )


                # ------------------------------------------------
                # STOP CHECK AFTER AGENT
                # ------------------------------------------------

                if self.stop_event.is_set():

                    break


                answer = result.get(
                    "answer",
                    "",
                )


                agent = result.get(
                    "agent",
                    "general",
                )


                # ------------------------------------------------
                # ASSISTANT MESSAGE
                # ------------------------------------------------

                self.events.put(
                    {
                        "type": "assistant",
                        "text": answer,
                        "agent": agent,
                        "result": result,
                    }
                )


                # ------------------------------------------------
                # TTS
                # ------------------------------------------------

                if (
                    answer
                    and not self.stop_event.is_set()
                ):

                    self._speak(
                        answer
                    )


                # ------------------------------------------------
                # STOP CHECK AFTER TTS
                # ------------------------------------------------

                if self.stop_event.is_set():

                    break


                self.events.put(
                    {
                        "type": "status",
                        "message": "Listening...",
                    }
                )


            except Exception as e:

                if self.stop_event.is_set():

                    break


                self.events.put(
                    {
                        "type": "error",
                        "message": str(e),
                    }
                )


                time.sleep(0.5)


        # ========================================================
        # FINAL CLEANUP
        # ========================================================

        self.stop_event.set()


        try:

            self.stt.stop_recording()

        except Exception:

            pass


        self._stop_tts()

        self.running = False


        self.events.put(
            {
                "type": "stopped"
            }
        )


    # ========================================================
    # EVENTS
    # ========================================================

    def get_events(self):

        events = []

        while True:

            try:

                events.append(
                    self.events.get_nowait()
                )

            except queue.Empty:

                break

        return events


# ============================================================
# CACHED COMPONENTS
# ============================================================

@st.cache_resource
def get_orchestrator():

    return AgentOrchestrator()


@st.cache_resource
def get_voice_manager():

    return VoiceConversationManager()


# ============================================================
# INITIALIZE
# ============================================================

try:

    orchestrator = get_orchestrator()

except Exception as e:

    st.error(
        f"Could not initialize OmniSupport AI: {e}"
    )

    st.stop()


try:

    voice_manager = get_voice_manager()

except Exception as e:

    st.error(
        f"Could not initialize voice system: {e}"
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "last_result" not in st.session_state:

    st.session_state.last_result = None


if "voice_status" not in st.session_state:

    st.session_state.voice_status = (
        "Voice conversation inactive."
    )


# ============================================================
# PROCESS VOICE EVENTS
# ============================================================

events = voice_manager.get_events()


for event in events:

    event_type = event.get(
        "type"
    )


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if event_type == "status":

        st.session_state.voice_status = (
            event.get(
                "message",
                "",
            )
        )


    # --------------------------------------------------------
    # LISTENING
    # --------------------------------------------------------

    elif event_type == "listening":

        st.session_state.voice_status = (
            "Listening..."
        )


    # --------------------------------------------------------
    # PROCESSING
    # --------------------------------------------------------

    elif event_type == "processing":

        st.session_state.voice_status = (
            "Processing your request..."
        )


    # --------------------------------------------------------
    # SPEAKING
    # --------------------------------------------------------

    elif event_type == "speaking":

        st.session_state.voice_status = (
            "Speaking..."
        )


    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    elif event_type == "user":

        text = event.get(
            "text",
            "",
        )


        st.session_state.messages.append(
            {
                "role": "user",
                "content": text,
                "source": "voice",
            }
        )


    # --------------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------------

    elif event_type == "assistant":

        text = event.get(
            "text",
            "",
        )


        agent = event.get(
            "agent",
            "general",
        )


        result = event.get(
            "result",
            {},
        )


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": text,
                "agent": agent,
                "source": "voice",
            }
        )


        st.session_state.last_result = result


    # --------------------------------------------------------
    # ERROR
    # --------------------------------------------------------

    elif event_type == "error":

        st.session_state.voice_status = (
            event.get(
                "message",
                "Voice error.",
            )
        )


    # --------------------------------------------------------
    # STOPPED
    # --------------------------------------------------------

    elif event_type == "stopped":

        st.session_state.voice_status = (
            "Voice conversation stopped."
        )


# ============================================================
# HEADER
# ============================================================

st.title(
    "OmniSupport AI Assistant"
)

st.caption(
    "Talk naturally with OmniSupport AI or continue "
    "the conversation using text."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "Voice Assistant"
    )


    if voice_manager.running:

        st.success(
            "Voice conversation active"
        )

    else:

        st.info(
            "Voice conversation inactive"
        )


    st.divider()


    # --------------------------------------------------------
    # AVAILABLE AGENTS
    # --------------------------------------------------------

    st.subheader(
        "Available Agents"
    )

    st.write("General")

    st.write("RAG")

    st.write("Research")

    st.write("Data Analysis")

    st.write("Database")


    st.divider()


    # --------------------------------------------------------
    # VOICE PIPELINE
    # --------------------------------------------------------

    st.subheader(
        "Voice Pipeline"
    )

    st.write("Microphone")

    st.write("Speech-to-Text")

    st.write("Agent Router")

    st.write("Specialized Agent")

    st.write("Text-to-Speech")


    st.divider()


    # --------------------------------------------------------
    # ACTIVE DATASET
    # --------------------------------------------------------

    st.subheader(
        "Active Dataset"
    )


    dataset_info = (
        orchestrator.get_dataset_info()
    )


    if dataset_info.get("loaded"):

        st.success(
            "Dataset loaded"
        )


        file_path = dataset_info.get(
            "file_path",
            "",
        )


        if file_path:

            st.write(
                f"File: {Path(file_path).name}"
            )


        st.write(
            f"Rows: "
            f"{dataset_info.get('rows', 0)}"
        )


        st.write(
            f"Columns: "
            f"{dataset_info.get('columns', 0)}"
        )


    else:

        st.info(
            "No active dataset"
        )


    st.divider()


    # --------------------------------------------------------
    # CLEAR CONVERSATION
    # --------------------------------------------------------

    if st.button(
        "Clear Conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.session_state.last_result = None

        st.rerun()


# ============================================================
# SYSTEM STATUS
# ============================================================

st.subheader(
    "System Status"
)


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "General",
        "Ready",
    )


with col2:

    st.metric(
        "RAG",
        "Ready",
    )


with col3:

    st.metric(
        "Research",
        "Ready",
    )


with col4:

    st.metric(
        "Data",
        "Ready",
    )


with col5:

    st.metric(
        "Database",
        "Ready",
    )


st.divider()


# ============================================================
# VOICE CONVERSATION
# ============================================================

st.subheader(
    "Voice Conversation"
)


if not voice_manager.running:

    st.write(
        "Start a continuous voice conversation. "
        "Speak naturally and the assistant will continue "
        "listening after each response."
    )


    if st.button(
        "Start Voice Conversation",
        type="primary",
        use_container_width=True,
    ):

        voice_manager.start()

        st.rerun()


else:

    st.success(
        "Voice conversation is active."
    )


    st.markdown(
        f"""
        <div class="voice-status">
            {st.session_state.voice_status}
        </div>
        """,
        unsafe_allow_html=True,
    )


    if st.button(
        "Stop Voice Conversation",
        type="secondary",
        use_container_width=True,
    ):

        voice_manager.stop()

        st.session_state.voice_status = (
            "Voice conversation stopped."
        )

        st.rerun()


# ============================================================
# REFRESH WHILE VOICE IS ACTIVE
# ============================================================

if voice_manager.running:

    time.sleep(0.25)

    st.rerun()


# ============================================================
# TEXT CONVERSATION
# ============================================================

st.divider()

st.subheader(
    "Text Conversation"
)

st.caption(
    "Continue the conversation using text."
)


# ============================================================
# CONVERSATION HISTORY
# ============================================================

if not st.session_state.messages:

    st.info(
        "No conversation yet."
    )

else:

    for message in st.session_state.messages:

        role = message.get(
            "role",
            "assistant",
        )


        content = message.get(
            "content",
            "",
        )


        source = message.get(
            "source",
            "text",
        )


        if role == "user":

            with st.chat_message(
                "user"
            ):

                st.caption(
                    "Voice"
                    if source == "voice"
                    else "Text"
                )


                st.write(
                    content
                )


        else:

            with st.chat_message(
                "assistant"
            ):

                agent = message.get(
                    "agent",
                    "general",
                )


                st.caption(
                    f"Agent: {agent}"
                )


                st.write(
                    content
                )


# ============================================================
# TEXT INPUT
# ============================================================

text_question = st.chat_input(
    "Type your question here..."
)


if text_question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": text_question,
            "source": "text",
        }
    )


    with st.spinner(
        "OmniSupport AI is thinking..."
    ):

        try:

            result = orchestrator.process(
                text_question
            )


            st.session_state.last_result = result


        except Exception as e:

            result = {
                "agent": "general",
                "answer": (
                    "An error occurred while "
                    "processing your request."
                ),
                "sources": [],
                "results": {},
                "charts": [],
                "reason": "",
                "error": str(e),
            }


            st.session_state.last_result = result


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result.get(
                "answer",
                "",
            ),
            "agent": result.get(
                "agent",
                "general",
            ),
            "source": "text",
        }
    )


    st.rerun()


# ============================================================
# LAST RESPONSE DETAILS
# ============================================================

result = st.session_state.last_result


if result:

    st.divider()

    st.subheader(
        "Last Response Details"
    )


    agent = result.get(
        "agent",
        "general",
    )


    reason = result.get(
        "reason",
        "",
    )


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            f"Selected Agent: `{agent}`"
        )


    with col2:

        if reason:

            st.write(
                f"Routing: {reason}"
            )


    # ========================================================
    # DATABASE
    # ========================================================

    if agent == "database":

        sql = result.get(
            "sql"
        )


        if sql:

            with st.expander(
                "Generated SQL"
            ):

                st.code(
                    sql,
                    language="sql",
                )


        db_results = result.get(
            "results",
            {},
        )


        if db_results:

            with st.expander(
                "Database Results",
                expanded=True,
            ):

                if isinstance(
                    db_results,
                    dict,
                ):

                    st.json(
                        db_results
                    )

                else:

                    st.write(
                        db_results
                    )


    # ========================================================
    # RESEARCH
    # ========================================================

    if agent == "research":

        sources = result.get(
            "sources",
            [],
        )


        if sources:

            with st.expander(
                "Research Sources",
                expanded=True,
            ):

                for source in sources:

                    if isinstance(
                        source,
                        dict,
                    ):

                        title = source.get(
                            "title",
                            "Source",
                        )


                        url = source.get(
                            "url",
                            "",
                        )


                        st.markdown(
                            f"**{title}**"
                        )


                        if url:

                            st.markdown(
                                f"[Open source]({url})"
                            )


                    else:

                        st.write(
                            source
                        )


    # ========================================================
    # RAG
    # ========================================================

    if agent == "rag":

        sources = result.get(
            "sources",
            [],
        )


        if sources:

            with st.expander(
                "Retrieved Documents",
                expanded=True,
            ):

                for source in sources:

                    st.write(
                        source
                    )


    # ========================================================
    # DATA ANALYSIS
    # ========================================================

    if agent == "data":

        data_results = result.get(
            "results",
            {},
        )


        if data_results:

            with st.expander(
                "Data Analysis Results",
                expanded=True,
            ):

                if isinstance(
                    data_results,
                    dict,
                ):

                    for key, value in data_results.items():

                        st.write(
                            f"{key}:"
                        )

                        st.write(
                            value
                        )

                else:

                    st.write(
                        data_results
                    )


        charts = result.get(
            "charts",
            [],
        )


        if charts:

            with st.expander(
                "Generated Charts",
                expanded=True,
            ):

                for chart in charts:

                    try:

                        st.image(
                            chart,
                            use_container_width=True,
                        )

                    except Exception:

                        st.write(
                            chart
                        )


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

st.divider()

st.subheader(
    "Example Questions"
)


examples = [
    "What is machine learning?",
    "What does my uploaded PDF say about AI?",
    "Research the latest developments in AI.",
    "Which product line has the highest total sales?",
    "Which product line has the highest total sales in the database?",
]


for index, example in enumerate(
    examples
):

    if st.button(
        example,
        key=f"example_{index}",
        use_container_width=True,
    ):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": example,
                "source": "text",
            }
        )


        with st.spinner(
            "Processing..."
        ):

            try:

                result = orchestrator.process(
                    example
                )


                st.session_state.last_result = result


            except Exception as e:

                result = {
                    "agent": "general",
                    "answer": (
                        "An error occurred while "
                        "processing the request."
                    ),
                    "sources": [],
                    "results": {},
                    "charts": [],
                    "reason": "",
                    "error": str(e),
                }


                st.session_state.last_result = result


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result.get(
                    "answer",
                    "",
                ),
                "agent": result.get(
                    "agent",
                    "general",
                ),
                "source": "text",
            }
        )


        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        OmniSupport AI · Voice Assistant
        <br>
        Speech-to-Text · Agent Router · Specialized Agents · Text-to-Speech
    </div>
    """,
    unsafe_allow_html=True,
)