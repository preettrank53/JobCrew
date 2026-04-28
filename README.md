# JobCrew

AI-Powered Job Application Assistant — Built with CrewAI, LangChain & Groq

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://jobcrew.streamlit.app)

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red) ![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-green) ![Deployed](https://img.shields.io/badge/Deployed-Live-brightgreen) ![License](https://img.shields.io/badge/License-MIT-yellow)

## [Live Demo : jobcrew.streamlit.app](https://jobcrew.streamlit.app)

JobCrew is an intelligent, multi-agent AI system designed to streamline the federal job application process. By leveraging advanced large language models via Groq, it automates the tedious tasks of job analysis, resume tailoring, outreach preparation, and interview preparation. This tool is built for career-driven individuals targeting federal positions who need high-quality, ATS-optimized application materials generated in seconds.

## Key Features
* live job fetching
* AI multi-agent pipeline (4 specialized agents)
* resume upload auto-fill
* one-click material generation
* interview preparation guide with STAR-format answers
* Demo Mode - full pipeline preview with no API key required
* application tracker with status management
* persistent logging

## Architecture

The JobCrew pipeline uses a multi-agent system to handle the complex workflow of job application preparation. By delegating specific responsibilities to specialized agents, the system ensures that each phase of the process-from requirement extraction to document generation—is handled with high precision and contextual awareness.

```
USAJobs API → Job Listings → User Selection
                                    ↓
                        ┌─────────────────────┐
                        │   CrewAI Pipeline   │
                        │                     │
                        │  Job Analyzer       │
                        │         ↓           │
                        │  Resume Agent       │
                        │         ↓           │
                        │  Messaging Agent    │
                        │         ↓           │
                        │  Interview Prep     │
                        └─────────────────────┘
                                    ↓
          Resume + Cover Letter + LinkedIn Message + Interview Guide
```

## Tech Stack

| Category | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| Agent Framework | CrewAI | 1.14.2 | Multi-agent orchestration and coordination |
| LLM Provider | Groq | 0.37.1 | Fast, high-quality inference using Llama 3 models |
| Web Interface | Streamlit | 1.56.0 | Interactive dashboard and UI components |
| Data Validation | Pydantic | 2.11.10 | Strong typing and schema enforcement |

## Getting Started

### Prerequisites
* Python 3.11+
* A Groq, Google Gemini, or OpenAI API key (user-provided via sidebar — bring your own key)
* [USAJobs API Key](https://developer.usajobs.gov/API-Request) (for the app owner, server-side only)

### Local Installation
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies with `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in API keys
5. Run with `streamlit run app.py`

### Environment Variables

| Variable | Required | Source |
| :--- | :--- | :--- |
| GROQ_API_KEY | Yes (server fallback) | [Groq Console](https://console.groq.com/keys) |
| USAJOBS_API_KEY | Yes | [USAJobs Developer Portal](https://developer.usajobs.gov/) |
| USAJOBS_USER_AGENT | Yes | Your registered email address |

Users provide their own LLM API key directly in the sidebar at runtime. Groq, Google Gemini, and OpenAI are supported.

## How to Use JobCrew

1. **Step 1 - Set up your candidate profile (manually or via resume upload)**
2. **Step 2 - Search for government jobs using keywords**
3. **Step 3 - Select target positions and run the pipeline**
4. **Step 4 - Review your resume, cover letter, LinkedIn message, and interview preparation guide**

### Demo Mode
Click **Launch Demo Mode** in the sidebar to experience the full pipeline instantly with no API key. Demo Mode loads a pre-built candidate profile, three sample job listings, and plays through the simulated agent pipeline to display all four output tabs with realistic pre-written content.

### Fast Mode
The Fast Mode toggle reduces the number of agent iterations and optimizes prompts for speed. This is ideal for quickly generating initial drafts or processing multiple job listings in a single session.

## Project Structure

```
JobCrew/
├── agents/             # AI agent definitions (Role, Goal, Backstory)
├── config/             # LLM configurations and application settings
├── demo/               # Demo Mode data and controller
├── tasks/              # Individual task definitions for the agents
├── tools/              # Custom tools for job fetching and data processing
├── tracker/            # Persistence logic for job application tracking
├── ui/                 # Streamlit UI components and layout helpers
├── app.py              # Main application entry point
├── crew.py             # Pipeline orchestration and execution logic
├── requirements.txt    # Production Python dependencies
└── requirements-dev.txt # Local development and testing tools
```

## AI Agents

| Agent | Role | Specialization | Output |
| :--- | :--- | :--- | :--- |
| Job Analyzer | Senior Federal Job Analyst | Requirements extraction | Structured Job Analysis |
| Resume Agent | Executive Resume Tailor | Content tailoring | Tailored Resume & Cover Letter |
| Messaging Agent | Networking Specialist | Outreach personalization | LinkedIn Message |
| Interview Prep Agent | Senior Interview Coach | STAR-format interview preparation | Interview Questions, Answers & Strategy |

## Deployment

### Streamlit Cloud
1. Push your repository to GitHub.
2. Log in to Streamlit Cloud and click "New app".
3. Select this repository and the `app.py` file.
4. Go to App Settings > Secrets to add your environment variables.

### Environment Secrets
Add your secrets in the Streamlit secrets management using this TOML format:

```toml
[secrets]
GROQ_API_KEY = "your-key-here"
USAJOBS_API_KEY = "your-key-here"
USAJOBS_USER_AGENT = "your-email@example.com"
```

Please note that the Streamlit Cloud filesystem is ephemeral; any data not saved to a persistent database or external storage will be lost when the application restarts.

## Testing
* Run the full test suite: `python tests/run_tests.py`
* Generate coverage report: `python tests/generate_coverage_report.py`

The testing strategy utilizes mocking for all external API calls (Groq and USAJobs) to ensure tests are fast, reliable, and do not incur API costs.

## Known Limitations
* Pipeline execution time can take 2-4 minutes due to four-agent reasoning chain.
* Streamlit Cloud uses an ephemeral filesystem, meaning local logs are lost on restart.
* The application currently supports single-user sessions without authentication.
* USAJobs is currently the only integrated job source.

## License
MIT License - feel free to use this project as a reference or starting point

⭐ If you found this project useful, please consider starring the repository
