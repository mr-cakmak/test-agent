import logging
from langchain_core.messages import HumanMessage, SystemMessage
from src.api.llm_client import model
from src.utils.parse_llm import parse_llm_json_response
from src.core.state import TestAgentState

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def evaluate_test_cases(state: TestAgentState):
    logger.info("📊 STARTING EVALUATE_TEST_CASES NODE")
    
    rubric = state["rubric"]
    
    evaluated_tc_num = len(state["evaluated_test_cases"])
    tc_num = len(state["test_cases"])
    last_idx = min(evaluated_tc_num + 5, tc_num)

    test_cases_to_evaluate = state["test_cases"][evaluated_tc_num : last_idx]

    logger.info(f"📋 Evaluating test cases {evaluated_tc_num + 1} to {last_idx} out of {tc_num} total")
    logger.info(f"🎯 Using rubric with {len(rubric)} dimensions")

    system_prompt = """
    You are a test case scoring assistant.

            Your task is to evaluate multiple test cases against a predefined prioritization rubric.

            Scoring Instructions:
            For each test case, and for each dimension in the rubric:
            1. Analyze how the test case aligns with the dimension
            2. Assign a raw score from 0 to 5, based on the rubric's scoring criteria
            3. Provide a concise justification for the score

            Then calculate for each test case:
            - Weighted score for each dimension (raw score × weight)
            - Total weighted score (sum of all weighted scores)
            - Normalized score: total weighted score / maximum possible weighted score

            After scoring each test case:
            - Provide a 2–3 sentence explanation summarizing why this test case received its priority level, especially in relation to the user's original query and context.

            Output:
            Return a clean JSON array with one object per test case. Each object should have the following structure:

            [
              {
                "test_name": "NAME_FROM_TEST_CASE",
                "overall_score": TOTAL_WEIGHTED_SCORE,
                "normalized_score": NORMALIZED_SCORE,
                "dimension_scores": [
                  {
                    "dimension_id": "1",
                    "name": "DIMENSION_NAME",
                    "raw_score": 0-5,
                    "weighted_score": raw_score × weight,
                    "justification": "Brief explanation for this score"
                  },
                  ...
                ],
                "explanation": "Short summary of why this test received its priority level"
              },
              ... more test case evaluations ...
            ]

            You will be provided:
            - Multiple test cases (up to 5 test cases as JSON)
            - A prioritization rubric (as a list of dimension objects, each with name, description, weight, and scoring criteria)

            Use only the provided data. Do not generate anything beyond the expected JSON output.
        """


    user_prompt = f"""
            Score these test cases against the prioritization rubric.

            Test Cases:
            {test_cases_to_evaluate}

            Rubric:
            {rubric}
        """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        logger.info("🤖 Calling LLM to evaluate test cases...")
        response = model.invoke(messages)
        parsed_response = parse_llm_json_response(response.content)
        
        logger.info(f"✅ Successfully evaluated {len(parsed_response)} test cases")
        logger.info("🏁 COMPLETED EVALUATE_TEST_CASES NODE")
        
        return {"evaluated_test_cases" : state["evaluated_test_cases"] + parsed_response}
    
    except Exception as e:
        logger.error(f"❌ Error in evaluate_test_cases: {str(e)}")
        raise