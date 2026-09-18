// Resolve both text and element-boundary carets, including Anki's shadow fields.
function getFieldInputSelection() {
    let active = document.activeElement;
    let focusedSelection = null;
    while (active?.shadowRoot) {
        const root = active.shadowRoot;
        const selection = root.getSelection?.();
        if (selection?.rangeCount && selection.focusNode) focusedSelection = selection;
        active = root.activeElement;
    }
    if (focusedSelection) return focusedSelection;
    const selection = window.getSelection();
    if (!selection?.rangeCount || !selection.focusNode) return null;
    const node = selection.focusNode;
    const element = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
    if (element?.closest('anki-editable,[contenteditable="true"]')) return selection;
    // Legacy Anki versions expose the field host through the window selection.
    for (const host of element?.querySelectorAll('.field,.rich-text-editable') || []) {
        const fieldSelection = host.shadowRoot?.getSelection?.();
        if (fieldSelection?.rangeCount && fieldSelection.focusNode) return fieldSelection;
    }
    return null;
}


// Toolbar activation can move focus outside the field's shadow root. Remember
// the field itself so its native selection remains reachable from the button.
let lastCassidySWEEditorField = null;
document.addEventListener('focusin', event => {
    const field = event.composedPath().find(node => node?.matches?.('anki-editable'));
    if (field) lastCassidySWEEditorField = field;
}, true);
const resolveFocusedFieldSelection = getFieldInputSelection;
getFieldInputSelection = function() {
    const current = resolveFocusedFieldSelection();
    if (current?.rangeCount) return current;
    if (!lastCassidySWEEditorField?.isConnected) return null;
    const root = lastCassidySWEEditorField.getRootNode();
    const selection = root.getSelection?.();
    if (!selection?.rangeCount) return null;
    const range = selection.getRangeAt(0);
    return lastCassidySWEEditorField.contains(range.startContainer) &&
        lastCassidySWEEditorField.contains(range.endContainer) ? selection : null;
};
