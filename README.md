# Intelligent Pac-Man Agent

An autonomous AI agent designed to play Pac-Man using real-time computer vision and hybrid intelligence. This project combines local high-speed processing for immediate reflexes with cloud-based AI (Google Gemini) for high-level strategic planning.

## 🚀 Features

- **Real-time Screen Capture**: Uses `mss` for low-latency, pixel-perfect game state acquisition.
- **Computer Vision Pipeline**: 
  - Custom `MapExtractor` to build a grid representation of the game level.
  - `ObjectDetectorCV` using template matching to track Pac-Man, ghosts, and pellets.
- **Hybrid AI Architecture**:
  - **Local Agent**: Fast, deterministic policy for collision avoidance and pathfinding (30 FPS).
  - **Cloud Strategist**: Asynchronous integration with Google Gemini to analyze game state and provide strategic advice.
- **Modular Design**: Decoupled modules for Capture, Vision, Agent, and Control, allowing for easy experimentation with different algorithms (e.g., RL vs. Heuristic).

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Computer Vision**: OpenCV (`cv2`), NumPy
- **Input/Output**: `mss` (Screen Capture), `pyautogui`/`keyboard` (Control)
- **AI Integration**: Google Generative AI SDK (Gemini)

## 📂 Project Structure

```
├── agent/          # Decision making logic (Pathfinding, Policies)
├── ai_google/      # Google Gemini integration for strategic advice
├── capture/        # Screen capture implementation
├── control/        # Keyboard input simulation
├── vision/         # Computer vision pipeline (Detection, Mapping)
├── docs/           # Documentation and Architecture details
├── tools/          # Calibration and utility scripts
└── main.py         # Application entry point
```

## ⚡ Getting Started

1.  **Clone the repository**
    ```bash
    git clone https://github.com/snowholt/Inteligent-PacMan.git
    cd Inteligent-PacMan
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Ensure you have `opencv-python`, `numpy`, `mss`, `google-generativeai`, etc. installed)*

3.  **Configuration**
    - Update `config.py` with your screen region coordinates.
    - Set your Google API Key in `.env`:
      ```
      GOOGLE_API_KEY=your_api_key_here
      ```

4.  **Run the Agent**
    Open your Pac-Man game window and run:
    ```bash
    python main.py
    ```

## 🧠 Architecture

The system follows a robotic **Sense-Plan-Act** loop:
1.  **Sense**: Capture screen frame -> Detect objects -> Update World Model.
2.  **Plan**: Calculate costs -> Consult Policy/Gemini -> Determine next move.
3.  **Act**: Send keystroke to OS.

For more details, see [ARCHITECTURE.md](docs/ARCHITECTURE.md).
