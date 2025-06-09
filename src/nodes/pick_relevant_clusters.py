import logging
from langchain_core.messages import HumanMessage, SystemMessage
from src.api.llm_client import model
from src.utils.parse_llm import parse_llm_json_response
from src.core.state import TestAgentState

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def pick_relevant_clusters(state: TestAgentState):
    logger.info("--- STARTING PICK_RELEVANT_CLUSTERS NODE ---")
    
    clusters = state["clusters"]
    query = state["query"]
    
    total_clusters = len(clusters.get("clusters", []))
    logger.info(f"Analyzing {total_clusters} clusters for relevance to query: '{query}'")

    system_prompt = """
      You are a Test Case Cluster Relevance Analyzer. Your role is to efficiently identify which test case clusters are most relevant to a user's testing query, thereby optimizing computational resources by eliminating irrelevant test cases from evaluation.

    ## Your Responsibilities:
    1. Analyze user queries to understand their testing intent, context, and scope
    2. Evaluate test case clusters against the query to determine relevance
    3. Select only the clusters that contain test cases likely to address the user's needs
    4. Provide clear reasoning for your selections to ensure transparency

    ## Decision Guidelines:
    - **High Relevance**: Clusters directly related to the query's main focus (e.g., "payment tests" for payment-related queries)
    - **Medium Relevance**: Clusters that might be indirectly affected or provide supporting evidence
    - **Low/No Relevance**: Clusters unrelated to the query's scope or intent

    ## Key Considerations:
    - Consider both direct matches (keywords, domain) and indirect relationships (dependencies, integrations)
    - Account for different query types: feature testing, security validation, performance checks, bug investigation, etc.
    - Balance thoroughness with efficiency - include enough clusters to be comprehensive but exclude clearly irrelevant ones
    - When in doubt about relevance, lean toward inclusion rather than exclusion to avoid missing important test cases

    ## Output Requirements:
    - Return a clean JSON object with no additional text before or after
    - Include selected cluster IDs and brief justifications
    - Maintain consistency in reasoning quality across all selections

    ## Quality Standards:
    - Selections should be defensible and logical
    - Reasoning should be concise but informative
    - Coverage should be appropriate for the query scope
    - Avoid both over-inclusion (too many irrelevant clusters) and under-inclusion (missing relevant clusters)
    """

    user_prompt = f"""
    Analyze the following user query and select the most relevant test case clusters for evaluation.

    User Query: "{query}"

    Available Clusters:
    {clusters}

    Instructions:
    1. Determine the main focus and intent of the user query
    2. Evaluate each cluster's relevance to this focus
    3. Select clusters that are highly or moderately relevant
    4. Exclude clusters that are clearly unrelated to the query

    For each selected cluster, provide a brief justification explaining why it's relevant to the user's query.

    Output Format in JSON:

    {{
      "selected_clusters": [
        {{
          "cluster_id": "cluster_id_here",
          "relevance_level": "high|medium", 
          "justification": "Brief explanation of why this cluster is relevant to the query"
        }}
      ],
      "excluded_count": number_of_excluded_clusters,
      "selection_summary": "Brief summary of the overall selection strategy for this query"
    }}

    Return only the JSON object with no additional text.
  
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        logger.info("Calling LLM to pick relevant clusters...")
        response = model.invoke(messages)
        res = parse_llm_json_response(response.content)
        
        selected_count = len(res.get("selected_clusters", []))
        excluded_count = res.get("excluded_count", 0)
        logger.info(f"Selected {selected_count} relevant clusters, excluded {excluded_count}")
        logger.info("--- COMPLETED PICK_RELEVANT_CLUSTERS NODE ---")
        
        return {"relevant_clusters" : res["selected_clusters"]}
    
    except Exception as e:
        logger.error(f"ERROR in pick_relevant_clusters: {str(e)}")
        raise