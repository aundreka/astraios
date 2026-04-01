# AstraiOS

AstraiOS is a desktop application built with Python and Tkinter that provides:

- Astrology profile generation
- Tarot readings
- Zodiac compatibility checking
- Lunar phase tracking
- Local SQLite data storage

## Run

```bash
python main.py
```

## Project Structure

- `main.py` – entry point
- `ui/` – Tkinter views and dashboard shell
- `backend/` – business logic
- `database/` – SQLite setup and models
- `utils/` – helper functions and theme constants

## Notes

- Moon sign and rising sign are lightweight approximations unless you integrate a library like `skyfield` or `ephem`.
- Tarot AI explanations currently use a local fallback generator.
