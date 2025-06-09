from src.nodes.evaluate_test_cases import evaluate_test_cases
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
state["rubric"] = [{'id': '1', 'name': 'API Endpoint Functionality', 'description': "Evaluates how well the test covers the updated payment API endpoints' functionality.", 'weight': 5, 'scoring_criteria': {'0': 'Does not test any payment API endpoints.', '1': 'Tests unrelated API endpoints.', '2': 'Tests related API endpoints but not the updated ones.', '3': 'Tests some of the updated payment API endpoints.', '4': 'Tests most of the updated payment API endpoints.', '5': 'Comprehensively tests all updated payment API endpoints.'}}, {'id': '2', 'name': 'Security and Data Integrity', 'description': "Assesses the test's ability to identify security vulnerabilities and ensure data integrity in the payment API.", 'weight': 5, 'scoring_criteria': {'0': 'Does not address security or data integrity.', '1': 'Minimally addresses security or data integrity.', '2': 'Covers basic security or data integrity checks.', '3': 'Includes moderate security and data integrity checks.', '4': 'Covers extensive security and data integrity checks.', '5': 'Thoroughly tests for security vulnerabilities and data integrity issues.'}}, {'id': '3', 'name': 'Business Impact', 'description': 'Measures the potential business impact of failures in the payment API.', 'weight': 4, 'scoring_criteria': {'0': 'No impact on business operations.', '1': 'Minimal impact on business operations.', '2': 'Minor impact on business operations.', '3': 'Moderate impact on business operations.', '4': 'Significant impact on business operations.', '5': 'Critical impact on business operations.'}}, {'id': '4', 'name': 'Technical Complexity', 'description': 'Evaluates the complexity of the test in terms of technical implementation and dependencies.', 'weight': 3, 'scoring_criteria': {'0': 'No technical complexity or dependencies.', '1': 'Minimal technical complexity or dependencies.', '2': 'Some technical complexity or dependencies.', '3': 'Moderate technical complexity or dependencies.', '4': 'High technical complexity or dependencies.', '5': 'Very high technical complexity or dependencies.'}}, {'id': '5', 'name': 'Regression Coverage', 'description': "Assesses the test's ability to ensure that existing functionalities are not broken by the API updates.", 'weight': 4, 'scoring_criteria': {'0': 'Does not cover regression testing.', '1': 'Minimal regression coverage.', '2': 'Covers some regression scenarios.', '3': 'Covers most regression scenarios.', '4': 'Extensive regression coverage.', '5': 'Comprehensive regression coverage ensuring no existing functionalities are broken.'}}]

# Capture the returned state updates and merge them with the existing state
state_update = evaluate_test_cases(state)
state.update(state_update)
print(state["evaluated_test_cases"])
print(len(state["evaluated_test_cases"]))

print("------------------------------------------------------------")

state_update = evaluate_test_cases(state)
state.update(state_update)
print(state["evaluated_test_cases"])
print(len(state["evaluated_test_cases"]))

