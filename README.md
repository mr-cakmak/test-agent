# LangGraph AI Agent with Flask UI

This project is a **LangGraph AI agent** designed for test case analysis and prioritization, with a **simple Flask web UI** for convenient interaction. The AI agent is completely independent from the Flask interface and can be used standalone via command line.

## Overview

The LangGraph AI agent processes test cases and queries to provide intelligent analysis and prioritization. It uses a graph-based workflow to:
- Cluster test cases when needed
- Create evaluation rubrics
- Evaluate and sort test cases by relevance
- Provide prioritized recommendations

## Project Structure

```
src/
├── core/
│   ├── graph.py          # Main LangGraph workflow
│   └── state.py          # State definitions
├── nodes/               # Graph nodes (workflow steps)
│   ├── create_clusters.py
│   ├── create_rubric.py
│   ├── evaluate_test_cases.py
│   ├── pick_relevant_clusters.py
│   └── sort_test_cases.py
├── api/
│   ├── llm_client.py     # LLM integration
│   └── tc_file.py        # Test case definitions
└── utils/
    └── parse_llm.py      # LLM response parsing
```

## Usage Options

### Option 1: Web UI (Recommended)

The Flask web interface provides an easy way to interact with the AI agent through your browser.

**1. Start the Flask server:**
```bash
./run_ui.sh
```
Or manually:
```bash
source test-agent-env/bin/activate
python app.py
```

**2. Open your browser** and navigate to: `http://localhost:5000`

**3. Fill in the form:**
- **Query**: Enter your testing question (e.g., "We updated the URL generation algorithm. What should we test?")
- **Test Cases**: Enter test cases in JSON format or as plain text

**4. Click "Run AI Agent"** to execute the agent with your inputs

### Option 2: Command Line (Standalone)

The AI agent can be run independently without the Flask UI:

```bash
source test-agent-env/bin/activate
python main.py
```

The agent is completely independent from Flask and uses the same core workflow regardless of how it's invoked.

## Test Cases Format

When using the web UI, you can provide test cases in two ways:

**JSON Format** (recommended):
```json
[
  {
    "id": "1",
    "test_name": "test_basic_functionality",
    "summary": "Test basic functionality works correctly",
    "steps": ["Step 1", "Step 2"],
    "notes": ["Important note"]
  }
]
```

**Plain Text**: The system will automatically convert plain text into a simple test case structure.

## Installation

1. Create and activate virtual environment:
```bash
python -m venv test-agent-env
source test-agent-env/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables (if needed for LLM APIs)


## Architecture

- **LangGraph Agent**: Core AI workflow in `src/core/graph.py`
- **Flask UI**: Optional web interface in `app.py`
- **Independence**: The agent works standalone - Flask is just a convenient wrapper
- **Modularity**: Each workflow step is a separate node for easy maintenance and testing