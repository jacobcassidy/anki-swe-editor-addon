window.cassidySWEEditor = {
    beginPasteLayout,
    finishPasteLayout,
    toggleInlineCode() {
        const selection = getFieldInputSelection();
        toggleInlineCode.call({node: selection?.focusNode}, '<code>', '</code>');
    }
};
