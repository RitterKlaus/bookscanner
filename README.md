# bookscanner
Eine Anwendung um ISBNs zu scannen, zu sammeln und Daten zu Büchern abzurufen.
Leider gibt es kaum vernünftige Services, um Daten zu ISBNs kostenlos abzurufen.
Ein Service ist https://openlibrary.org/, aber der kannte viele meiner Bücher nicht.
Daher habe ich ISBN**DB** ausprobiert. Die ersten 7 Tage sind kostenlos.

# Voraussetzungen

* Python 3.13
* Ein API-Key bei https://isbndb.com. Der API-Key muss als `API_KEY=` in einer `.env`-Datei eingetragen werden.

# Installation

1. Virtuelle Umgebung anlegen: `python -m venv path/to/working/folder/.venv`
2. Virtuelle Umgebung aktivieren: `.venv/Scripts/Activate`
3. Abhängigkeiten installieren: `pip install -r requirements.txt`
4. Starten des Skripts mit `streamlit run bookscanner.py`
5. Im Browser `http://localhost:8502/` aufrufen und ISBNs eintippen.

Das Python-Skript `get_isbn_by_batch.py` kann benutzt werden, um den API-Zugriff mit einer Liste von ISBNs zu testen.

__Info:__
Erstellt mit Hilfe des KI-Assistenten Github Copilot und Claude Sonnet 3.5 * 0.9x