from typing import TypedDict, List, Dict, Any, Optional

class TestAgentState(TypedDict):
  query:                     str
  test_cases:                List[Dict[str,Any]]
  clusters:                  Optional[List[Dict[str,Any]]]
  relevant_clusters:         Optional[List[int]]
  rubric:                    List[Dict[str,Any]]
  evaluated_test_cases:      List[Dict[str,Any]]
  sorted_test_cases:         List[Dict[str,Any]]