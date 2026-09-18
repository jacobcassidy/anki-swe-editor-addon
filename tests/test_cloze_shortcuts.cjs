const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync(`${__dirname}/../web/cloze_shortcuts.js`, "utf8");

function setup(platform = "MacIntel") {
    let buttons = [];
    let observer;
    const handlers = {};
    vm.runInNewContext(source, {
        navigator: { platform },
        document: {
            documentElement: {},
            querySelectorAll: () => buttons,
            addEventListener: (type, callback, capture) => {
                assert.equal(capture, true);
                handlers[type] = callback;
            },
        },
        MutationObserver: class {
            constructor(callback) { observer = callback; }
            observe() {}
        },
    });
    buttons = ["Cloze new card (⌘⇧C)", "Cloze same card (⌘⌥⇧C)"].map(title => ({
        title, disabled: false, clicks: 0,
        click() { this.clicks++; },
    }));
    return { buttons, handlers, update: () => observer() };
}

const { buttons, handlers, update } = setup();
update();
update();
assert.deepEqual(buttons.map(b => b.title), ["Cloze new card (⌃⇧C)", "Cloze same card (⌃⌥⇧C)"]);
function press(overrides = {}) {
    const event = {
        type: "keydown", code: "KeyC", shiftKey: true, ctrlKey: true,
        metaKey: false, altKey: false, repeat: false, isComposing: false,
        preventDefault() { this.prevented = true; },
        stopImmediatePropagation() { this.stopped = true; },
        ...overrides,
    };
    handlers[event.type](event);
    return event;
}
press();
press({ altKey: true });
assert.deepEqual(buttons.map(b => b.clicks), [1, 1]);
for (const altKey of [false, true]) {
    for (const type of ["keydown", "keyup"]) {
        assert.equal(press({ ctrlKey: false, metaKey: true, altKey, type }).stopped, true);
    }
}
press({ type: "keyup" });
press({ repeat: true });
press({ isComposing: true });
press({ shiftKey: false });
press({ metaKey: true });
buttons[0].disabled = true;
press();
assert.deepEqual(buttons.map(b => b.clicks), [1, 1]);
assert.deepEqual(Object.keys(setup("Win32").handlers), []);
console.log("Cloze shortcut and tooltip checks passed.");
