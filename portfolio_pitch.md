# Friday AI: Portfolio Strategy 💼

## Repository
[**View Source Code on GitHub**](https://github.com/Andalexskywalker/jarvis-like.git)

## The Pitch
"Friday is an **Autonomous OS Orchestrator** that bridges the gap between Large Language Models and local system environments. Unlike standard chatbots, Friday utilizes a **Dynamic Tool Registry** and a **Self-Healing API Client** to execute real-world tasks (Media, File System, System Stats) on a Windows environment."

## Top 3 Technical Highlights (Interview Talk)
1.  **Dynamic Introspection Tooling**: Built a registry that uses Python's `inspect` module to automatically map LLM JSON outputs to local function signatures. This makes the system infinitely extensible with zero hard-coding of argument mapping.
2.  **Thread-Safe COM Integration**: Solved complex Windows threading issues (PyCaw/TTS) using `CoInitialize` within background worker threads, ensuring stability in a "headless" background environment.
3.  **Self-Healing Client Pattern**: Designed a resilient API client that dynamically probes for working model versions and implements exponential backoff for rate-limiting, making the agent "production-ready" despite API instability.

## Framing the "Friday" Persona
If asked why a feminine persona or why "Friday
- "It's an exploration in **Human-Computer Interaction (HCI)**. I wanted to see how a proactive assistant (instead of a reactive one) changes the user experience in a desktop environment."
- "The personification allows for clearer feedback loops (voice synthesis), making the 'headless' nature of the background process intuitive for the user."

## Future Roadmap (Shows growth mindset)
- Implementation of **Computer Vision** (OpenCV/Vision LLM) for screen-aware reasoning.
- **Native Windows Toast** integration for non-intrusive background alerting.
- **RAG (Retrieval Augmented Generation)** for local file indexing and intelligent search.
