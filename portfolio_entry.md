# Portfolio Entry: Friday AI

**Title:** Friday AI - Autonomous Desktop Agent
**Role:** Backend / AI Engineer
**Tech Stack:** Python, Google Gemini API, SQLite, Function Calling

## 🚀 The Pitch
Friday is not just a chatbot—it's an **autonomous agent** that lives on my desktop. Unlike standard LLM wrappers, Friday possesses "hands" (Python functions) to interact with the Operating System, allowing it to organize files, control media, and manage tasks autonomously based on natural language commands.

## 💡 Key Features
-   **Autonomous Tool Execution:** Uses LLM Function Calling to decide *when* and *how* to use local tools (e.g., `media.play`, `files.organize`).
-   **Self-Healing Connectivity:** Implements a custom `LLMClient` that automatically probes for available Gemini models, handles 429 Rate Limits with exponential backoff, and switches between "Flash" and "Pro" models based on availability.
-   **Dynamic Plugin System:** Tools are registered via a scalable `ToolsRegistry` pattern, allowing new skills to be added without modifying the core agent logic.
-   **Robust Error Handling:** Designed to fail gracefully—if a specific skill (like Audio) breaks due to missing drivers, the agent disables just that skill and continues operating.

## 🔧 Technical Challenges Solved
One of the hardest parts was managing the **unstable nature of experimental AI APIs**.
*   **Challenge:** The `gemini-2.0-flash-exp` model would frequently hit Rate Limits (429) or become unavailable.
*   **Solution:** I built a "smart resolver" in `llm_client.py` that tests multiple models on startup. If the preferred model is rate-limited, it automatically downgrades to a stable version (`gemini-1.5-flash`) seamlessly, ensuring the user never sees a crash.

## 🔮 Future Roadmap
-   Add **Computer Vision** to let Friday "see" the screen.
-   Implement a **Voice Interface** (STT/TTS).
-   Migrate memory to **Vector Database** (ChromaDB) for long-term semantic recall.
