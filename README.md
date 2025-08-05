# Urdu ASR Comparative Analysis using Whisper Models

This repository contains the complete codebase and dataset for the research project: **"Comparative Performance Analysis of Lightweight Whisper Models for Urdu Automatic Speech Recognition (ASR)."**
The project evaluates the zero-shot capabilities of Whisper-Tiny, Whisper-Base, and Whisper-Small models on real-world Urdu speech samples using open-source tools and FastAPI-based web services.

---

## Project Overview

Automatic Speech Recognition (ASR) systems have seen great progress in high-resource languages, yet remain underdeveloped for low-resource ones like Urdu. This project explores the performance of multilingual Whisper models for Urdu by:

* Collecting native Urdu voice recordings.
* Evaluating Whisper-Tiny, Base, and Small models.
* Measuring **Word Error Rate (WER)** and **Character Error Rate (CER)**.
* Identifying performance gaps and bottlenecks for Urdu ASR.

---

## How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/whisper-urdu-asr-comparative-analysis.git
cd whisper-urdu-asr-comparative-analysis
```

### 2. Set Up Virtual Environment and Install Dependencies

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment (Windows)
venv\Scripts\activate

# Or activate (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a **.env** file in the root directory with your PostgreSQL database URL:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/your_db_name
```

### 4. Run the Voice Recording Interface

```bash
uvicorn main:app --reload
```

Navigate to **[http://127.0.0.1:8000](http://127.0.0.1:8000)**
You’ll see an interface where users can record and upload Urdu speech samples. All entries are saved to the database via SQLAlchemy ORM.

***⚠️ Important: Before running the app, make sure to manually add Urdu prompts to your PostgreSQL database using SQL queries. These prompts are necessary for the dropdown in the evaluation interface and for accurate transcription comparison.***

### 5. Evaluate ASR Models

Run any of the model files (e.g., for Whisper-Small):

```bash
uvicorn whisper_small:app --reload
```

### 🧪 Evaluation Workflow

<details>
<summary>✨ Click to view the evaluation steps</summary>

> ⚠️ **Note:** You must manually insert Urdu prompts into the database before using the evaluation system. This can be done using SQL queries directly on your PostgreSQL instance. Without prompt entries, the dropdown menu will appear empty.

#### Step-by-Step Guide:

1. **Start the FastAPI Interface**
   Navigate to `http://localhost:8000` to access the frontend.

2. **Select a Prompt**
   Use the dropdown menu to choose from predefined Urdu prompts. These sentences are used as ground truth for ASR evaluation.

3. **Upload Your Recording**
   Choose your Urdu audio file recorded against the selected prompt. Supported formats: `.wav`, `.mp3`, `.m4a` (automatically converted if needed).

4. **Submit for Evaluation**
   Once submitted, the system will:

   * Transcribe the audio using the selected Whisper model
   * Compare the transcription with the selected prompt
   * Calculate:

     * 🟢 **Word Error Rate (WER)** — Measures word-level mistakes
     * 🟢 **Character Error Rate (CER)** — Measures character-level mistakes

5. **Review Feedback**
   Get instant evaluation feedback shown on the results page, with:

   * Highlighted errors (optional enhancement)
   * Accuracy percentages

6. **Manual Logging / Exporting**
   Results are also stored locally in CSV files (`log.csv`) for manual review or future export.

   * Format: `filename, prompt_key, ground_truth, transcription, WER, CER`

7. **Compare Across Models**
   Repeat the above steps using different Whisper variants to benchmark performance.

</details>

Repeat for other models:

```bash
uvicorn whisper_tiny:app --reload
uvicorn whisper_base:app --reload
uvicorn whisper_medium:app --reload
```

---

### 6. Dataset

The `uploads/` folder contains Urdu recordings collected during this project. These are provided for reproducibility and further model training or evaluation. Contributions to this dataset are encouraged — extend it by adding more recordings and fine-tune models accordingly.

---

### 7. Contributing

Want to extend the dataset? Add a new evaluation script? Tune a model?

Feel free to:

1. Fork the repo
2. Add improvements
3. Open pull requests!

---

### 8. Citation

If this project contributes to your research or work, please consider citing the paper (coming soon) or referencing this GitHub repository.

### 9. License

This project is licensed under the [MIT License](LICENSE).

You are free to use, modify, and distribute this project for personal, academic, or commercial purposes — as long as you include the original copyright.
