# JobCrew

## Project Overview

JobCrew is an autonomous, multi-agent artificial intelligence application designed to streamline the federal job application process. By integrating directly with the USAJobs API, the system allows users to search for live government positions and automatically generates tailored application materials. 

The core engine relies on a sequential pipeline of specialized AI agents that analyze job requirements, customize resumes and cover letters, and draft professional outreach messages. The system runs entirely locally using Ollama, ensuring data privacy and eliminating API costs.

## Architecture and Agents

JobCrew utilizes a CrewAI orchestration pipeline consisting of three distinct agents:

1. **Job Analyzer Agent**: Ingests raw job description data from the USAJobs API and extracts structured requirements, including necessary skills, required education, and organizational culture signals.
2. **Resume Customizer Agent**: Receives the structured analysis and the user's candidate profile to draft a highly tailored resume summary and a targeted cover letter.
3. **Messaging Agent**: Analyzes the job context and candidate profile to draft a professional, concise outreach message suitable for networking.

## Prerequisites

Before installing the application, ensure the following dependencies are installed on your system:

- Python 3.10 or higher
- Ollama (installed and running locally)
- Llama 3.2 model downloaded via Ollama

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd JobCrew
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .\.venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install the required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and add your USAJobs API credentials:
   ```env
   USAJOBS_API_KEY=your_api_key_here
   USAJOBS_USER_AGENT=your_email@example.com
   ```

5. **Download the local language model:**
   Ensure the Ollama application is running on your machine, then execute:
   ```bash
   ollama run llama3.2
   ```

## Usage Instructions

To launch the application interface:

1. Activate your virtual environment if it is not already active.
2. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open your web browser and navigate to the local URL provided by Streamlit (typically `http://localhost:8501`).
4. **Step 1**: Complete and save your Candidate Profile in the left sidebar.
5. **Step 2**: Search for government jobs using keywords and locations in the main panel. Select the positions you wish to apply for.
6. **Step 3**: Click the Run Pipeline button to execute the multi-agent workflow. The system will process each selected job and present the generated materials in organized tabs for review and download.

## Project Structure

- `app.py`: The main entry point for the Streamlit web application.
- `crew.py`: The orchestration logic defining the CrewAI sequential process.
- `agents/`: Contains the definitions and configurations for the AI agents.
- `tasks/`: Contains the specific tasks assigned to the AI agents.
- `tools/`: Contains utility scripts, including the USAJobs API integration.
- `config/`: Contains the system settings and Language Model configuration.
- `ui/`: Contains modular UI components for layout, sidebar, search, and results display.
- `logs/`: Directory where generated application materials are automatically saved.

## Contributing

Contributions to JobCrew are welcome. Please ensure that any pull requests maintain the existing modular architecture and adhere to standard Python styling guidelines (PEP 8). Prior to submitting a pull request, verify that all UI components render correctly and that the agent pipeline executes without errors.

## License

This project is licensed under the MIT License. See the LICENSE file for details.