import logging
from langchain_core.messages import HumanMessage, SystemMessage
from src.api.llm_client import model
from src.utils.parse_llm import parse_llm_json_response
from src.core.state import TestAgentState

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_rubric(state: TestAgentState):
    logger.info("--- STARTING CREATE_RUBRIC NODE ---")
    
    query = state["query"]
    logger.info(f"Creating rubric for query: '{query}'")

    system_prompt = """
            You are a test rubric generation assistant.

            Your task is to create a test prioritization rubric based on a user-provided query and context.

            The rubric should contain dimentions that are most relevant for prioritizing tests in the given scenario.

            For each dimension:
            1. Provide a clear and concise name
            2. Write a description of what this dimension measures
            3. Assign a weight from 1 to 5 (where 5 indicates highest importance)
            4. Define scoring criteria for values 0 through 5 (what each score level means)
            
            Ensure that the rubric addresses key considerations such as:
            - Functional relevance to the query's focus area
            - Risk factors (e.g., security, data integrity)
            - Business impact of potential failures
            - Technical complexity or dependencies

            Output a clean JSON object with the following structure:

            {
            "rubric": [
                {
                "id": unique id per dimension
                "name": "DIMENSION_NAME",
                "description": "What this dimension evaluates",
                "weight": 1-5,
                "scoring_criteria": {
                    "0": "Description of what score 0 means",
                    "1": "Description of what score 1 means",
                    ...
                    "5": "Description of what score 5 means"
                }
                },
                ...more dimensions...
            ]
            }

            here is an example output to understand the format :

            {
            "rubric": [
                {
                "id": "1",
                "name": "API Coverage",
                "description": "How directly the test verifies the payment API functionality",
                "weight": 5,
                "scoring_criteria": {
                    "5": "Directly tests core payment API endpoints with various scenarios",
                    "4": "Tests payment API but not comprehensively",
                    "3": "Tests features that use payment API indirectly",
                    "2": "Related to payment flow but not the API",
                    "1": "Minimally related to payments",
                    "0": "Unrelated to payment processing"
                }
                },
                // More dimensions...
            ]
            }
        """

    user_prompt = f"""
            Create a test prioritization rubric based on this query:
            {query}
    """
  
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        logger.info("Calling LLM to create rubric...")
        response = model.invoke(messages)
        parsed_response = parse_llm_json_response(response.content)
        
        rubric_dimensions = len(parsed_response.get("rubric", []))
        logger.info(f"Successfully created rubric with {rubric_dimensions} dimensions")
        logger.info("--- COMPLETED CREATE_RUBRIC NODE ---")
        
        return {"rubric": parsed_response["rubric"]}
    
    except Exception as e:
        logger.error(f"ERROR in create_rubric: {str(e)}")
        raise

  