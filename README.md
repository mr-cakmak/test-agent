# LangGraph AI Agent with Flask UI

This project is a **LangGraph AI agent** designed for test case analysis and prioritization, with a **simple Flask web UI** for convenient interaction. The AI agent is completely independent from the Flask interface and can be used standalone via command line.

## Overview

The LangGraph AI agent is a **test case prioritizer** that helps development and QA teams intelligently prioritize testing efforts based on natural language queries. Instead of manually sifting through hundreds of test cases, teams can ask questions in plain English and get prioritized, relevant test cases that address their specific concerns.

### What Does the Agent Do?

The agent processes your testing concerns and automatically:
- **Analyzes** your query to understand the testing context and risks
- **Clusters** related test cases when dealing with large test suites
- **Creates evaluation rubrics** based on your specific needs and concerns
- **Evaluates and scores** test cases against these criteria
- **Prioritizes** test cases to show you what to test first

### Real-World Use Cases

**Feature Change Testing:**
- *"We just updated the password reset flow to include multi-factor authentication. Which tests should we run first?"*
- *"The team refactored how product images are loaded and cached. What should we test to make sure this didn't break anything?"*

**Risk-Based Testing:**
- *"We're pushing this update to production tonight. What tests would catch the issues that would cause the biggest customer impact?"*
- *"We need to validate our system's security before the compliance audit next week. What should we focus on?"*

**Performance & Load Testing:**
- *"We're concerned about performance on the mobile app for users with slow connections. What tests should we prioritize?"*
- *"We have a major promotional event this weekend with expected traffic spikes. What should we test?"*

**Integration & Dependencies:**
- *"We updated several third-party dependencies. What core functionality should we verify first?"*
- *"I'm worried about how these changes might affect our payment gateway integration. What tests should we focus on?"*

### Agent Workflow

The agent uses a graph-based workflow to:
- Cluster test cases when needed
- Create evaluation rubrics
- Evaluate and sort test cases by relevance
- Provide prioritized recommendations

### Agent Workflow Visualization

![AI Agent Graph](graph.png)

*The above diagram shows the complete workflow of the LangGraph AI agent, including all nodes and their connections.*

## Project Structure

```
src/
├── core/                 # Core components: graph and state
│   ├── graph.py          # Main LangGraph workflow
│   └── state.py          # State definitions
├── nodes/               # Graph nodes (workflow steps)
│   ├── create_clusters.py
│   ├── create_rubric.py
│   ├── evaluate_test_cases.py
│   ├── pick_relevant_clusters.py
│   └── sort_test_cases.py
├── api/                 # External API connection codes
│   ├── llm_client.py     # LLM integration
│   └── tc_file.py        # Test case definitions
└── utils/               # Utility functions that nodes use
    └── parse_llm.py      # LLM response parsing
```

### Folder Descriptions

- **core/**: Contains the main graph definition and state management
- **nodes/**: Individual workflow nodes that make up the LangGraph execution steps
- **api/**: External API connection codes for integrating with LLMs and other services
- **utils/**: Utility functions and helpers that the nodes use for processing

## Agent Architecture & Workflow

The AI agent uses a **LangGraph-based workflow** with intelligent routing between specialized nodes. Each node handles a specific aspect of test case analysis and prioritization.

### Workflow Nodes

**1. Create Clusters (`create_clusters.py`)**
- Groups similar test cases together when dealing with large test suites
- Uses semantic similarity to identify related functionality
- Only triggered when clustering would improve analysis efficiency

**2. Pick Relevant Clusters (`pick_relevant_clusters.py`)**
- Analyzes your query to identify which test case clusters are most relevant
- Filters out unrelated test groups to focus analysis
- Ensures the agent works efficiently even with hundreds of test cases

**3. Create Rubric (`create_rubric.py`)**
- Dynamically generates evaluation criteria based on your specific query
- Creates scoring rubrics that align with your testing concerns
- Adapts to different types of testing needs (security, performance, functionality, etc.)

**4. Evaluate Test Cases (`evaluate_test_cases.py`)**
- Scores each relevant test case against the generated rubric
- Considers factors like risk, coverage, and relevance to your query
- Provides detailed reasoning for each test case's importance

**5. Sort Test Cases (`sort_test_cases.py`)**
- Ranks test cases by their evaluation scores
- Provides a prioritized list with the most critical tests first
- Includes explanations for why each test case was prioritized

### Intelligent Routing

The agent doesn't always execute every node. Based on your query and the test suite size, it intelligently decides:
- Whether clustering is needed (for large test suites)
- Which clusters are relevant to your specific concern
- How to weight different evaluation criteria

This makes the agent both efficient and accurate, providing relevant results quickly regardless of test suite size.

## Agent Internal Mechanisms

Understanding how the agent processes your query and test cases helps appreciate its sophistication and efficiency.

### Step-by-Step Processing

**1. Input Processing**
- User provides a natural language query and test cases
- Agent analyzes the query to understand testing context and priorities

**2. Semantic Clustering**
- Agent clusters test cases based on their semantic and domain meanings
- This is crucial for efficiency: with hundreds of test cases, many may be unrelated to your query
- Clustering eliminates unnecessary computation and reduces LLM API costs
- Groups similar functionality together (e.g., all authentication tests, all payment tests)

**3. Cluster Relevance Selection**
- A specialized node picks only the most relevant clusters for your specific query/task
- If you ask about "payment gateway issues," only payment-related clusters are selected
- This further reduces processing scope and improves accuracy

**4. Dynamic Rubric Creation**
- Agent creates a custom evaluation rubric based on your specific query
- Instead of generic scoring, the rubric adapts to your testing concerns
- For security queries: focuses on risk, vulnerability coverage, compliance
- For performance queries: emphasizes load testing, response times, resource usage
- This rubric-based approach is much more robust than passing all test cases to LLM for ad-hoc evaluation

**5. Batch Evaluation with Justification**
- Agent processes test cases in batches of 5 (to optimize API costs while maintaining quality)
- Each batch is evaluated against the custom rubric by the LLM
- LLM provides numerical grades for each dimension in the rubric
- **Crucially**: LLM must provide justification for each grade, ensuring transparent reasoning
- This batch approach balances cost efficiency with evaluation quality

**6. Completion Check & Continuation**
- Agent tracks evaluation progress and ensures all relevant test cases are processed
- If test cases remain unevaluated, the process continues with remaining batches
- Guarantees complete coverage of all relevant test cases

**7. Final Prioritization**
- Final node takes all evaluated test cases with their scores and justifications
- Sorts them by overall points to create a prioritized list
- Returns ranked test cases with explanations for why each is important

### Why This Approach Works

**Cost Efficiency**: Clustering and batching reduce unnecessary LLM calls
**Quality**: Rubric-based evaluation provides consistent, measurable scoring
**Transparency**: Justifications explain why each test case is prioritized
**Scalability**: Works efficiently with 10 or 1000+ test cases
**Adaptability**: Custom rubrics adapt to any type of testing concern

### Agent State Management

The agent maintains its workflow state using a structured `TestAgentState` that tracks progress through each processing step:

```python
class TestAgentState(TypedDict):
    query:                     str                           # User's natural language query
    test_cases:                List[Dict[str,Any]]          # Input test cases to be prioritized
    clusters:                  Optional[List[Dict[str,Any]]] # Semantic clusters (if clustering applied)
    relevant_clusters:         Optional[List[int]]          # Selected cluster IDs for the query
    rubric:                    List[Dict[str,Any]]          # Custom evaluation criteria
    evaluated_test_cases:      List[Dict[str,Any]]          # Test cases with scores and justifications
    sorted_test_cases:         List[Dict[str,Any]]          # Final prioritized list
```

This state flows through each node, with each step adding or refining information until the final prioritized test cases are produced.

### Intelligent Clustering Threshold

The agent uses a **25 test case threshold** for clustering decisions:
- **≤ 25 test cases**: No clustering applied - direct evaluation is efficient enough
- **> 25 test cases**: Semantic clustering activated to group related tests and reduce processing overhead

This threshold optimizes the balance between processing efficiency and LLM API costs, ensuring clustering only occurs when it provides meaningful benefits.

## Usage Options

### Option 1: Web UI (Recommended)

The Flask web interface provides an easy way to interact with the AI agent through your browser.

**1. Start the Flask server:**
```bash
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

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables** by creating a `.env` file in the project root:
```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Langfuse tracing (if you want web-based monitoring)
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
LANGFUSE_HOST=https://cloud.langfuse.com
```

**Required Environment Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key for LLM integration *(Required)*

**Optional Environment Variables (Langfuse Tracing):**
- `LANGFUSE_SECRET_KEY`: Langfuse secret key for web-based tracing and monitoring
- `LANGFUSE_PUBLIC_KEY`: Langfuse public key for web-based tracing and monitoring  
- `LANGFUSE_HOST`: Langfuse host URL (typically https://cloud.langfuse.com)

> **Note:** Langfuse is **not mandatory**. The agent has extensive CLI logging implemented, so you can trace and monitor the agent execution through console output without Langfuse. If you want to use Langfuse's web-based monitoring, you'll need to create a [Langfuse account](https://langfuse.com) first to get your API keys.

**Optional: Virtual Environment**
If you prefer to use a virtual environment (recommended for isolation):
```bash
python -m venv your-env-name
source your-env-name/bin/activate  # On Windows: your-env-name\Scripts\activate
pip install -r requirements.txt
```
