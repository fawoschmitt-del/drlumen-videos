# Dr. Lumen – tägliche Erklärvideos (TikTok)

Neues Projekt, ersetzt die Serie Kitchen Chaos (abgebrochen). Die alten Dateien im übergeordneten Ordner werden nicht mehr gebraucht.

- Host: **DR. LUMEN**, eine 3D-Glühbirne mit runder Brille, roter Fliege und weißen Handschuhen. Sie leuchtet, wenn sie spricht.
- Format: Englisch, 9:16 (1080x1920), **über 60 s** (wichtig für die Monetarisierung), spannende Alltagsfragen ("Why can't you tickle yourself?")
- Stimme: Kokoro TTS (Open Source, ONNX-Version), Stimme `am_michael`, Tempo 1.08
- Untertitel: Wort für Wort (Whisper-Alignment), aktives Wort gelb
- Oben eine Illustrationskarte pro Satz, Musikbett mit Ducking, Lautheit auf -14 LUFS normalisiert
- Posten: über Buffer (Organisation "My organization") auf TikTok @editor_73902 und YouTube "Hans peter" (Shorts),
  täglich **01:00 Europe/Berlin** (= 19 Uhr US-Ostküste / 16 Uhr US-Westküste). Nach 2–4 Wochen mit eigenen Analytics prüfen.
- Repo: github.com/fawoschmitt-del/drlumen-videos – Code auf `main`, fertige Videos auf dem Branch `media`
  (enthält nur die neuesten 7 Videos; daraus lädt Buffer die Datei).
- Tägliche Folge: eine geplante Aufgabe in Claude arbeitet `DAILY.md` ab (Thema aus `topics.md`, Recherche, Skript,
  Rendern, Veröffentlichen, in Buffer einplanen).

## Folgen
| Datei | Thema | Länge |
|---|---|---|
| episodes/tickle.py | Why can't you tickle yourself? | 91 s |

## Dateien
- `lumen3d.py` – Figur (SDF-Raymarching, numpy + PIL). `python lumen3d.py` rendert alle Posen nach cache/ (dauert ca. 10 Min.)
- `voice.py` – Kokoro-Stimme pro Satz + Wort-Timings (faster-whisper), schreibt voice.wav + timing.json
- `explainer.py` – Video-Renderer. `python explainer.py tickle preview` (Kontaktbogen) / `python explainer.py tickle` (fertiges MP4 in out/tickle/)
- `publish.py` – lädt ein fertiges Video auf den media-Branch und gibt die öffentliche URL aus
- `DAILY.md` – Anleitung für den täglichen Lauf, `topics.md` – erledigte Themen + Ideenliste
- `episodes/<thema>.py` – eine Folge = TITLE, CAPTION und BEATS = [(visual, arme, text), ...]
  Arme: down / point / shrug / up. Für unbekannte visual-Keys erscheint automatisch eine Stichwort-Karte;
  eigene Illustrationen kommen als `v_<name>` in explainer.py und werden in VISUALS eingetragen.

## Einrichtung
    bash setup.sh      # Linux; unter Windows: pip install -r requirements.txt + Modelle manuell
    # Modelle nach ./models/ (oder Umgebungsvariable KOKORO_DIR):
    #   https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
    #   https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
    # ffmpeg im PATH. Fonts liegen in ./fonts/ (OFL-Lizenz)

## Quellen Folge "tickle"
Blakemore, Wolpert & Frith 1998 (Nature Neuroscience), Blakemore et al. 1999 (J. Cogn. Neurosci., Kitzel-Roboter: 0–200 ms Verzögerung = kitzliger),
Blakemore et al. 2000 (NeuroReport), Panksepp 2003 (Ratten-Lachen ~50 kHz), Ishiyama & Brecht 2016 (Science, HU Berlin: Bauch und Füße).
