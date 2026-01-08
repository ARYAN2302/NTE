# Narrative Transposition Engine (NTE)

NTE is a structured framework for reimagining classic, public-domain narratives in entirely new contexts (temporal, cultural, or technological) while preserving their original narrative integrity.

![Architecture Diagram](assets/architecture.png)

## Overview

The engine uses a 4-step pipeline to systematically transform stories:
1.  **Analyze**: Deconstructs the source material into an abstract narrative representation (themes, characters, plot beats).
2.  **Remap**: Translates the abstract components into the target world's logic using relational analogy and external world knowledge.
3.  **Generate**: Drafts a detailed narrative prose (800-1200 words) using the remapped framework.
4.  **Verify**: Performs a "Logline Lock" and "Beat Presence" check to ensure the new story hasn't drifted from its source logic.

## Project Structure

```text
NTE/
├── app.py              # Streamlit Web UI
├── run.py              # CLI Entry point
├── core.py             # Pipeline logic
├── llm_utils.py        # Gemini API wrapper
├── prompts/            # Pipeline prompt templates
├── data/               # Source stories and world knowledge
├── artifacts/          # Auto-generated intermediate steps
└── assets/             # Documentation visuals
```

## Getting Started

### Prerequisites
- Python 3.10+
- Google Gemini API Key

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/ARYAN2302/NTE.git
    cd NTE
    ```

2.  **Environment Setup**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    pip install -r requirements.txt
    ```

3.  **API Configuration**:
    Create a `.env` file in the root:
    ```text
    GOOGLE_API_KEY=your_key_here
    ```

### Usage

#### Web UI
```bash
streamlit run app.py
```

#### Command Line
```bash
python run.py
```

## Guardrails
- **No Direct Plagiarism**: Prompts are tuned to avoid verbatim quotes from source material.
- **Structural Enforcement**: The remapping agent is strictly constrained by the output of the analysis agent.
- **Integrity Validation**: Automated "critic" step flags stories that fail to maintain core character goals or plot beats.

