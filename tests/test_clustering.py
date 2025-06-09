from src.nodes.create_clusters import create_clusters
from src.api.tc_file import nl_test_cases
from src.core.state import TestAgentState


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


state = create_initial_test_state("trial")
state["test_cases"] = nl_test_cases

# Capture the returned state update and merge it with the existing state
state_update = create_clusters(state)
state.update(state_update)

print(state["clusters"])
