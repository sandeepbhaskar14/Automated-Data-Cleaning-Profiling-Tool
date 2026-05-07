# 🧹 Automated Data Cleaning & Profiling Tool

A desktop application built with **PyQt5** and **Flask** that automates data cleaning, profiling, and preprocessing for CSV and tabular datasets — giving you actionable quality reports without writing a single line of code.

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Running the App](#-running-the-app)
- [Screenshots](#-screenshots)
- [Future Improvements](#-future-improvements)
- [License](#-license)

---

## 🚩 Problem Statement

Data analysts and data scientists spend a disproportionate amount of time — often cited as **60–80% of a project** — cleaning and preparing raw datasets before any meaningful analysis can begin. Common pain points include:

- Manually hunting for missing values and deciding how to handle them
- Identifying and removing duplicate records
- Detecting outliers that skew results
- Correcting inconsistent data types across columns

**Automated Data Cleaning & Profiling Tool** eliminates this toil by providing a clean desktop UI that automates all of the above, generates a data quality score, and produces a downloadable report — in seconds.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Data Profiling** | Instant summary statistics and column-level analysis |
| 🧼 **Missing Value Handling** | Fill with mean / median / mode, forward fill, or drop |
| 🗑️ **Duplicate Removal** | Detect and remove exact duplicate rows |
| 📊 **Outlier Detection** | IQR and Z-score based outlier flagging |
| 🔢 **Data Type Correction** | Automatically infer and fix column data types |
| 🏅 **Quality Score** | Composite score (0–100%) with Excellent / Good / Fair / Poor rating |
| 📄 **Report Generation** | Export a full data quality report |
| 🎨 **Light / Dark Theme** | Toggle between themes from Settings |
| 🗂️ **Multi-format Support** | `.csv`, `.xlsx`, `.xls`, `.tsv`, `.parquet` |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Desktop GUI | PyQt5 5.15.10 |
| Backend API | Flask 3.0.3 |
| Data Processing | Pandas 2.2.2, NumPy 1.26.4, SciPy 1.13.0 |
| Visualisation | Matplotlib 3.9.0 |
| Report Generation | ReportLab 4.2.2, Jinja2 3.1.4 |
| HTTP Client | Requests 2.32.3 |
| Environment Config | python-dotenv 1.0.1 |

---

## 📁 Project Structure

```
project-root/
│
├── shared/
│   └── constants.py              # Shared constants (app name, version, routes)
│
├── Frontend/
│   ├── main.py                   # Entry point — run this to launch the GUI
│   ├── config/
│   │   └── settings.py           # Frontend config (API URL, window size, logging)
│   ├── services/
│   │   ├── api_client.py         # All HTTP calls to the backend
│   │   └── logger.py             # Rotating file + coloured console logger
│   ├── ui/
│   │   └── mainUI.py             # Auto-generated PyQt5 UI class
│   ├── ui_controller/
│   │   └── ui_functions.py       # Window behaviour (toggle, maximize, navigation)
│   ├── xml_ui/
│   │   └── mainUI.ui             # Qt Designer source file
│   └── logs/
│       └── frontend.log
│
├── Backend/
│   ├── run.py                    # Entry point — run this to start the Flask server
│   ├── config/
│   │   └── settings.py           # Backend config (Flask host/port, upload limits)
│   ├── core/
│   │   └── logger.py             # Backend logger
│   ├── api/
│   │   ├── app.py                # Flask application factory
│   │   └── blueprints/
│   │       ├── health.py         # GET /api/health/
│   │       ├── dataset.py        # POST/GET/DELETE /api/dataset/
│   │       ├── clean.py          # POST /api/clean/<id>/*
│   │       ├── profile.py        # GET /api/profile/<id>/*
│   │       └── report.py         # POST/GET /api/report/
│   └── logs/
│       └── backend.log
│
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Requirements

- **Python** `3.10.0` or higher (developed and tested on `3.10.x`)
- **pip** (comes with Python)
- **Windows 10/11** (primary target; Linux/macOS may work with minor path adjustments)

> ⚠️ PyQt5 requires a display server. On headless Linux servers you will need `Xvfb` or a virtual display.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/automated-data-cleaning-tool.git
cd automated-data-cleaning-tool
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure environment variables

Create `.env` files if you want to override defaults:

**`Frontend/.env`**
```env
API_BASE_URL=http://127.0.0.1:5050
API_TIMEOUT=10
LOG_LEVEL=INFO
```

**`Backend/.env`**
```env
FLASK_HOST=0.0.0.0
FLASK_PORT=5050
FLASK_DEBUG=false
SECRET_KEY=your-secret-key-here
LOG_LEVEL=INFO
```

---

## ▶️ Running the App

You need **two terminals** — one for the backend, one for the frontend.

### Terminal 1 — Start the Backend

```bash
cd Backend
python run.py
```

You should see:
```
INFO  __main__  —  Backend starting  http://0.0.0.0:5050  (debug=False)
```

### Terminal 2 — Start the Frontend

```bash
cd Frontend
python main.py
```

The desktop window will open. The frontend automatically connects to `http://127.0.0.1:5050`.

---

## 🖼️ Screenshots

> _Add screenshots of the Home, Dashboard, Cleaning, and Report pages here._

---

## 🔮 Future Improvements

The following enhancements are planned for upcoming releases:

### 🤖 AI-Assisted Cleaning Suggestions
Integrate a lightweight ML model (or LLM prompt) that analyses the dataset context and recommends the most appropriate cleaning strategy per column — e.g., suggesting `median` fill for skewed distributions instead of `mean`.

### 📊 Interactive Column Explorer
Add a drill-down panel in the Dashboard where users can click any column to see its full distribution histogram, unique value counts, and per-column quality score — powered by embedded Matplotlib canvases.

### 🔄 Cleaning History & Undo
Maintain a versioned cleaning log so users can step back through each operation (undo/redo) without having to re-upload the original file.

### ☁️ Cloud Dataset Support
Allow direct import from Google Sheets, AWS S3, or a URL endpoint, removing the friction of first downloading datasets locally.

### 📤 Export Formats
Support exporting the cleaned dataset back to `.xlsx`, `.parquet`, and `.json` in addition to `.csv`, along with a PDF data quality report generated via ReportLab.

### 🌐 Web Interface
Provide an optional browser-based UI (React or plain HTML) served by the existing Flask backend, making the tool accessible without installing PyQt5.

---

## 📬 Contact

For questions or feedback, reach out at **san767bhbaskar@gmail.com**

---

<p align="center">
  Built with ❤️ using Python, PyQt5 and Flask
</p>
