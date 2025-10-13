## LangGraph-Agents Starter Branch

This is a custom branch forked from [kXborg/Agents](https://github.com/kXborg/Agents).

---

## What’s Included?

- **4 beginner-level scripts** that illustrate core LangGraph concepts: *states, tools, nodes*  
- **2 end-to-end agentic applications**.
- Minimal illustrative code along with real-world agent examples.  
---

## Repository Structure

Here’s a suggested structure:
```
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
```
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

These articles help explain the logic behind the advanced agents and are good companion reading.

------

## Contribute / Extend

- Add new **agent examples** (e.g. agents for data analysis, file operations, web scraping).
- Add tests / example notebooks with visualizations and flow-diagrams.
