"""Tests for skills/sole/scripts/fetch.py. Standard library only; no network beyond 127.0.0.1."""
import contextlib
import http.server
import io
import os
import sys
import threading
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "sole", "scripts"))
import fetch  # noqa: E402

ARTICLE = "<html><body><main>" + "<p>Loose-leaf tea, packed in Bristol since 2019.</p>" * 20 + "</main></body></html>"
CHALLENGE = ("<html><head><title>Just a moment...</title></head><body><h1>Verify you are human</h1>"
             "<p>Checking your browser before accessing the site.</p></body></html>")
FORM_WITH_RECAPTCHA = ("<html><head><script src='https://www.google.com/recaptcha/api.js'></script></head><body><main>"
                       + "<p>Contact our shop about wholesale orders and tasting sessions.</p>" * 15
                       + "<p>This form is protected by reCAPTCHA.</p></main></body></html>")
SHORT = "<html><body><p>Loading...</p></body></html>"

PAGES = {"/article": (200, ARTICLE), "/challenge": (503, CHALLENGE), "/challenge200": (200, CHALLENGE),
         "/form": (200, FORM_WITH_RECAPTCHA), "/short": (200, SHORT)}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 - http.server naming
        status, body = PAGES.get(self.path, (404, "<html><body>not found</body></html>"))
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


class FetchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def run_main(self, url):
        out, err = io.StringIO(), io.StringIO()
        code = 0
        with mock.patch.object(sys, "argv", ["fetch.py", url]), contextlib.redirect_stdout(out), \
                contextlib.redirect_stderr(err), mock.patch.object(sys.stdout, "reconfigure", create=True):
            try:
                fetch.main()
            except SystemExit as e:
                code = e.code
        return code, out.getvalue(), err.getvalue()

    def test_html_to_text_drops_scripts_and_keeps_main(self):
        text = fetch.html_to_text("<html><script>var x=1</script><main>" + "<p>tea</p>" * 200 + "</main></html>")
        self.assertNotIn("var x", text)
        self.assertIn("tea", text)

    def test_direct_reads_a_normal_page(self):
        self.assertIn("packed in Bristol", fetch.direct(self.base + "/article"))

    def test_recaptcha_widget_on_a_normal_page_is_not_a_bot_check(self):
        self.assertFalse(fetch.is_bot_check(FORM_WITH_RECAPTCHA))
        self.assertIn("wholesale", fetch.direct(self.base + "/form"))

    def test_challenge_page_raises_bot_check(self):
        for path in ("/challenge", "/challenge200"):
            with self.subTest(path=path), self.assertRaises(fetch.BotCheck):
                fetch.direct(self.base + path)

    def test_short_page_is_blocked_but_not_a_bot_check(self):
        with self.assertRaises(RuntimeError) as ctx:
            fetch.direct(self.base + "/short")
        self.assertNotIsInstance(ctx.exception, fetch.BotCheck)

    def test_bot_check_stops_the_chain_without_calling_readers(self):
        with mock.patch.object(fetch, "jina") as jina, mock.patch.object(fetch, "firecrawl") as firecrawl:
            code, out, err = self.run_main(self.base + "/challenge")
        self.assertEqual(code, 3)
        jina.assert_not_called()
        firecrawl.assert_not_called()
        self.assertIn("does not route around", err)
        self.assertEqual(out, "")

    def test_short_page_falls_through_to_the_reader(self):
        with mock.patch.object(fetch, "jina", return_value="# Rendered page\n\n" + "text " * 100) as jina:
            code, out, err = self.run_main(self.base + "/short")
        self.assertEqual(code, 0)
        jina.assert_called_once()
        self.assertIn("method=jina", err)
        self.assertIn("Rendered page", out)

    def test_rejects_non_http_urls(self):
        code, _, _ = self.run_main("file:///etc/passwd")
        self.assertNotEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
