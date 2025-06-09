import logging
from src.core.graph import compiled_graph
from src.core.state import TestAgentState
from src.api.tc_file import nl_test_cases
from langfuse.langchain import CallbackHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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


def main():
    logger.info("--- STARTING TEST AGENT ---")

    # Initialize Langfuse CallbackHandler for LangGraph/Langchain (tracing)
    langfuse_handler = CallbackHandler()

    # create an initial state
    query = "We updated the URL generation algorithm. What should we test?"
    logger.info(f"Initial query: '{query}'")
    
    initial_state = create_initial_test_state(query)
    initial_state["test_cases"] = nl_test_cases
    
    logger.info(f"Loaded {len(nl_test_cases)} test cases")

    compiled_graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
    
    # run the agent
    logger.info("Starting graph execution...")
    result = compiled_graph.invoke(
        input=initial_state,
        config={"callbacks": [langfuse_handler]}
    )
    
    logger.info("--- AGENT EXECUTION COMPLETED ---")
    logger.info(f"Final result: {len(result.get('sorted_test_cases', []))} test cases prioritized")


if __name__ == "__main__":
    main()

main()