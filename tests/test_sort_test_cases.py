from src.core.state import TestAgentState
from src.nodes.create_rubric import create_rubric
from src.api.tc_file import nl_test_cases
from src.nodes.sort_test_cases import sort_test_cases
from src.nodes.evaluate_test_cases import evaluate_test_cases


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
state["test_cases"] = nl_test_cases

# Capture the returned state updates and merge them with the existing state
state_update = create_rubric(state)
state.update(state_update)

state_update = evaluate_test_cases(state)
state.update(state_update)

state_update = evaluate_test_cases(state)
state.update(state_update)

state_update = sort_test_cases(state)
state.update(state_update)

print("SORTED IN STATE : ")
print(state["sorted_test_cases"])

