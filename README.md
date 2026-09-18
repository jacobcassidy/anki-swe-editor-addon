# Cassidy Editor

Personal Anki editor add-on. Restart Anki after installation or configuration changes.

## Features

- `web/inline_code.js`: inline-code toggle, caret entry/exit, selection wrapping.
- `web/code_spaces.js`: normalize single non-breaking separators around inline code.
- `web/copy_source.js`: copy selected source markup without computed CSS styles.
- `web/cloze_shortcuts.js`: macOS Control shortcuts and matching cloze tooltips:
  new card `⌃⇧C`, same card `⌃⌥⇧C`.
- `web/paste_layout.js`: restore the closing line of newly pasted lists after insertion.
- `web/selection.js`: shared selection handling, including shadow-root fields.
- `web/bootstrap.js`: public entry point for the toolbar button and shortcut.
- `__init__.py`: Anki hooks, toolbar button, configuration, and script loading.

The default shortcut is Ctrl+Shift+C (Command+Shift+C on macOS through Anki).
Configuration is available through Tools → Add-ons → Cassidy Editor → Config.
The files run inside one private JavaScript scope, without the Wrapper meta-addon.

## Migration

Wrapper meta-addon (396502676) was disabled because its only configured button
was the inline-code action now provided here. Its files remain intact.
Original custom JavaScript, commands, and metadata are preserved in
`user_files/migration_backup/` for rollback. Do not enable both add-ons together:
they would register duplicate shortcuts and clipboard handlers.

To roll back, disable Cassidy Editor and re-enable Wrapper, then restart Anki.

## Validation and limits

Python syntax, JavaScript syntax, and mocked Anki hook wiring are checked during
migration. Full editor behavior still needs validation in the running Anki app.
The clipboard customization handles Copy in rich-text fields; it does not
intercept Cut or remove inline styles already present in existing notes.
Anki's paste sanitization and browser insertion may still adjust HTML structure.

Block-aware wrapping was adapted from the installed Wrapper meta-addon,
which cites https://github.com/ankitects/anki/pull/3038.

## Paste cleanup

`features/paste_cleanup.py` cleans external rich HTML through Anki's
`editor_will_process_mime` filter. Enabled by default; set `paste_cleanup` to
`false` in the add-on config to disable it. Restart Anki after updating.

Blank structural whitespace is removed. Sibling blocks get one newline; nested
opening and closing tags share their parent's edge lines. List items and table
rows/cells have separate lines from their containers, for example:

```html
<div><ul>
<li>some 1</li>
<li>some 2</li>
</ul></div>
```

Normal Craft Command+C includes a Cocoa HTML document inside a clipboard div.
The cleaner removes document headers, metadata, doctypes, and comments outside
protected regions before joining adjacent whitespace. Nested list wrappers used
only for indentation share edge lines, so Anki's insertion does not leave blank
lines when it collapses those wrappers.

Inline separators, explicit breaks, empty elements, nonbreaking spaces, and
pre/code or inline whitespace-preserving regions are retained. This formats
HTML source; CSS may still affect displayed spacing. Plain-text pastes and
internal Anki pastes are skipped. The same MIME hook also covers external HTML
drops. Other clipboard formats are copied unchanged; the system clipboard and
existing notes are not rewritten. Anki may further sanitize the pasted HTML.

Validation: `python3 -m unittest discover -s cassidy_editor/tests` from the
add-ons directory, plus Python syntax checks. Verified normal Craft Command+C
and Anki Command+V in the running editor, including the resulting HTML source.
Anki's insertion can still adjust wrapping. For newly inserted lists with an
opening newline, a final paste step restores the newline before `</ul>` or
`</ol>` that Chromium can drop. Existing lists and protected code regions are
left alone. Verified the separate closing line in the HTML editor and native
one-step paste undo in an empty field.

Inline-only code snippets from Option-Command-C have their redundant bare outer
`div` removed before insertion. This prevents Chromium from replacing `code`
with computed-style spans when merging the snippet into existing prose. Wrappers
with attributes and snippets containing blocks or lists retain their structure.
Validated with an isolated Chromium insertion/undo/redo reproduction and the
Python cleanup tests; the updated hook still needs a live Anki paste check.
