"""Personal editor features, isolated from other add-ons' JavaScript globals."""
import json
from pathlib import Path

from aqt import gui_hooks, mw
from aqt.editor import Editor

from .features.paste_cleanup import clean_paste_mime, finish_paste_layout
from .features.shortcut_labels import shortcut_label

ROOT = Path(__file__).parent
PACKAGE = __name__
FEATURE_FILES = (
    "selection.js",
    "code_spaces.js",
    "inline_code.js",
    "copy_source.js",
    "cloze_shortcuts.js",
    "paste_layout.js",
    "bootstrap.js",
)


def settings():
    defaults = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    defaults.update(mw.addonManager.getConfig(PACKAGE) or {})
    return defaults


def feature_script():
    config = json.dumps(settings()).replace("<", "\\u003c")
    source = "\n".join((ROOT / "web" / name).read_text(encoding="utf-8") for name in FEATURE_FILES)
    # One shared private scope lets feature files cooperate without replacing
    # Anki's or another add-on's functions. Each editor webview gets its own copy.
    script = (
        "(() => { if (window.cassidyEditor) return;\n"
        f"const settings = {config};\n{source}\n"
        "})();"
    )
    return script


def inject_features(content, context):
    if isinstance(context, Editor):
        content.body += "<script>" + feature_script() + "</script>"


def load_features(editor):
    editor.web.eval(feature_script())


def toggle_inline_code(editor):
    # Initialize and invoke in the same evaluation. Do not silently swallow a
    # missing API when an editor webview was rebuilt or skipped body injection.
    editor.web.eval(feature_script() + "\nwindow.cassidyEditor.toggleInlineCode();")


def add_button(buttons, editor):
    shortcut = settings()["inline_code_shortcut"]
    buttons.append(editor.addButton(
        icon=str(ROOT / "icons" / "inline-code.svg"),
        cmd="cassidy_inline_code",
        func=toggle_inline_code,
        tip=f"Inline Code ({shortcut_label(shortcut)})",
        keys=shortcut,
    ))


gui_hooks.webview_will_set_content.append(inject_features)
gui_hooks.editor_did_init_buttons.append(add_button)

gui_hooks.editor_did_load_note.append(load_features)

gui_hooks.editor_will_process_mime.append(clean_paste_mime)
gui_hooks.editor_did_paste.append(finish_paste_layout)
