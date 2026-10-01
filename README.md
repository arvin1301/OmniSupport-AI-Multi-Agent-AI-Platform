# OmniSupport-AI-Multi-Agent-AI-Platform

OmniSupport AI is an end-to-end AI platform that combines LLM reasoning, RAG, web research, data analysis, PostgreSQL querying, and voice interaction into a single modular application.
The system uses an Agent Router to understand the user's request and route it to the appropriate specialized agent. Each agent uses a dedicated workflow, tools, and LLM depending on the task.
Overview
OmniSupport AI supports the following capabilities:
- General AI conversations
- Retrieval-Augmented Generation (RAG)
- Current web research
- CSV and Excel data analysis
- Natural-language PostgreSQL querying
- Continuous voice interaction
- Dataset state management
- Tool-based processing
- Agent and integration testing

  
The main interaction flow is:
<img width="1024" height="1536" alt="Architecture" src="https://github.com/user-attachments/assets/e459f8a5-2e0a-4f0c-ba57-e169319b87d4" />


Key Features
General AI
Handles general questions and conversations using:
LLM: openai/gpt-oss-20b
RAG
Answers questions based on uploaded documents using:
- PyMuPDF
- Sentence Transformers
- all-MiniLM-L6-v2
- ChromaDB
- GPT-OSS 120B
Web Research
Performs current information research using:
- Google News RSS
- Source processing
- Qwen 3.8 27B
Data Analysis
Allows users to upload CSV/Excel datasets and interact with them using natural language.
Uses:
- Pandas
- NumPy
- Python execution
- Matplotlib
- GPT-OSS 120B
PostgreSQL Database Agent
Allows users to ask database questions in natural language.
Uses:
- PostgreSQL
- Docker
- Schema inspection
- SQL generation
- Read-only SQL execution
- GPT-OSS 20B
Voice Assistant
Provides continuous voice interaction using:
- Whisper Large V3 Turbo
- GPT-OSS 20B
- PyAudio
- Voice Activity Detection
- pyttsx3 / Windows SAPI5
AI Agents and LLM Models
Agent	LLM / Model	Main Purpose
General Agent	openai/gpt-oss-20b	General conversations
RAG Agent	openai/gpt-oss-120b	Document-based Q&A
Research Agent	qwen/qwen3.8-27b	Current web research
Data Analysis Agent	openai/gpt-oss-120b	Dataset analysis
Database Agent	openai/gpt-oss-20b	Natural-language SQL
Voice Assistant	openai/gpt-oss-20b	Voice interaction


Supporting Models
Component	Model
Speech-to-Text	whisper-large-v3-turbo
RAG Embeddings	all-MiniLM-L6-v2
Text-to-Speech	pyttsx3 / Windows SAPI5


System Architecture

<img width="1024" height="1536" alt="Inner Architecture" src="https://github.com/user-attachments/assets/559615c9-d8b8-49de-8606-98d6e0d67999" />


Agent Router
The Agent Router determines which specialized workflow should handle a request.
Examples:
"Explain this uploaded PDF"
        |
        v
    RAG Agent

"What are the latest developments in generative AI?"
        |
        v
 Research Agent

"What is the average sales?"
        |
        v
Data Analysis Agent

"Which product line has the highest total sales?"
        |
        v
Database Agent

"Explain what machine learning is."
        |
        v
General Agent

The router allows the platform to use different tools and models depending on the user's intent.

## RAG Agent
The RAG Agent allows the system to answer questions from uploaded documents.

RAG Pipeline
<img width="1536" height="1024" alt="RAG" src="https://github.com/user-attachments/assets/7e930004-dfc3-4919-84d4-d8d72f8c0c8d" />


Models
LLM:
openai/gpt-oss-120b

Embedding:
all-MiniLM-L6-v2

Vector Database:
ChromaDB

Example:
According to the uploaded document,
what are the major impacts of AI?

The system retrieves relevant document chunks and provides them as context to the LLM.

# Research Agent
The Research Agent is designed for questions that require current external information.
Research Pipeline
<img width="1774" height="887" alt="Research_agent" src="https://github.com/user-attachments/assets/c3978ef0-941f-4520-8c41-0fc447aa1dce" />

Model
qwen/qwen3.8-27b

Search Source
Google News RSS

Example:
What are the latest developments in generative AI?

The agent retrieves relevant search results and provides the available research context to the LLM.


# Data Analysis Agent
The Data Analysis Agent allows users to work with structured datasets through natural-language questions.
Supported files:
.csv
.xlsx
.xls

Data Analysis Pipeline
<img width="1536" height="1024" alt="Data Analysis" src="https://github.com/user-attachments/assets/62fe10d9-9186-459b-b46f-01007913a947" />

Example questions:
What is the average sales?

Which product has the highest sales?

Show sales by region.

What is the correlation between sales and quantity?

Create a chart showing sales by product.

The agent can generate Python analysis code, execute it against the active dataset, and return results or visualizations.


# PostgreSQL Database Agent
The Database Agent provides natural-language interaction with PostgreSQL.
Instead of manually writing SQL, users can ask questions in natural language.

Database Pipeline
<img width="1536" height="1024" alt="database" src="https://github.com/user-attachments/assets/8d68b68a-83a2-47c2-8b80-ff012f42640e" />

Example:
Which product line has the highest total sales?

The generated SQL can follow a workflow such as:
SELECT
    "Product line",
    SUM("Total") AS total_sales
FROM walmart_sales
GROUP BY "Product line"
ORDER BY total_sales DESC
LIMIT 1;

The PostgreSQL database runs inside Docker.
Voice Assistant
The Voice Assistant provides a continuous voice interface to the platform.
Voice Models
Speech-to-Text
whisper-large-v3-turbo

LLM
openai/gpt-oss-20b

Text-to-Speech
pyttsx3 / Windows SAPI5

# Voice Pipeline
<img width="1536" height="1024" alt="Voice_agent" src="https://github.com/user-attachments/assets/8c0210b7-e666-4afd-9e89-4275f5d02f26" />

The voice assistant uses the same backend agents as the text interface.
For example:
User speaks:
"What are the latest developments in artificial intelligence?"

        ↓

Whisper

        ↓

Agent Router

        ↓

Research Agent

        ↓

Google News RSS

        ↓

Qwen 3.8 27B

        ↓

Response

        ↓

Text-to-Speech


# Orchestrator
The AgentOrchestrator coordinates the different agents and provides a common processing layer for the dashboard and voice assistant.
It manages:
- Agent routing
- General conversations
- RAG requests
- Research requests
- Data analysis
- Database queries
- Active dataset state
- Dataset restoration
- Agent responses
- Results
- Charts
- Sources


The high-level flow is:
User Request
     |
     v
Agent Router
     |
     v
Agent Orchestrator
     |
     +---- General Agent
     |
     +---- RAG Agent
     |
     +---- Research Agent
     |
     +---- Data Analysis Agent
     |
     +---- Database Agent

## Streamlit Dashboard
The project uses Streamlit as the main user interface.
The dashboard provides dedicated pages for:
Home
 |
 +-- RAG
 |
 +-- Research
 |
 +-- Data Analysis
 |
 +-- Voice Assistant
 |
 +-- Database

Each page communicates with the corresponding backend components.
Project Structure
Project_OmniSupport_AI/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
│
├── data/
│   ├── documents/
│   ├── datasets/
│   ├── uploads/
│   ├── vectorstore/
│   └── charts/
│
├── voice_assistant/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── llm.py
│   ├── stt.py
│   ├── tts.py
│   │
│   ├── router/
│   │   ├── __init__.py
│   │   └── agent_router.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   │
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── rag_agent.py
│   │   │   ├── document_loader.py
│   │   │   ├── chunker.py
│   │   │   ├── embeddings.py
│   │   │   ├── vector_store.py
│   │   │   ├── retriever.py
│   │   │   └── ingestion.py
│   │   │
│   │   ├── research/
│   │   │   ├── __init__.py
│   │   │   ├── research_agent.py
│   │   │   ├── web_search.py
│   │   │   └── source_manager.py
│   │   │
│   │   ├── data_analysis/
│   │   │   ├── __init__.py
│   │   │   ├── data_agent.py
│   │   │   ├── data_loader.py
│   │   │   ├── analyzer.py
│   │   │   ├── python_executor.py
│   │   │   └── chart_generator.py
│   │   │
│   │   └── database/
│   │       ├── __init__.py
│   │       ├── database_agent.py
│   │       ├── connection.py
│   │       ├── schema_inspector.py
│   │       ├── sql_generator.py
│   │       └── sql_executor.py
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── memory_manager.py
│   │   └── dataset_state.py
│   │
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   └── agent_orchestrator.py
│   │
│   └── tools/
│       ├── __init__.py
│       ├── calculator.py
│       ├── web_tools.py
│       └── file_tools.py
│
├── dashboard/
│   ├── app.py
│   │
│   ├── pages/
│   │   ├── 1_Home.py
│   │   ├── 2_RAG.py
│   │   ├── 3_Research.py
│   │   ├── 4_Data_Analysis.py
│   │   ├── 5_Voice_Assistant.py
│   │   └── 6_Database.py
│   │
│   └── components/
│       ├── charts.py
│       ├── chat.py
│       └── metrics.py
│
└── tests/
    ├── test_memory.py
    ├── test_rag.py
    ├── test_research.py
    ├── test_data_loader.py
    ├── test_analyzer.py
    ├── test_chart_generator.py
    ├── test_python_executor.py
    ├── test_data_agent.py
    ├── test_orchestrator.py
    ├── test_dataset_state.py
    ├── test_database_connection.py
    ├── test_database_import.py
    ├── test_schema_inspector.py
    ├── test_sql_generator.py
    ├── test_sql_executor.py
    ├── test_database_agent.py
    ├── test_agent_router.py
    ├── test_orchestrator_database.py
    └── test_all_agents.py

Technology Stack
Programming
- Python 3.10
- Pandas
- NumPy
- Matplotlib
LLM
- Groq
- GPT-OSS 20B
- GPT-OSS 120B
- Qwen 3.8 27B
RAG
- PyMuPDF
- Sentence Transformers
- all-MiniLM-L6-v2
- ChromaDB
Web Research
- Google News RSS
- Requests
- BeautifulSoup
Data Analysis
- Pandas
- NumPy
- Matplotlib
- Controlled Python execution
Database
- PostgreSQL
- SQLAlchemy
- psycopg2
- Docker
Voice
- Whisper Large V3 Turbo
- PyAudio
- pyttsx3
- Windows SAPI5
- Voice Activity Detection
Frontend
- Streamlit
System Requirements
Recommended environment:
- Windows 10/11
- Python 3.10
- Git
- Docker Desktop
- Internet connection
- Microphone for voice functionality
- At least 8 GB RAM
- 16 GB RAM recommended
Installation
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/OmniSupport-AI.git
cd OmniSupport-AI

Replace YOUR_USERNAME with your GitHub username.
2. Create a Virtual Environment
python -m venv .venv

Activate it on Windows PowerShell:
.venv\Scripts\Activate.ps1

Verify Python:
python --version

The project is designed for Python 3.10.
3. Install Dependencies
pip install -r requirements.txt

Environment Configuration
Create a .env file in the project root.
Example:
GROQ_API_KEY=your_groq_api_key

STT_MODEL=whisper-large-v3-turbo
LLM_MODEL=openai/gpt-oss-20b

GENERAL_LLM_MODEL=openai/gpt-oss-20b
RAG_LLM_MODEL=openai/gpt-oss-120b
RESEARCH_LLM_MODEL=qwen/qwen3.8-27b
DATA_LLM_MODEL=openai/gpt-oss-120b

POSTGRES_HOST=localhost
POSTGRES_PORT=15432
POSTGRES_DB=omnisupport
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_database_password

Never commit your .env file to GitHub.
Use .env.example to document the required variables.
PostgreSQL and Docker Setup
The Database Agent requires PostgreSQL.
Docker Desktop should be installed and running.
Create the PostgreSQL container:
docker run -d `
  --name omnisupport-postgres `
  -e POSTGRES_PASSWORD=your_database_password `
  -e POSTGRES_DB=omnisupport `
  -e POSTGRES_USER=postgres `
  -p 15432:5432 `
  -v omnisupport_postgres_data:/var/lib/postgresql/data `
  postgres:17

Check the container:
docker ps

Check PostgreSQL:
docker exec omnisupport-postgres pg_isready -U postgres

Expected result:
accepting connections

The application uses:
Host: localhost
Port: 15432
Database: omnisupport
User: postgres

The host port is mapped to PostgreSQL's internal Docker port:
localhost:15432
        |
        v
Docker PostgreSQL:5432

Database Dataset
The project uses a Walmart Sales dataset for the PostgreSQL workflow.
The primary table is:
walmart_sales

After importing the dataset, verify the table:
docker exec omnisupport-postgres psql `
  -U postgres `
  -d omnisupport `
  -c "\dt"

Check the row count:
docker exec omnisupport-postgres psql `
  -U postgres `
  -d omnisupport `
  -c "SELECT COUNT(*) FROM walmart_sales;"

Running the Application
After configuring the environment and starting PostgreSQL:
streamlit run dashboard/app.py

The Streamlit dashboard will open in your browser.
Project Usage
RAG
1. Open the RAG page.
2. Upload a PDF or supported document.
3. Ingest the document.
4. Ask a question about the document.
5. The system retrieves relevant chunks from ChromaDB.
6. GPT-OSS 120B generates the response.
Example:
According to this document, what are the major impacts of AI?

Research
1. Open the Research page.
2. Enter a research question.
3. Start the research workflow.
4. Google News RSS retrieves current search results.
5. Sources are processed.
6. Qwen 3.8 27B generates the research response.
Example:
What are the latest developments in generative AI?

Data Analysis
1. Open Data Analysis.
2. Upload a CSV or Excel dataset.
3. The dataset becomes the active dataset.
4. Ask questions using natural language.
5. The Data Analysis Agent generates analysis logic.
6. Controlled Python execution performs the analysis.
7. Results and charts are returned.
Example:
What is the average sales?

Show sales by product.

Which product has the highest sales?

Create a chart of sales by region.

Database
1. Start PostgreSQL.
2. Ensure the walmart_sales table exists.
3. Open the Database page.
4. Enter a natural-language database question.
5. The Database Agent inspects the schema.
6. SQL is generated.
7. The query is executed against PostgreSQL.
8. Results are converted into a natural-language response.
Example:
Which product line has the highest total sales?

Voice Assistant
1. Connect a microphone.
2. Open the Voice Assistant page.
3. Start the voice conversation.
4. Speak naturally.
5. Whisper converts speech into text.
6. The Agent Router determines the appropriate agent.
7. The selected agent processes the request.
8. pyttsx3 speaks the response.
The voice assistant can access the same specialized workflows as the text interface.
Standalone Voice Assistant
The voice assistant can also be launched directly:
python -m voice_assistant.main

The application provides:
1. Text Mode
2. Voice Mode

Text mode:
Keyboard
   ↓
Agent Router
   ↓
Agent
   ↓
Text Response

Voice mode:
Microphone
   ↓
Whisper
   ↓
Agent Router
   ↓
Agent
   ↓
Text-to-Speech
   ↓
Speaker

Testing
The project contains tests for individual components, agents, routing, orchestration, and integrations.
RAG
python tests/test_rag.py

Research
python tests/test_research.py

Data Loading
python tests/test_data_loader.py

Data Analysis
python tests/test_analyzer.py

Chart Generation
python tests/test_chart_generator.py

Python Execution
python tests/test_python_executor.py

Data Analysis Agent
python tests/test_data_agent.py

Dataset State
python tests/test_dataset_state.py

PostgreSQL Connection
python tests/test_database_connection.py

Database Import
python tests/test_database_import.py

Schema Inspector
python tests/test_schema_inspector.py

SQL Generator
python tests/test_sql_generator.py

SQL Executor
python tests/test_sql_executor.py

Database Agent
python tests/test_database_agent.py

Agent Router
python tests/test_agent_router.py

Orchestrator
python tests/test_orchestrator.py

Database Orchestration
python tests/test_orchestrator_database.py

Full Agent Regression
python tests/test_all_agents.py

Recommended Development Workflow
Activate Virtual Environment
          |
          v
Modify Source Code
          |
          v
Run Component Tests
          |
          v
Run Integration Tests
          |
          v
Run Full Regression
          |
          v
Start Streamlit
          |
          v
Test Dashboard
          |
          v
Commit Changes

Example:
.venv\Scripts\Activate.ps1

python tests/test_agent_router.py

python tests/test_all_agents.py

streamlit run dashboard/app.py

Troubleshooting
PostgreSQL Connection Failed
Check whether the container is running:
docker ps

If it is stopped:
docker start omnisupport-postgres

Check PostgreSQL:
docker exec omnisupport-postgres pg_isready -U postgres

Check the .env configuration:
POSTGRES_HOST=localhost
POSTGRES_PORT=15432
POSTGRES_DB=omnisupport
POSTGRES_USER=postgres

Groq API Error
Verify:
GROQ_API_KEY=your_groq_api_key

Then restart the application.
Make sure the API key has not been accidentally committed to Git.
RAG Embedding Model Download
The first RAG execution may take longer because the embedding model can need to be downloaded and initialized.
Later executions should reuse the locally available model.
Microphone Problems
Check:
- Windows microphone permissions
- Default recording device
- PyAudio installation
- Microphone availability
- Windows audio settings
Then restart the application.
Text-to-Speech Problems
The Voice Assistant uses:
pyttsx3
Windows SAPI5

Verify that Windows audio output and speech services are available.
Security
Do not commit sensitive information to GitHub.
Never commit:
.env
API keys
Database passwords
Private documents
Private datasets
Credentials

Runtime/generated files should also remain outside version control where appropriate:
.venv/
__pycache__/
data/vectorstore/
data/uploads/
data/charts/
data/memory.db

The .gitignore file should exclude these files and directories.
Use:
.env.example

to document required environment variables without exposing secrets.
The PostgreSQL workflow is designed around read-only SQL execution.
The Data Analysis Agent uses controlled Python execution rather than unrestricted system-level execution.
Example End-to-End Workflows
Document Question
User
 |
 v
"According to the uploaded document,
 what are the major impacts of AI?"
 |
 v
Agent Router
 |
 v
RAG Agent
 |
 v
ChromaDB Retrieval
 |
 v
GPT-OSS 120B
 |
 v
Answer + Sources

Current Research
User
 |
 v
"What are the latest developments
 in generative AI?"
 |
 v
Agent Router
 |
 v
Research Agent
 |
 v
Google News RSS
 |
 v
Qwen 3.8 27B
 |
 v
Answer + Sources

Dataset Analysis
User
 |
 v
"What is the average sales?"
 |
 v
Agent Router
 |
 v
Data Analysis Agent
 |
 v
GPT-OSS 120B
 |
 v
Python / Pandas
 |
 v
Analysis Result

Database Query
User
 |
 v
"Which product line has the
 highest total sales?"
 |
 v
Agent Router
 |
 v
Database Agent
 |
 v
Schema Inspection
 |
 v
SQL Generation
 |
 v
PostgreSQL
 |
 v
Natural Language Answer

Voice Query
User Speech
 |
 v
Microphone
 |
 v
VAD
 |
 v
Whisper Large V3 Turbo
 |
 v
Agent Router
 |
 v
Specialized Agent
 |
 v
LLM
 |
 v
Response
 |
 v
pyttsx3
 |
 v
Speaker

Project Goals
OmniSupport AI was developed to demonstrate how multiple AI capabilities can be combined into a modular application.
The project demonstrates:
- LLM-based agent routing
- Specialized AI agents
- Retrieval-Augmented Generation
- Vector search
- Current web research
- Natural-language data analysis
- LLM-generated Python analysis
- Natural-language SQL generation
- PostgreSQL integration
- Voice AI
- Speech-to-text
- Text-to-speech
- Dataset state management
- Docker-based database infrastructure
- Streamlit application development
- Component testing
- Integration testing
- End-to-end agent testing
Future Improvements
Potential future extensions include:
- Additional specialized agents
- More external tools and APIs
- Advanced conversational memory
- Additional database connectors
- Improved agent evaluation
- More visualization capabilities
- Improved voice interruption handling
- Authentication and user management
- Production deployment
- Cloud deployment
Author
Phurailatpam Arvind Sharma
Data Science | Machine Learning | Generative AI | LLM Applications
License
This project is intended for educational, experimental, and portfolio purposes.
If a specific open-source license is added to the repository, this section should be updated accordingly.
Quick Start
For a quick local setup:
git clone https://github.com/YOUR_USERNAME/OmniSupport-AI.git

cd OmniSupport-AI

python -m venv .venv

.venv\Scripts\Activate.ps1

pip install -r requirements.txt

Create .env and configure the required variables.
Start PostgreSQL:
docker start omnisupport-postgres

Then launch OmniSupport AI:
streamlit run dashboard/app.py

The application is then ready to use through the Streamlit dashboard.
