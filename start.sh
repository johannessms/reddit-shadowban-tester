#!/bin/bash
cd "$(dirname "$0")"

# Prüfe, ob venv existiert, sonst erstelle sie
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# Aktiviere venv
source venv/bin/activate

# Installiere benötigte Pakete, falls noch nicht vorhanden
pip install --upgrade pip
pip install streamlit praw python-dotenv pandas

# Starte die App
streamlit run shadowbantester.py
