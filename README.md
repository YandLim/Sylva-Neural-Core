# [🧠 Sylva Neural Core](https://github.com/YandLim/Sylva-Neural-Core)
Sylva is a long-running, local-first backend service that routes voice and command input into automated system actions without relying on cloud services.


## 💥 The Problem 
Local automation often consists of small, isolated scripts executed independently. As these scripts accumulate, managing entry points, execution context, and lifecycle becomes increasingly fragmented.

This fragmentation introduces operational friction and makes automation brittle once tasks need to stay running, respond to input, or coordinate with one another.

## 🎯 Sylva's responsibilities 
Sylva acts as a centralized backend system responsible for integrating and coordinating multiple standalone automation scripts.
At a high level, the system is responsible for:
- Providing a single, stable entry point for triggering automation tasks
- Routing command input into structured modules and corresponding actions
- Managing the lifecycle of long-running automation processes
- Executing modules without requiring users to interact with individual scripts directly

The system does not perform autonomous decision-making or rely on cloud services. It executes predefined actions based on explicit input and configured automation logic.

## 🗺️ High-level Architecture 
- Runs as a persistent background service
- Accepts user input via voice or text interfaces
- Transforms raw input into structured intent data
- Routes the intent to the appropriate internal module
- Executes the module within Sylva’s controlled runtime
- Returns results as voice output or structured data

## ⚙️ Execution model 
Sylva operates as a long-running backend service rather than a one-off script.
The system is started once and remains active in the background, waiting for incoming commands. Execution is triggered by voice or text input and routed through a centralized intent processor rather than direct script invocation.

Each command is mapped to a single module execution at a time. Modules are executed within Sylva’s controlled execution context to ensure consistent lifecycle handling and output delivery.
The system follows a simple lifecycle:
- Startup: initialize input handlers, intent processor, and module registry
- Run: accept commands, execute one module per request, and return results
- Shutdown: gracefully stop active execution and release system resources

## ➕ Extending the system
Sylva is designed around a stable core with clearly defined extension points.

The core system, including input handling, intent processing, and execution flow, lives under the `core/` directory and is treated as stable. Changes to this layer are intentionally minimized to preserve system reliability and predictable behavior.

New behavior is introduced by adding modules under the `modules/` directory. Each module encapsulates its own execution logic and is registered through the intent routing layer (`core/sylva_decision.py`) without modifying the core execution loop.

This separation allows the system to evolve by adding new automation capabilities while keeping the core runtime readable, stable, and easy to reason about.

## 🚫 Out of scope
The system is not designed to function as a conversational AI or general-purpose chatbot. It does not perform open-ended reasoning or dialogue management beyond intent-based command routing.

Sylva is not a cloud-based service and does not rely on external APIs for core functionality. Remote synchronization, user accounts, and cross-device state management are considered out of scope.

The project does not focus on graphical user interfaces or frontend experiences. Any UI or client application is treated as an external consumer of the backend system.

The core system avoids advanced scheduling, complex workflows, and built-in user scripting, keeping the focus on simplicity and long-term maintainability. Developers may extend the codebase directly if needed.

## 🛠️ Current status 
The core execution model, intent routing, and module boundaries are considered stable. New automation modules and command capabilities are still evolving as the system is extended and refined.

While Sylva is not positioned as a production-ready assistant, it is intentionally built with long-term maintainability and backend system design in mind.

## ▶️ How to run
#### Requirements
- Python 3.10
- Local text to speech in linux environment
- uv as project manager. You can check uv [here](https://pypi.org/project/uv/) (recomended)
- .env with format `SERPAPI_APIKEY=your_key_here` to execute web search module

#### Run
```cmd
uv sync
uv run sylva
