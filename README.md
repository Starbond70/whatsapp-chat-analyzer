# whatsapp-chat-analyzer

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
