# LangGraph-Agents Starter Branch

This is a custom branch forked from [kXborg/Agents](https://github.com/kXborg/Agents).

It’s tailored for learners and practitioners who want to build agents using **LangGraph**, with clear, minimal examples and two in-depth advanced agent scripts.

---

## What’s the Goal?

- Provide **4 beginner-level scripts** that illustrate core LangGraph concepts: *states, tools, nodes*  
- Provide **2 advanced agent scripts** based on published tutorials:
  1. *Building a Visual Web Browser Agent* (using screenshots, scroll logic, summarization) :contentReference[oaicite:1]{index=1}  
  2. *Self-Correcting Agent / Code Generation Agent* (as per LearnOpenCV article)  
- Serve as a learning ladder: from minimal illustrative code to more complete, real-world agent examples  
- Make it easier for newcomers to get started with LangGraph without being overwhelmed by a large, monolithic repo  

---

## Repository Structure

Here’s a suggested structure:

├── README.md
├── requirements.txt
├── scripts
│   ├── browser_automation.py
│   ├── self_code_correction.py
│   └── whatsapp_msg_automation.py
└── starting_with_langgraph
    ├── langGraph-101.py
    ├── langGraph-102.py
    ├── langGraph-103.py
    └── langGraph-104.py

- **starting_with_langGraph/**: minimal examples each focusing on one LangGraph concept  
- **scripts/**: full agents implementing the logic from the LearnOpenCV tutorials  
- **requirements.txt**: the Python dependencies (langchain, langgraph, playwright, etc.)

---

## Getting Started

### Prerequisites

- System Requirement: 

  - Debian 12 / 13, Ubuntu 22.04 / 24.04 (x86-64 or arm64).
  - Windows 10+, Windows Server 2016+ or Windows Subsystem for Linux (WSL).
  - macOS 14 (Ventura) or later.
- Python 3.10+
- Install dependencies:

  ```bash
  pip install -r requirements.txt

* For browser-based agent -> Install Playwright browser binaries:

  * ```bash
    playwright install
    ```

* Create a `.env` file and provide any required API keys by creating environment variables, e.g. GOOGLE_API_KEY.

* Running the beginner scripts

  * Each script in `starting_with_langgraph/` is independent and demonstrates a specific LangGraph concept.

------

## Background & References

- *Building an Agentic Browser with LangGraph: A Visual Automation & Summarization Pipeline*: [LearnOpenCV](https://learnopencv.com/langgraph-building-a-visual-web-browser-agent/).
- *LangGraph Self-Correcting Agent / Code Generation*: [LearnOpenCV](https://learnopencv.com/langgraph-self-correcting-agent-code-generation/)
- Original upstream repo: [kXborg/Agents](https://github.com/kXborg/Agents?utm_source=chatgpt.com) [GitHub](https://github.com/kXborg/Agents)

These articles help explain the logic behind the advanced agents and are good companion reading.

------

## Contribute / Extend

- Add new **agent examples** (e.g. agents for data analysis, file operations, web scraping).
- Add tests / example notebooks with visualizations and flow-diagrams.
