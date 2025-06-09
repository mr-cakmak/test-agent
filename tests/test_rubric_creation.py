from src.nodes.create_rubric import create_rubric 
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


state = create_initial_test_state("We updated the URL generation algorithm. What should we test?")

# Capture the returned state update and merge it with the existing state
state_update = create_rubric(state)
state.update(state_update)  # Merge the returned update into the state

print(state["rubric"])