"""Run with python3 -m unittest discover -s cassidy_swe_editor/tests."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("paste_cleanup", Path(__file__).resolve().parents[1] / "features" / "paste_cleanup.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
clean = module.clean_paste_html


class PasteCleanupTests(unittest.TestCase):
    def test_inline_code_clipboard_wrapper(self):
        snippet = '<b>Use</b> <code>var_name = &lt;object&gt;</code> here'
        self.assertEqual(clean('<div>' + snippet + '</div>'), snippet)
        self.assertEqual(clean(snippet), snippet)
        for source in (
            '<div style="color: red"><code>x</code></div>',
            '<div><pre><code>x</code></pre></div>',
            '<div><code>x</code></div><div>next</div>',
        ):
            self.assertIn('<div', clean(source))

    def test_cocoa_indentation_wrappers(self):
        html = '<div><ul>\n<ul>\n<ul>\n<li>one</li>\n<li>two</li>\n</ul>\n</ul>\n</ul></div>'
        expected = '<div><ul><ul><ul>\n<li>one</li>\n<li>two</li>\n</ul></ul></ul></div>'
        self.assertEqual(clean(html), expected)
        self.assertEqual(clean(expected), expected)

    def test_craft_document_scaffolding(self):
        html = ('<meta charset="utf-8"><div id="craft_clipboard">'
                '<!DOCTYPE html>\n<html>\n<head>\n'
                '<meta name="Generator" content="Cocoa HTML Writer">\n'
                '<title></title>\n<style type="text/css"></style>\n'
                '</head>\n<body>\n<ul>\n<!--StartFragment-->\n'
                '<li><b>Mutable</b>: list</li>\n'
                '<li><b>Immutable</b>: tuple</li>\n<!--EndFragment-->\n'
                '</ul>\n</body>\n</html>\n</div>')
        expected = ('<div id="craft_clipboard"><html><body><ul>\n'
                    '<li><b>Mutable</b>: list</li>\n'
                    '<li><b>Immutable</b>: tuple</li>\n'
                    '</ul></body></html></div>')
        self.assertEqual(clean(html), expected)
        self.assertEqual(clean(expected), expected)

    def test_comments_do_not_hide_structural_whitespace(self):
        self.assertEqual(clean('<div>\n<!--comment-->\n<ul>\n<li>a</li>\n</ul>\n</div>'),
                         '<div><ul>\n<li>a</li>\n</ul></div>')
        self.assertEqual(clean('<pre>a\n<!--keep-->\n b</pre>'),
                         '<pre>a\n<!--keep-->\n b</pre>')

    def test_requested_layout(self):
        self.assertEqual(clean('<div>\n\n<ul>\n\n<li>some 1</li>\n<li>some 2</li>\n\n</ul>\n</div>'), '<div><ul>\n<li>some 1</li>\n<li>some 2</li>\n</ul></div>')

    def test_nested_list(self):
        expected = '<div><ul>\n<li>one\n<ul>\n<li>child</li>\n</ul></li>\n<li>two</li>\n</ul></div>'
        self.assertEqual(clean('<div><ul><li>one<ul><li>child</li></ul></li><li>two</li></ul></div>'), expected)
        self.assertEqual(clean(expected), expected)

    def test_sibling_blocks(self):
        self.assertEqual(clean('<div><p>one</p>\n\n<p>two</p></div>'), '<div><p>one</p>\n<p>two</p></div>')

    def test_inline_spaces_and_breaks(self):
        html = '<p><b>one</b>  <i>two</i><br/><br/>three</p>'
        self.assertEqual(clean(html), html)

    def test_protected_whitespace(self):
        for html in ('<pre>  a\n\n  b</pre>', '<code> \n\n </code>', '<div style="white-space: pre-wrap"><div>a</div>\n\n<div>b</div></div>'):
            self.assertEqual(clean(html), html)

    def test_content_is_retained(self):
        html = '<div><b>Mutable</b>: list, dictionary, set<br/><img src="image.png"/></div>'
        self.assertEqual(clean(html), html)

    def test_nbsp_and_empty_blocks(self):
        self.assertEqual(clean('<div><p>\u00a0</p><p></p></div>'), '<div><p>\u00a0</p>\n<p></p></div>')


if __name__ == '__main__':
    unittest.main()
