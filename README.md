# whatsapp-chat-analyzer

A small Streamlit app to analyze WhatsApp exported chat files. It computes message statistics, timelines, activity maps, word clouds, emoji counts and more.

## What I added
- Top-level `.gitignore` to ignore common Python artifacts and IDE files.
- `requirements.txt` listing the project's Python dependencies.
- This expanded `README.md` with setup and run instructions.

## Project structure
- `app.py` — Streamlit application (do not modify unless needed)
- `preprocessor.py` — chat parsing and preprocessing (do not modify)
- `helper.py` — analysis helper functions (do not modify)
- `stop_hinglish.txt` — stopwords used for wordcloud

## Requirements
This project was developed with Python 3.8+. Install dependencies with:

Windows PowerShell:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the app
After installing dependencies, run the Streamlit app:

```powershell
streamlit run app.py
```

Then open the URL shown by Streamlit (usually http://localhost:8501).

## Notes
- I did not modify `app.py`, `preprocessor.py`, or `helper.py` as requested.
- The `requirements.txt` includes the packages observed from imports in the code. If you use additional packages, add them to the file and run `pip install -r requirements.txt` again.

## License & Author
Your repository — add license details here if desired.