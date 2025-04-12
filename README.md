# UMHackathon 2025 - CommitThis: Grab Voice AI Chat

*   **Theme**: Economic empowerment through AI (from Grab's vision + AI)
*   **Group Name**: CommitThis
*   [**Presentation Slides**](https://www.canva.com/design/DAGkXBa41B0/trNP6qixFYITy1mW9XGaSg/edit?utm_content=DAGkXBa41B0&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) - Demo Video Included

## 🔍 Problem Statement

While waiting at traffic signals, Grab drivers are often required to simultaneously monitor new ride requests, fare information, real-time traffic conditions, and market opportunities at the destination. This multitasking can significantly increase the risk of driver distraction and compromise road safety.

**Objective**: To build a robust voice interaction system that enables reliable driver–assistant communication in challenging audio environments. The solution should:

*   Maintain high accuracy in noisy conditions using noise cancellation and filtering.
*   Adapt to diverse speech patterns (regional accents, dialects, colloquialisms) using NLP.
*   Provide clear, reliable functionality even with partial audio clarity.
*   Demonstrate resilience across various environmental challenges.

## ✨ Overall Flow

1.  The driver initiates a voice recording by tapping a button on the interface.
2.  System preprocesses audio (noise reduction).
3.  Audio file sent to FastAPI backend.
4.  Backend transcribes audio using OpenAI Whisper (Python library).
5.  Backend sends transcription to Gemini AI for understanding and response generation.
6.  Gemini AI returns AI-generated text response to the backend.
7.  Backend converts text to speech using Google Text-to-Speech.
8.  Speech delivered to the frontend.
9.  Driver listens to the system's response.

## 🛠️ System Architecture

*   **Model**: Client-server
*   **Frontend**: React Native with Expo Go. Handles audio recording, sending requests (fetch/axios), and receiving/playing responses.
*   **Backend**: FastAPI (running with Uvicorn).
    *   `/transcribe`: Converts audio to text (Whisper).
    *   `/ask-chatbot`: Sends text to Gemini AI, returns response.
*   **External Services**:
    *   Gemini AI: Response generation.
    *   OpenAI Whisper: Audio processing and transcription.
    *   Google Text-to-Speech: Speech synthesis.

## 💡 Utilization & Features

The system allows drivers to interact solely through voice, minimizing distractions. Key features include:

*   **Voice-Only Interaction**: Speak and listen without diverting attention from the road.
*   **Noise Reduction & Multilingual Detection**: Ensures accurate responses in various conditions.
*   **Order Evaluation**: Provide an Order ID to retrieve relevant details.
*   **Smart Recommendation Engine**: Analyzes distance, earnings, traffic, fuel, and weather to recommend accepting or declining orders, providing insights into market opportunities.

## 🔭 Planned Improvements

*   **Advanced Audio Preprocessing**: Further enhance transcription accuracy.
*   **External API Integration**:
    *   **Waze API** (Traffic Conditions): Get real-time jam information.
    *   **OpenWeather API** (Weather): Provide weather forecasts for destinations, aiding decisions on longer trips.
*   **UI Enhancements**: Improve the graphical user interface using `styles.js`.

## 💻 Setup & Installation

### Frontend (React Native with Expo)

```bash
# Install Expo CLI if you haven't already
# npm install -g expo-cli

# Install project dependencies
npm install

# Install specific packages
npx expo install expo-av
npm install axios
npx expo install expo-speech
npx expo install @react-native-picker/picker
```

### Backend (Python/FastAPI)

```bash
# Create and activate a virtual environment (recommended)
# python -m venv venv
# source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install Python dependencies
pip install fastapi uvicorn openai pydub requests python-dotenv

# Install Whisper (latest from GitHub)
pip install git+https://github.com/openai/whisper.git
# Or install the standard package (might be older)
# pip install -U openai-whisper
```

### RNNoise Setup (Optional Noise Suppression Library)

```bash
git clone https://github.com/xiph/rnnoise.git
cd rnnoise
./autogen.sh
./configure
make
# Note: Integration into the Python backend requires additional steps (e.g., using CFFI or ctypes).
cd ..
```

### FFmpeg Setup (Required by PyDub/Whisper)

*   **Windows (using MSYS2 UCRT64 environment)**:
    ```bash
    pacman -S mingw-w64-ucrt-x86_64-ffmpeg
    ```
*   **Windows (using MSYS2 MINGW64 environment)**:
    ```bash
    pacman -S mingw-w64-x86_64-ffmpeg
    ```
*   **Windows (using MSYS2 MINGW32 environment)**:
    ```bash
    pacman -S mingw-w64-i686-ffmpeg
    ```
*   **macOS (using Homebrew)**:
    ```bash
    brew install ffmpeg
    ```
*   **Linux (Debian/Ubuntu)**:
    ```bash
    sudo apt update && sudo apt install ffmpeg
    ```

*Ensure FFmpeg is added to your system's PATH or accessible by the application.*

## ▶️ Running the Application

### 1. Start the Backend Server

Navigate to the backend directory:

```bash
# Assuming your FastAPI app instance is in Server/server.py as 'app'
uvicorn Server.server:app --host 0.0.0.0 --reload
# OR
# python -m uvicorn Server.server:app --host 0.0.0.0 --reload
```

### 2. Start the Frontend Application

Navigate to the frontend directory (root of the Expo project):

```bash
npx expo start
```

Follow the instructions in the terminal to open the app in Expo Go, an emulator, or a development build.
