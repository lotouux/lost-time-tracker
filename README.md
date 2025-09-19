# ⏳ Lost Time Tracker

[![Status](https://img.shields.io/badge/status-Development-yellow?style=for-the-badge)](#)
[![Python](https://img.shields.io/badge/python-3.12-blue?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](#)

## 📌 Overview
**Lost Time Tracker** is a Python project that analyzes system usage logs and estimates **how much time you spend in different applications**.  

It generates weekly reports with detailed statistics and translates wasted time into **creative equivalents**, such as: 

- How many books you could have read 📚  
- How many movies you could have watched 🎥  
- How many kilometers you could have run 🏃

The project now includes **automatic application categorization using Hugging Face's Zero-Shot Classification** and shows a **progress bar** for classification with `tqdm`.

---

## 🚀 Features

✔️ Collects running process data from the operating system  
✔️ Automatic app categorization (Browser, Games, Productivity, etc.) using AI  
✔️ Classification progress shown with a **progress bar**  
✔️ Reports in **tables** (terminal output)  
✔️ Stats per category and per application  
✔️ Creative conversion of hours → productivity (e.g. books, movies, km run)  

🛠️ Planned:  
- Export reports to `.txt` and `.pdf`  
- Graphs with `matplotlib`  
- Cross-platform support (Windows, macOS, Linux)  

---

## 🛠️ Technologies

- **Python 3.12**
- **Main libraries:**
  - `wmi` → process collection on Windows  
  - `pandas` → data handling  
  - `tqdm` → classification progress bar  
  - `transformers` → zero-shot classification of apps  
  - `tabulate` / `prettytable` → terminal table reports  
  - `matplotlib` → chart generation (planned)

---

 ## 📊 Example Output
```bash
 --- Screen Time Report (Last 7 Days) ---
 
Estimated Total Screen Time: 45.23 hours

Total Process Execution Time by Category:
Productivity     18.50
Browser          12.30
Games             8.20
Entertainment     5.80

You could have read 2.05 books (10h each) with the time spent on games and browsing.
```
---

## 📌 Roadmap

- Historical data collection (last 7 days)
- Automatic AI-based app categorization
- Classification progress display (tqdm)
- Usage reports by category
- Creative conversions (books, movies, marathons, km run)
- Report export (.txt, .pdf)
- Graphical visualization with matplotlib
- Cross-platform support (Windows, macOS, Linux)

---

## ⚙️ How to Run

1. Clone the repository:  
```bash
git clone https://github.com/lotouux/lost-time-tracker.git

```
2. Create and activate a virtual environment (optional but recommended):  
```bash
python -m venv venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:  
```bash
pip install -r requirements.txt
```

4. Run the script:  
```bash
python main.py
```

---

## 📜 License

This project is under the MIT License – feel free to use, modify, and contribute.

---

## 🤝 Contribution

Contributions are welcome!

Suggestions, improvements, and new ideas can be discussed via issues or pull requests.
