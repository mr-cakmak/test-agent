#!/usr/bin/env python3
"""
Simple Flask UI for the LangGraph AI Agent
"""
import json
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from src.core.graph import compiled_graph
from src.core.state import TestAgentState
from langfuse.langchain import CallbackHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

def create_initial_test_state(query: str) -> TestAgentState:
    """Helper function to create a new TestAgentState with sensible defaults"""
    return {
        "query": query,
        "test_cases": [],
        "is_clustering_needed": False,
        "clusters": None,
        "relevant_clusters": [],
        "rubric": [],
        "evaluated_test_cases": [],
        "sorted_test_cases": []
    }

def parse_test_cases(test_cases_text: str):
    """Parse test cases from text input. Expects JSON format."""
    try:
        # Try to parse as JSON first
        test_cases = json.loads(test_cases_text)
        if isinstance(test_cases, list):
            return test_cases
        else:
            return [test_cases]
    except json.JSONDecodeError:
        # If not valid JSON, treat as plain text and create a simple test case
        if test_cases_text.strip():
            return [{
                "id": "1",
                "test_name": "user_input_test",
                "summary": test_cases_text.strip(),
                "steps": [test_cases_text.strip()],
                "notes": ["User provided test case"]
            }]
        return []

@app.route('/')
def index():
    """Main page with the form"""
    return render_template('index.html')

@app.route('/run_agent', methods=['POST'])
def run_agent():
    """Process the form submission and run the AI agent"""
    try:
        query = request.form.get('query', '').strip()
        test_cases_text = request.form.get('test_cases', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        logger.info(f"Received query: '{query}'")
        logger.info(f"Received test cases: {test_cases_text[:100]}...")
        
        # Parse test cases
        test_cases = parse_test_cases(test_cases_text)
        logger.info(f"Parsed {len(test_cases)} test cases")
        
        # Create initial state
        initial_state = create_initial_test_state(query)
        initial_state["test_cases"] = test_cases
        
        # Initialize Langfuse CallbackHandler
        langfuse_handler = CallbackHandler()
        
        # Run the agent
        logger.info("Starting graph execution...")
        result = compiled_graph.invoke(
            input=initial_state,
            config={"callbacks": [langfuse_handler]}
        )
        
        logger.info("--- AGENT EXECUTION COMPLETED ---")
        final_test_cases = result.get('sorted_test_cases', [])
        logger.info(f"Final result: {len(final_test_cases)} test cases prioritized")
        
        return jsonify({
            'success': True,
            'message': f'Agent execution completed successfully. {len(final_test_cases)} test cases prioritized.',
            'result': {
                'query': result.get('query'),
                'total_test_cases': len(result.get('test_cases', [])),
                'sorted_test_cases_count': len(final_test_cases),
                'sorted_test_cases': final_test_cases[:5]  # Return first 5 for preview
            }
        })
        
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}", exc_info=True)
        return jsonify({'error': f'Error running agent: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
