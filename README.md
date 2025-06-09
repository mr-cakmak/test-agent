
# Folder Structure : 

src/
├── nodes/
│   ├── clustering_node.py
│   └── analysis_node.py
├── utils/
│   ├── clustering/
│   │   ├── parsers.py
│   │   └── validators.py
│   ├── rubric/
│   │   ├── scorers.py
│   │   └── calculators.py
│   └── shared/
│       └── file_utils.py
├── api/
│   ├── openai_client.py
│   └── external_apis.py
└── core/
    ├── graph.py
    ├── state.py
    └── config.py