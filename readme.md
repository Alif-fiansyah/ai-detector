# AI Text Detector & Academic Paraphraser

A Python-based stylistic text analysis tool designed to detect indicators of AI generation (ChatGPT, Claude, Gemini, etc.) in essays, research drafts, and academic papers—specifically optimized for Indonesian linguistic patterns.

The system utilizes a **hybrid evaluation pipeline**: combining local statistical metrics (burstiness, sentence length variance, and structural symmetry) with structured semantic reasoning via the **Google Gemini API**.

---

## Key Features

- **Local Statistical Profiling:** Computes word counts, average sentence lengths, and variance (burstiness) offline to conserve API tokens.
- **AI Probability Scoring:** Provides an estimated AI generation score (0%–100%) alongside calibrated risk levels (*Low, Medium, High*).
- **Cliché Transition Detection:** Flags repetitive formal conjunctive markers commonly overused by LLMs (e.g., *oleh karena itu*, *dengan demikian*, *tidak dapat dimungkiri bahwa*).
- **Actionable Humanizer Suggestions:** Pinpoints rigid, robotic sentences and generates contextual, natural paraphrase alternatives.
- **Resilient Fallback Mechanism:** Includes built-in model retry logic to handle temporary server spikes (`503 UNAVAILABLE`) and guarantees structured output via Pydantic schemas.

---

## System Requirements

- Python 3.10 or newer
- Google Gemini API Key (obtainable for free via [Google AI Studio](https://aistudio.google.com/))
- Linux / macOS / Windows

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-detector.git
cd ai-detector
```

### 2. Configure Virtual Environment

For **Bash / Zsh**:
```bash
python -m venv env
source env/bin/activate
```

For **Fish Shell**:
```fish
python -m venv env
source env/bin/activate.fish
```

For **Windows (PowerShell)**:
```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install google-genai pydantic python-dotenv
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```bash
cp .env.example .env  # or create it manually
```

Add your Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## Usage Guide

1. **Run the script:**
   ```bash
   python detector.py
   ```
2. **Input Text:**
   - Paste the text excerpt you want to evaluate into the terminal.
   - Press **Enter**, then press:
     - `Ctrl + D` on Linux/macOS
     - `Ctrl + Z` followed by `Enter` on Windows to trigger the analysis pipeline.

### Sample Terminal Output

```text
=== AI TEXT DETECTOR & REWRITING ASSISTANT ===
Enter your draft text (press Ctrl+D on a new line to finish):
-------------------------------------------------------------------

[*] Computing local linguistic metrics...
[*] Analyzing textual patterns via Gemini...

=======================================================
📊 AI PROBABILITY SCORE : 75%
⚠️  RISK LEVEL           : High
=======================================================

[Text Statistics]
- Total Words       : 124
- Total Sentences   : 6
- Burstiness (SD)   : 2.14 (lower values indicate robotic uniformity)

[Linguistic Assessment]
The excerpt exhibits excessive structural symmetry, uniform sentence cadence, and repetitive formal transitions at paragraph break points.

[Flagged Sentences for Revision (1)]

1. Target   : "Oleh karena itu, implementasi teknologi ini sangat krusial."
   Reason   : Monotonous passive structure paired with formulaic transition marker.
   Revision : "Maka dari itu, penerapan teknologi ini penting untuk segera dijalankan."
```

---

## ⚠️ Disclaimer

No AI detection mechanism is 100% deterministic. AI detectors evaluate statistical variance, perplexity, and stylistic markers; they do not extract absolute cryptographic fingerprints. This utility is intended strictly as a self-assessment mirror to assist students and writers in identifying formulaic phrasing and improving natural cadence before submission.

---

## 📄 License

This project is open-source and distributed under the [MIT License](LICENSE).
