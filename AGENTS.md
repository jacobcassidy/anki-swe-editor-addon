# Cassidy SWE Editor: instructions for coding agents

These instructions apply to this directory and all of its subdirectories.

## Anki reference

- Use the official Anki add-on documentation as the primary reference when
  working on this add-on: https://addon-docs.ankiweb.net/.
- Consult the relevant documentation before implementing or changing Anki
  integration. Check Anki's source for the installed version when the
  documentation does not cover an API or behavior.

## Feature organization

- Keep each distinct feature in its own file when practical. Keep shared
  utilities separate, and use `__init__.py` for Anki integration and loading.
- Put Python feature modules and Python helpers in `features/`. These run in
  Anki's Python process and handle work such as clipboard HTML cleanup, Anki
  API calls, and shortcut label formatting.
- Put JavaScript that runs in the editor's webview in `web/`. This includes
  DOM changes, text selection, formatting, and browser keyboard events.
- A feature may span both directories: keep its Python work in `features/`
  and its browser work in `web/`. Register Anki hooks and load the feature
  modules and scripts in the root `__init__.py`.

## Git commits

- Create a Git commit for each completed new feature, fix, refactor, or other
  logical change after appropriate validation.
- Use a concise, descriptive commit message explaining the change.
- Stage only files belonging to that change. Do not include unrelated user work.
- Check the repository root before committing, especially when accessing this
  directory through a symlink. If no repository is available, report that and
  arrange repository setup rather than claiming a commit was created.
- Report validation performed and any limitations; do not claim live Anki
  verification when only syntax checks or isolated tests were run.
