import logging
from src.core.state import TestAgentState

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def sort_test_cases(state: TestAgentState):
    logger.info("--- STARTING SORT_TEST_CASES NODE ---")
    
    evaluated_test_cases = state["evaluated_test_cases"]
    logger.info(f"Sorting {len(evaluated_test_cases)} evaluated test cases by overall score")

    sorted_test_cases_desc = sorted(evaluated_test_cases, key=lambda x: x['overall_score'], reverse=True)

    logger.info("=== SORTED BY OVERALL SCORE (HIGHEST TO LOWEST) ===")
    for i, test_case in enumerate(sorted_test_cases_desc, 1):
        logger.info(f"{i}. {test_case['test_name']} - Score: {test_case['overall_score']}")
    
    logger.info("Successfully sorted test cases")
    logger.info("--- COMPLETED SORT_TEST_CASES NODE ---")
    
    return {"sorted_test_cases" : sorted_test_cases_desc}
