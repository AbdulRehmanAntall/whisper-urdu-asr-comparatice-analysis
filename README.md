# Urdu ASR Comparative Analysis using Whisper Models

This repository contains the complete codebase and dataset for the research project: **"Comparative Performance Analysis of Lightweight Whisper Models for Urdu Automatic Speech Recognition (ASR)."**  
The project evaluates the zero-shot capabilities of Whisper-Tiny, Whisper-Base, and Whisper-Small models on real-world Urdu speech samples using open-source tools and FastAPI-based web services.

---

## Project Overview

Automatic Speech Recognition (ASR) systems have seen great progress in high-resource languages, yet remain underdeveloped for low-resource ones like Urdu. This project explores the performance of multilingual Whisper models for Urdu by:

- Collecting native Urdu voice recordings.
- Evaluating Whisper-Tiny, Base, and Small models.
- Measuring **Word Error Rate (WER)** and **Character Error Rate (CER)**.
- Identifying performance gaps and bottlenecks for Urdu ASR.

---

---

## How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/whisper-urdu-asr-comparative-analysis.git
cd whisper-urdu-asr-comparative-analysis
```
### 2. Install Dependencies

```bash
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
Navigate to **http://127.0.0.1:8000**
You’ll see an interface where users can record and upload Urdu speech samples. All entries are saved to the database via SQLAlchemy ORM.

### 5. Evaluate ASR Models

Run any of the model files (e.g., for Whisper-Small):

 ```bash
uvicorn whisper_small:app --reload
```

<details>


1. A FastAPI interface will start at: `http://localhost:8000`
2. Upload a recorded **Urdu voice sample**.
3. Select the correct **prompt** from the dropdown.
4. The app will return:
   - 🟢 **WER** (Word Error Rate)
   - 🟢 **CER** (Character Error Rate)
5. Results can be:
   - Logged manually for tracking.
   - Exported for performance evaluation.

</details>

Repeat for Whisper-Tiny, Whisper-Base, Whisper-Medium:
 ```bash
uvicorn whisper_tiny:app --reload
uvicorn whisper_base:app --reload
uvicorn whisper_medium:app --reload


```

