# Project context

- This repository is a self-contained data Skill. The canonical endpoint implementations live in the Python blocks of `SKILL.md`.
- Read the relevant endpoint section and required helpers before changing or calling it. Preserve the upstream source and Apache-2.0 license.
- Use the project virtual environment: `.venv/bin/python`. Install dependencies with `.venv/bin/python -m pip install -r requirements.txt`.
- Run offline checks with `.venv/bin/python -m unittest discover -s tests`. Live checks require explicit environment flags described in the test files.
- `examples/quote.py` loads the quote implementation from `SKILL.md`; avoid duplicating endpoint implementations in the example.
- Use `docs/local-development.md` for local usage and Git workflow instructions.
- Never commit `.venv`, `.env`, API credentials, or generated reports. Keep Eastmoney requests serial and use the existing throttling helper.
