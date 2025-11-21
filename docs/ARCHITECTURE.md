# Pac-Man AI Agent Architecture

## 1. Core Design Decisions

### Screen Capture vs. Webcam
**Decision:** Direct Screen Capture (preferred).
**Reasoning:**
- **Latency & Frame Rate:** Direct capture (e.g., via `mss`) is significantly faster and has lower latency than processing a webcam feed.
- **Fidelity:** Screen capture provides pixel-perfect data, avoiding issues with glare, perspective distortion, and lighting changes that plague webcam computer vision.
- **Reliability:** It removes external physical variables (camera position, room lighting).

### Local CV vs. Cloud AI (Gemini)
**Decision:** Hybrid approach.
- **Local CV (OpenCV/ML):** Handles the high-frequency control loop (30 FPS). It performs immediate tasks: sprite detection, grid mapping, and collision avoidance. It must be fast and deterministic.
- **Cloud AI (Gemini):** Acts as a "Coach" or "Strategist". It runs asynchronously (e.g., every few seconds or on demand) to analyze the broader game state, suggest heuristic tuning, or provide high-level strategy (e.g., "Focus on the bottom-left quadrant"). It is NOT in the critical path for frame-by-frame movement.

### Main Control Loop
The architecture follows a classic robotics sense-plan-act cycle:
1.  **Capture:** Grab the latest frame from the OS window manager.
2.  **Perception (Vision):**
    - Crop to game region.
    - Detect entities (Pac-Man, Ghosts, Pellets).
    - Update the internal World Model (Grid/Graph).
3.  **Reasoning (Agent):**
    - Update pathfinding costs (e.g., ghost proximity).
    - Select the next best action (Policy).
4.  **Action (Control):**
    - Send keyboard input to the OS.
5.  **Feedback/Logging:**
    - Log state for debugging or async sending to Gemini.

## 2. Module Responsibilities

- **`capture/`**: Abstraction for getting image data.
- **`vision/`**: Image processing. Converts pixels -> structured data (positions, types).
- **`agent/`**: Brains. Converts structured data -> decisions (UP/DOWN/LEFT/RIGHT).
- **`control/`**: Actuators. Converts decisions -> OS events.
- **`ai_google/`**: High-level intelligence. Interface to Gemini.

## 3. Future Extensibility
- The `Agent` class structure allows swapping `SimpleHeuristicAgent` with `RLAgent` without changing the vision or control pipelines.
- The `StateEstimator` decouples the raw pixels from the agent's understanding, allowing us to switch from Template Matching to a CNN detector without breaking the agent logic.
