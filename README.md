# GUVI_HCL_TASK15_DataDriven-KeywordDrivenTestingFramework_May2026
GUVI HCL TASK 15 - Data Driven & Keyword Driven Testing Framework

The current repository contains python codes to the questions mentioned in HCL GUVI Python Task 15 - https://docs.google.com/document/d/1wF0eKJ2PhUNJoVQAIPOQHFfsdmIqhAxjNYn9tQrolGo/edit?tab=t.0

==================================================================================================================

POM Project Structure 
----------------------
OrangeHRM_Automation_Framework/
│
├── config/
│   └── config.json
│
├── data/
│   └── login_test_data.xlsx
│
├── drivers/
│   └── driver_factory.py
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── dashboard_page.py
│
├── tests/
│   └── test_login_ddtf.py
│
├── utils/
│   ├── logger.py
│   ├── config_reader.py
│   └── excel_utils.py 
│
├── reports/
│   ├── html/
│   └── screenshots/     (auto-generated on failure)
│
├── logs/
│   └── framework logs (.log files)
│
├── screenshots/
│   └── failure screenshots
│
├── conftest.py
├── requirements.txt
├── pytest.ini
└── README.md
