import logging
from src.core.state import TestAgentState
from langgraph.graph import StateGraph, START, END
from src.nodes import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

agent_graph = StateGraph(TestAgentState)

agent_graph.add_node("create_clusters", create_clusters)
agent_graph.add_node("create_rubric", create_rubric)
agent_graph.add_node("evaluate_test_cases", evaluate_test_cases)
agent_graph.add_node("pick_relevant_clusters", pick_relevant_clusters)
agent_graph.add_node("sort_test_cases", sort_test_cases)



def is_clustering_needed(state: TestAgentState):
    number_of_tc = len(state["test_cases"])
    logger.info(f"🔍 Checking if clustering is needed for {number_of_tc} test cases")
    
    if number_of_tc > 50:
        logger.info("✅ Clustering is needed (>50 test cases)")
        return "clustering_is_needed"
    else:
        logger.info("⏭️  Clustering not needed (≤50 test cases)")
        return "clustering_is_not_needed"

def are_all_tc_evaluated(state: TestAgentState):
    num_evaluated_tc = len(state["evaluated_test_cases"])
    num_tc = len(state["test_cases"])
    
    logger.info(f"🔍 Checking evaluation progress: {num_evaluated_tc}/{num_tc} test cases evaluated")

    if num_evaluated_tc < num_tc:
        logger.info("⏩ Continue evaluation - not all test cases evaluated yet")
        return "not_all_evaluated"
    else:
        logger.info("✅ All test cases evaluated - proceeding to sort")
        return "all_evaluated"



agent_graph.add_conditional_edges(
    START,
    is_clustering_needed,
    {
        "clustering_is_needed": "create_clusters",
        "clustering_is_not_needed": "create_rubric"
    }                         
)

agent_graph.add_edge("create_clusters", "pick_relevant_clusters")
agent_graph.add_edge("pick_relevant_clusters", "create_rubric")
agent_graph.add_edge("create_rubric", "evaluate_test_cases")

agent_graph.add_conditional_edges(
    "evaluate_test_cases",
    are_all_tc_evaluated,
    {
        "not_all_evaluated" : "evaluate_test_cases",
        "all_evaluated" : "sort_test_cases"
    }
)

agent_graph.add_edge("sort_test_cases", END)

compiled_graph = agent_graph.compile()