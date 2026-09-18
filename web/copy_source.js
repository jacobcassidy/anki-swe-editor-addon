// Copy source markup instead of Chromium's computed-style clipboard snapshot.
function copyEditorSourceHtml(event) {
    if (!event.clipboardData) return;
    const selection = getFieldInputSelection();
    if (!selection?.rangeCount || selection.isCollapsed) return;
    const range = selection.getRangeAt(0);
    const element = node => node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
    const field = element(range.startContainer)?.closest('anki-editable');
    if (!field || !field.contains(range.endContainer)) return;
    // Leave copies from the HTML source editor and other controls to Anki.
    if (!event.composedPath().includes(field)) return;
    let fragment = range.cloneContents();
    // cloneContents omits the common ancestor: retain its inline formatting and
    // list/block context without copying unselected siblings or editor wrappers.
    for (let parent = element(range.commonAncestorContainer); parent && parent !== field; parent = parent.parentElement) {
        const wrapper = parent.cloneNode(false);
        wrapper.append(fragment);
        fragment = wrapper;
    }
    const container = document.createElement('div');
    container.append(fragment);
    event.clipboardData.setData('text/html', container.innerHTML);
    event.clipboardData.setData('text/plain', selection.toString());
    event.preventDefault();
    // Allow Anki's own copy listener to record this as an internal copy.
}
if (settings.copy_source_html) document.addEventListener('copy', copyEditorSourceHtml, true);
