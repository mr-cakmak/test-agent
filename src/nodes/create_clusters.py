import logging
from langchain_core.messages import HumanMessage, SystemMessage
from src.api.llm_client import model
from src.utils.parse_llm import parse_llm_json_response
from src.core.state import TestAgentState

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_clusters(state: TestAgentState):
    logger.info("🔧 STARTING CREATE_CLUSTERS NODE")
    
    test_cases = state["test_cases"]
    logger.info(f"📊 Processing {len(test_cases)} test cases for clustering")

    system_prompt = """
            You are a test case clustering assistant.

            Your job is to analyze test cases and group them into semantic clusters. Each cluster should group test cases that verify similar functionality or components.

            For each cluster:
            1. Give a descriptive name
            2. Write a brief description of what the tests cover
            3. Include a list of relevant keywords
            4. List the "id" values of the test cases in that cluster

            Rules:
            - Use test names, file paths, summaries, and steps to determine similarity
            - Each test case must belong to exactly one cluster
            - Output must be a clean JSON object only

            Format:
            {
            "clusters": [
                {
                "cluster_id": 1,
                "name": "CLUSTER_NAME",
                "description": "DESCRIPTION",
                "test_ids": [ID1, ID2],
                "keywords": ["KEYWORD1", "KEYWORD2"]
                },
                ...
            ]
            }

      """

    user_prompt = f"""
          Analyze the following test cases and group them into semantic clusters.
            {test_cases}
    """

        
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        logger.info("🤖 Calling LLM to create clusters...")
        response = model.invoke(messages)
        clusters_dict = parse_llm_json_response(response.content)
        
        num_clusters = len(clusters_dict.get("clusters", []))
        logger.info(f"✅ Successfully created {num_clusters} clusters")
        logger.info("🏁 COMPLETED CREATE_CLUSTERS NODE")
        
        return {"clusters" : clusters_dict}
    
    except Exception as e:
        logger.error(f"❌ Error in create_clusters: {str(e)}")
        raise
