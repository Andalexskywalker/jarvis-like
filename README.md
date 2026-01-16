# Friday AI 👩‍💻
> *A self-healing, intelligent desktop agent powered by Google Gemini.*

Friday is not just a chatbot. She is an **Autonomous Agent** capable of executing Python skills on your local machine. She understands context, manages her own API connectivity (Self-Healing Client), and interacts with the OS to automate tasks.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![AI](https://img.shields.io/badge/AI-Gemini_2.5-flash-orange.svg)
![Architecture](https://img.shields.io/badge/Architecture-Function_Calling-purple.svg)

## 🧠 Architecture
This project demonstrates modern **AI Engineering** patterns:

1.  **Orchestrator (`agent.py`)**: The reasoning loop. It maintains context and decides *which* tool to call based on user intent.
2.  **Dynamic Registry (`tools_registry.py`)**: A scalable plugin system. Tools are defined with typed schemas, allowing the LLM to understand how to use them (Function Calling).
3.  **Self-Healing Client (`llm_client.py`)**: A custom zero-dependency wrapper for the Gemini API that:
    *   Dynamically probes endpoints to find the fastest available model (Flash vs Pro).
    *   Handles Rate Limits (`429`) with exponential backoff.
    *   Prevents `404` errors by validating model versions on startup.

```mermaid
graph TD
    User([User]) <--> CLI[Terminal / UI]
    CLI <--> Agent[Agent Orchestrator]
    
    subgraph Brain ["🧠 Brain (LLM Client)"]
        Agent <--> LLM[Gemini API Wrapper]
        LLM -- "Self-Healing" --> Model{Model Selector}
        Model -- "Rate Limit Retry" --> Google[Google Gemini]
    end
    
    subgraph Body ["🛠️ Tools Registry"]
        Agent -- "Function Call" --> Registry[Tools Registry]
        Registry --> Skills
        
        subgraph Skills ["Hands (Skills)"]
            Media[Media Control]
            Files[File Organizer]
            System[OS Utils]
        end
    end
```

## 🛠️ Skills
Friday has "hands" to control your PC:
*   **🎵 Media**: Control volume, mute audio, and play music on YouTube.
*   **📂 Organizer**: Automatically scan Desktop and file downloads into categorized folders (Images, Docs, Installers).
*   **⚡ Automation**: Set timers, reminders, and launch applications.
*   **🌦️ Real-time**: Check weather and date.

## 🚀 Quick Start

### 1. Setup
```bash
# Clone and install dependencies
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. API Key
Create a `.env` file with your Google Gemini Key (Free Tier):
```ini
GEMINI_API_KEY=AIzaSy...
```

### 3. Run
```bash
python main.py
```
*Note: Friday will automatically detect the best model version for your key.*

## 📸 Example Usage
> **User**: "Friday, it's messy here. Clean up my desktop."  
> **Friday**: *Scans desktop, moves 12 files to 'Images' and 'Documents' folders.*  
> **Friday**: "Done! I organized 12 files for you."

> **User**: "Play some Lo-Fi beats and set volume to 30%."  
> **Friday**: *Sets volume to 30, opens YouTube.*

---
*Built as a portfolio showcase of AI Agent architecture.*
